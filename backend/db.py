import os
from pathlib import Path

from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import DeclarativeBase, sessionmaker


DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./data/codemind.db")
if DATABASE_URL.startswith("sqlite"):
    Path("data").mkdir(exist_ok=True)
    engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
else:
    engine = create_engine(DATABASE_URL, pool_pre_ping=True)

SessionLocal = sessionmaker(bind=engine, autoflush=False, expire_on_commit=False)


class Base(DeclarativeBase):
    pass


def migrate_schema():
    """Add language and multi-file columns to existing local prototype databases."""
    additions = {
        "exercises": {
            "category": "VARCHAR(80) NOT NULL DEFAULT 'Python fundamentals'",
            "language": "VARCHAR(20) NOT NULL DEFAULT 'python'",
            "execution_mode": "VARCHAR(30) NOT NULL DEFAULT 'function'",
            "entry_point": "VARCHAR(100) NOT NULL DEFAULT 'solution.py'",
            "starter_files": "JSON",
            "language_starters": "JSON",
            "language_solutions": "JSON",
            "examples": "JSON",
            "constraints": "JSON",
        },
        "submissions": {"files": "JSON", "language": "VARCHAR(20) NOT NULL DEFAULT 'python'"},
    }
    with engine.begin() as connection:
        inspector = inspect(connection)
        for table, columns in additions.items():
            existing = {column["name"] for column in inspector.get_columns(table)}
            for name, definition in columns.items():
                if name not in existing:
                    connection.exec_driver_sql(f"ALTER TABLE {table} ADD COLUMN {name} {definition}")
