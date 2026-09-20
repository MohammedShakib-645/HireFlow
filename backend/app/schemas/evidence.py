from pydantic import BaseModel
from typing import Any, Optional
from uuid import UUID
from datetime import datetime

class EvidenceItem(BaseModel):
    id: UUID
    candidate_id: UUID
    requirement_id: UUID
    requirement_label: str
    source: Optional[str]
    source_reference: Optional[str]
    confidence: Optional[float]
    score: Optional[float]
    status: str
    created_at: datetime

    class Config:
        from_attributes = True

class EvidenceUpdateRequest(BaseModel):
    interview_transcript: str
    notes: Optional[str] = None

class EvidenceHistoryItem(BaseModel):
    event: str
    delta: Any
    actor: str
    timestamp: datetime

    class Config:
        from_attributes = True
