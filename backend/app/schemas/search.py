from pydantic import BaseModel
from typing import Optional
from uuid import UUID

class CandidateSearchResult(BaseModel):
    candidate_id: UUID
    name: str
    matching_evidence_snippet: str
    similarity_score: float
    status: str
