from sqlalchemy import Column, String, Text, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from pgvector.sqlalchemy import Vector
import uuid
from datetime import datetime, timezone
from app.core.database import Base
from sqlalchemy.orm import relationship

class Candidate(Base):
    __tablename__ = "candidates"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    org_id = Column(UUID(as_uuid=True), ForeignKey("organizations.id"))
    job_id = Column(UUID(as_uuid=True), ForeignKey("jobs.id"))
    name = Column(String, nullable=False)
    email = Column(String, nullable=False)
    resume_file_url = Column(String)
    status = Column(String, default="new")
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    
    facts = relationship("CandidateFact", back_populates="candidate", cascade="all, delete")

class CandidateFact(Base):
    __tablename__ = "candidate_facts"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    candidate_id = Column(UUID(as_uuid=True), ForeignKey("candidates.id"))
    fact_type = Column(String, nullable=False)
    text = Column(Text, nullable=False)
    source_span = Column(String)
    embedding = Column(Vector(1536))
    
    candidate = relationship("Candidate", back_populates="facts")
