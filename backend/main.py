import json
import os
from datetime import datetime, timezone

from dotenv import load_dotenv
from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import select
from sqlalchemy.orm import Session

load_dotenv()

from .catalog import EXERCISES
from .db import Base, SessionLocal, engine, migrate_schema
from .models import Exercise, Mastery, Submission
from .runner import RunnerUnavailable, execute, execute_stdio
from .schemas import HintRequest, SubmissionRequest
from .tutor import PREREQUISITES, diagnose, next_hint, update_bkt


app = FastAPI(title="CodeMind AI", version="1.0.0", description="A local coding practice workspace for Python, Java, C, HTML, CSS, and JavaScript.")
origins = os.getenv("FRONTEND_ORIGINS", "http://localhost:5173").split(",")
app.add_middleware(CORSMiddleware, allow_origins=origins, allow_credentials=False, allow_methods=["GET", "POST"], allow_headers=["Content-Type"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def exercise_dict(exercise: Exercise, include_solution: bool = False, language: str | None = None) -> dict:
    result = {
        "id": exercise.id,
        "title": exercise.title,
        "description": exercise.description,
        "starter_code": exercise.starter_code,
        "function_name": exercise.function_name,
        "concept": exercise.concept,
        "category": exercise.category or exercise.concept,
        "difficulty": exercise.difficulty,
        "tags": exercise.tags,
        "language": exercise.language or "python",
        "execution_mode": exercise.execution_mode or "function",
        "entry_point": exercise.entry_point or "solution.py",
        "starter_files": exercise.starter_files,
        "language_starters": exercise.language_starters,
        "languages": list((exercise.language_starters or {}).keys()) if exercise.language == "multi" else [exercise.language or "python"],
        "examples": exercise.examples or [],
        "constraints": exercise.constraints or [],
        "test_count": len(exercise.tests),
    }
    if exercise.execution_mode == "browser":
        result["tests"] = exercise.tests
    if include_solution:
        result["solution"] = (exercise.language_solutions or {}).get(language or exercise.language, exercise.solution)
    return result


def attempt_dict(attempt: Submission) -> dict:
    return {
        "id": attempt.id,
        "exercise_id": attempt.exercise_id,
        "files": attempt.files,
        "language": attempt.language,
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
    migrate_schema()
    with SessionLocal() as db:
        for record in EXERCISES:
            exercise = db.get(Exercise, record["id"])
            if exercise is None:
                db.add(Exercise(**record))
            else:
                # Keep previously seeded local exercises in step with catalog
                # changes while leaving their saved submissions and mastery intact.
                for key, value in record.items():
                    if key != "id" and hasattr(exercise, key):
                        setattr(exercise, key, value)
        db.commit()


@app.get("/api/health")
def health():
    return {"status": "ok", "runner": os.getenv("RUNNER_MODE", "docker")}


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
    submitted_files = request.files
    stored_code = request.code
    language = request.language or exercise.language or "python"
    if exercise.execution_mode == "multi_language_stdio":
        if language not in (exercise.language_starters or {}):
            raise HTTPException(422, "Choose C, Python, or Java for this problem.")
    elif language != (exercise.language or "python"):
        raise HTTPException(422, "That language is not enabled for this exercise.")
    if exercise.execution_mode == "browser":
        if not submitted_files:
            raise HTTPException(422, "Web exercises require index.html, style.css, and script.js files.")
        allowed_files = {"index.html", "style.css", "script.js"}
        if set(submitted_files) - allowed_files:
            raise HTTPException(422, "Web exercise files must be named index.html, style.css, or script.js.")
        if any(not isinstance(value, str) for value in submitted_files.values()):
            raise HTTPException(422, "Web exercise files must contain text.")
        if sum(len(value.encode("utf-8")) for value in submitted_files.values()) > int(os.getenv("MAX_SOURCE_BYTES", "20000")):
            raise HTTPException(413, "Your project is too large.")
        if request.test_results is None or len(request.test_results) != len(exercise.tests):
            raise HTTPException(422, "Run all browser checks before submitting this web exercise.")
        web_results = []
        for expected_test, received in zip(exercise.tests, request.test_results):
            if not isinstance(received.get("passed"), bool):
                raise HTTPException(422, "Each browser check must include a boolean passed value.")
            web_results.append({**received, "label": expected_test.get("label", "Browser check")})
        stored_code = json.dumps(submitted_files, ensure_ascii=False)
        run = {"status": "completed", "tests": web_results, "duration_ms": 0, "message": "Browser checks completed."}
    else:
        if not request.code.strip():
            raise HTTPException(422, "Enter code before submitting.")
        try:
            if exercise.execution_mode == "multi_language_stdio":
                entry_point = {"c": "main.c", "python": "main.py", "java": "Main.java"}[language]
                run = execute_stdio(language, request.code, entry_point, exercise.tests)
            elif exercise.execution_mode == "stdin_stdout":
                run = execute_stdio(language, request.code, exercise.entry_point, exercise.tests)
            else:
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
        code=stored_code,
        language=language,
        files=submitted_files if exercise.execution_mode == "browser" else None,
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
        solution = (exercise.language_solutions or {}).get(request.language or attempt.language, exercise.solution)
        hint = next_hint(exercise.concept, attempt.hint_level, solution=solution)
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
