from pydantic import BaseModel, Field


class SubmissionRequest(BaseModel):
    exercise_id: str
    code: str = Field(min_length=1, max_length=20000)


class HintRequest(BaseModel):
    reveal_solution: bool = False
