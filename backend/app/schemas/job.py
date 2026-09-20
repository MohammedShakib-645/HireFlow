from pydantic import BaseModel
from typing import List, Optional
from uuid import UUID
from datetime import datetime

class RequirementBase(BaseModel):
    label: str
    category: str
    weight: float

class RequirementOut(RequirementBase):
    id: UUID
    created_at: datetime

    class Config:
        from_attributes = True

class JobCreate(BaseModel):
    title: str
    raw_jd: str

class JobOut(BaseModel):
    id: UUID
    title: str
    status: str
    requirements: List[RequirementOut]
    created_at: datetime

    class Config:
        from_attributes = True

class JDAnalyzeRequest(BaseModel):
    raw_jd: str

class JDAnalyzeResponse(BaseModel):
    job_id: UUID
    requirements: List[RequirementOut]
