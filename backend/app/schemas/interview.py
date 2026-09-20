from pydantic import BaseModel
from typing import Any
from uuid import UUID
from datetime import datetime

class QuestionOut(BaseModel):
    id: UUID
    evidence_id: UUID
    gap_type: str
    prompt: str
    follow_up_branches: Any
    created_at: datetime

    class Config:
        from_attributes = True

class ResponseCreate(BaseModel):
    transcript: str

class ResponseOut(BaseModel):
    id: UUID
    question_id: UUID
    outcome: str
    created_at: datetime

    class Config:
        from_attributes = True
