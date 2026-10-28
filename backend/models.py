from datetime import datetime, timezone

from sqlalchemy import Boolean, DateTime, Float, ForeignKey, Integer, JSON, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from .db import Base


def now_utc():
    return datetime.now(timezone.utc)


class Exercise(Base):
    __tablename__ = "exercises"

    id: Mapped[str] = mapped_column(String(80), primary_key=True)
    title: Mapped[str] = mapped_column(String(160))
    description: Mapped[str] = mapped_column(Text)
    starter_code: Mapped[str] = mapped_column(Text)
    function_name: Mapped[str] = mapped_column(String(100))
    tests: Mapped[list] = mapped_column(JSON)
    solution: Mapped[str] = mapped_column(Text)
    concept: Mapped[str] = mapped_column(String(100), index=True)
    difficulty: Mapped[str] = mapped_column(String(30))
    tags: Mapped[list] = mapped_column(JSON, default=list)
    category: Mapped[str] = mapped_column(String(80), default="Python fundamentals")
    language: Mapped[str] = mapped_column(String(20), default="python")
    execution_mode: Mapped[str] = mapped_column(String(30), default="function")
    entry_point: Mapped[str] = mapped_column(String(100), default="solution.py")
    starter_files: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    language_starters: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    language_solutions: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    examples: Mapped[list | None] = mapped_column(JSON, nullable=True)
    constraints: Mapped[list | None] = mapped_column(JSON, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=now_utc)


class Submission(Base):
    __tablename__ = "submissions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    exercise_id: Mapped[str] = mapped_column(ForeignKey("exercises.id"), index=True)
    code: Mapped[str] = mapped_column(Text)
    language: Mapped[str] = mapped_column(String(20), default="python")
    files: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    passed: Mapped[bool] = mapped_column(Boolean)
    status: Mapped[str] = mapped_column(String(40))
    diagnosis: Mapped[dict] = mapped_column(JSON)
    test_results: Mapped[list] = mapped_column(JSON)
    duration_ms: Mapped[int] = mapped_column(Integer, default=0)
    hint_level: Mapped[int] = mapped_column(Integer, default=0)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=now_utc)


class Mastery(Base):
    __tablename__ = "mastery"

    concept: Mapped[str] = mapped_column(String(100), primary_key=True)
    probability: Mapped[float] = mapped_column(Float, default=0.25)
    attempts: Mapped[int] = mapped_column(Integer, default=0)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=now_utc)
