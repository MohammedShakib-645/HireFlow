from pydantic import BaseModel
from typing import List, Optional, Any
from uuid import UUID
from datetime import datetime

class ReportPayload(BaseModel):
    coverage_pct: float
    verified_count: int
    needs_validation_count: int
    missing_count: int
    verified_skills: List[str]
    gaps: List[str]
    interview_insights: List[str]
    recommendations: List[str]
    audit_note: str = "AI analyzes the evidence. Human makes the final decision."

class ReportOut(BaseModel):
    id: UUID
    candidate_id: UUID
    job_id: UUID
    coverage_pct: float
    payload: ReportPayload
    generated_at: datetime

    class Config:
        from_attributes = True
