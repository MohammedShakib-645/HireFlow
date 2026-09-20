from pydantic import BaseModel, EmailStr
from typing import List, Optional
from uuid import UUID
from datetime import datetime

class CandidateFact(BaseModel):
    fact_type: str
    text: str
    source_span: str

class CandidateProfile(BaseModel):
    name: str
    email: str
    skills: List[str]
    experience: List[str]
    education: List[str]
    projects: List[str]
    facts: List[CandidateFact]

class CandidateOut(BaseModel):
    id: UUID
    name: str
    email: str
    status: str
    job_id: UUID
    resume_file_url: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True
