from pydantic import BaseModel, Field


class SubmissionRequest(BaseModel):
    exercise_id: str
    code: str = Field(default="", max_length=20000)
    files: dict[str, str] | None = None
    test_results: list[dict] | None = None
    language: str | None = None


class HintRequest(BaseModel):
    reveal_solution: bool = False
    language: str | None = None
