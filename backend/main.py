import os
from datetime import datetime, timezone

from dotenv import load_dotenv
from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import select
from sqlalchemy.orm import Session

load_dotenv()

from .catalog import EXERCISES
from .db import Base, SessionLocal, engine
from .models import Exercise, Mastery, Submission
from .runner import RunnerUnavailable, execute
from .schemas import HintRequest, SubmissionRequest
from .tutor import PREREQUISITES, diagnose, next_hint, update_bkt


app = FastAPI(title="CodeMind AI", version="1.0.0", description="An evidence-based adaptive tutor for Python programming.")
origins = os.getenv("FRONTEND_ORIGINS", "http://localhost:5173").split(",")
app.add_middleware(CORSMiddleware, allow_origins=origins, allow_credentials=False, allow_methods=["GET", "POST"], allow_headers=["Content-Type"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def exercise_dict(exercise: Exercise, include_solution: bool = False) -> dict:
    result = {
        "id": exercise.id,
        "title": exercise.title,
        "description": exercise.description,
        "starter_code": exercise.starter_code,
        "function_name": exercise.function_name,
        "concept": exercise.concept,
        "difficulty": exercise.difficulty,
        "tags": exercise.tags,
        "test_count": len(exercise.tests),
    }
    if include_solution:
        result["solution"] = exercise.solution
    return result


def attempt_dict(attempt: Submission) -> dict:
    return {
        "id": attempt.id,
        "exercise_id": attempt.exercise_id,
        "passed": attempt.passed,
        "status": attempt.status,
        "diagnosis": attempt.diagnosis,
        "test_results": attempt.test_results,
        "duration_ms": attempt.duration_ms,
        "hint_level": attempt.hint_level,
        "created_at": attempt.created_at.isoformat() if attempt.created_at else None,
    }


@app.on_event("startup")
def startup():
    Base.metadata.create_all(bind=engine)
    with SessionLocal() as db:
        for record in EXERCISES:
            if db.get(Exercise, record["id"]) is None:
                db.add(Exercise(**record))
        db.commit()


@app.get("/api/health")
def health():
    return {"status": "ok", "runner": "isolated-docker"}


@app.get("/api/exercises")
def list_exercises(db: Session = Depends(get_db)):
    exercises = db.scalars(select(Exercise).order_by(Exercise.difficulty, Exercise.title)).all()
    return [exercise_dict(item) for item in exercises]


@app.get("/api/exercises/{exercise_id}")
def get_exercise(exercise_id: str, db: Session = Depends(get_db)):
    exercise = db.get(Exercise, exercise_id)
    if exercise is None:
        raise HTTPException(404, "Exercise not found")
    return exercise_dict(exercise)


@app.post("/api/submissions")
def submit(request: SubmissionRequest, db: Session = Depends(get_db)):
    exercise = db.get(Exercise, request.exercise_id)
    if exercise is None:
        raise HTTPException(404, "Exercise not found")
    try:
        run = execute(request.code, exercise.function_name, exercise.tests)
    except RunnerUnavailable as error:
        raise HTTPException(503, str(error)) from error
    diagnosis = diagnose(exercise_dict(exercise), request.code, run)
    prior_failures = db.scalars(
        select(Submission)
        .where(Submission.exercise_id == exercise.id, Submission.passed.is_(False))
        .order_by(Submission.created_at.desc())
        .limit(10)
    ).all()
    similar_count = sum(1 for prior in prior_failures if prior.diagnosis.get("title") == diagnosis["title"])
    diagnosis["similar_attempts"] = similar_count
    if similar_count:
        diagnosis["evidence"].append(f"A similar test outcome appeared in {similar_count} earlier attempt(s) on this exercise.")
    passed = run["status"] == "completed" and bool(run["tests"]) and all(test.get("passed") for test in run["tests"])
    attempt = Submission(
        exercise_id=exercise.id,
        code=request.code,
        passed=passed,
        status=run["status"],
        diagnosis=diagnosis,
        test_results=run.get("tests", []),
        duration_ms=run.get("duration_ms", 0),
    )
    db.add(attempt)
    mastery = db.get(Mastery, exercise.concept)
    if mastery is None:
        mastery = Mastery(concept=exercise.concept, probability=0.25, attempts=0)
        db.add(mastery)
    mastery.probability = update_bkt(mastery.probability, passed)
    mastery.attempts += 1
    mastery.updated_at = datetime.now(timezone.utc)
    db.commit()
    db.refresh(attempt)
    return {**attempt_dict(attempt), "message": run.get("message", "")}


@app.get("/api/attempts")
def list_attempts(limit: int = 30, db: Session = Depends(get_db)):
    limit = min(max(limit, 1), 100)
    attempts = db.scalars(select(Submission).order_by(Submission.created_at.desc()).limit(limit)).all()
    return [attempt_dict(item) for item in attempts]


@app.get("/api/attempts/{attempt_id}")
def get_attempt(attempt_id: int, db: Session = Depends(get_db)):
    attempt = db.get(Submission, attempt_id)
    if attempt is None:
        raise HTTPException(404, "Attempt not found")
    return {**attempt_dict(attempt), "code": attempt.code}


@app.post("/api/attempts/{attempt_id}/hints")
def get_hint(attempt_id: int, request: HintRequest, db: Session = Depends(get_db)):
    attempt = db.get(Submission, attempt_id)
    if attempt is None:
        raise HTTPException(404, "Attempt not found")
    exercise = db.get(Exercise, attempt.exercise_id)
    if request.reveal_solution:
        hint = next_hint(exercise.concept, attempt.hint_level, solution=exercise.solution)
    else:
        hint = next_hint(exercise.concept, attempt.hint_level)
        attempt.hint_level = max(attempt.hint_level, hint["level"])
        db.commit()
    return hint


@app.get("/api/mastery")
def mastery_summary(db: Session = Depends(get_db)):
    records = {row.concept: row for row in db.scalars(select(Mastery)).all()}
    concepts = sorted({exercise["concept"] for exercise in EXERCISES})
    return [
        {
            "concept": concept,
            "probability": round(records[concept].probability if concept in records else 0.25, 3),
            "attempts": records[concept].attempts if concept in records else 0,
        }
        for concept in concepts
    ]


@app.get("/api/concepts")
def concept_graph(db: Session = Depends(get_db)):
    records = {row.concept: row for row in db.scalars(select(Mastery)).all()}
    nodes = [{
        "id": concept,
        "mastery": round(records[concept].probability if concept in records else 0.25, 3),
        "attempts": records[concept].attempts if concept in records else 0,
    } for concept in sorted(PREREQUISITES)]
    edges = [{"from": prerequisite, "to": concept} for concept, dependencies in PREREQUISITES.items() for prerequisite in dependencies]
    return {"nodes": nodes, "edges": edges}


@app.get("/api/recommendation")
def recommendation(db: Session = Depends(get_db)):
    exercises = db.scalars(select(Exercise)).all()
    attempted = set(db.scalars(select(Submission.exercise_id).distinct()).all())
    mastery = {row.concept: row.probability for row in db.scalars(select(Mastery)).all()}
    candidates = [exercise for exercise in exercises if exercise.id not in attempted]
    eligible = [exercise for exercise in candidates if all(mastery.get(prerequisite, 0.25) >= 0.35 for prerequisite in PREREQUISITES.get(exercise.concept, []))]
    candidates = eligible or candidates
    if not candidates:
        candidates = exercises
    if not candidates:
        return {"exercise": None, "reason": "No exercises are available yet."}
    candidate = min(candidates, key=lambda item: mastery.get(item.concept, 0.25))
    probability = mastery.get(candidate.concept, 0.25)
    prerequisites = PREREQUISITES.get(candidate.concept, [])
    reason = f"This is a {candidate.difficulty.lower()} exercise for {candidate.concept.lower()}, an area with an estimated mastery of {round(probability * 100)}%."
    if prerequisites:
        reason += f" It follows practice with {', '.join(prerequisites).lower()}."
    return {"exercise": exercise_dict(candidate), "reason": reason}


@app.get("/api/progress")
def progress(db: Session = Depends(get_db)):
    submissions = db.scalars(select(Submission).order_by(Submission.created_at.desc())).all()
    return {
        "attempts": len(submissions),
        "passed": sum(1 for attempt in submissions if attempt.passed),
        "concept_count": len({exercise["concept"] for exercise in EXERCISES}),
        "recent": [attempt_dict(item) for item in submissions[:5]],
    }
