from pydantic import BaseModel, Field, validator
from typing import List, Optional
from datetime import date

class Task(BaseModel):
    title: str
    due_date: Optional[date] = None
    source: str = "doctor"
    confidence: float = Field(ge=0.0, le=1.0, default=0.8)

    @validator("title")
    def title_not_empty(cls, v):
        if not v or not v.strip():
            raise ValueError("Task title cannot be empty")
        return v.strip()

class CoachOutput(BaseModel):
    checklist: List[str] = []
    cautions: List[str] = []
    questions_for_doctor: List[str] = []
