from sqlalchemy import Column, String, Text, DateTime, ForeignKey, Float
from sqlalchemy.dialects.postgresql import UUID, JSONB
import uuid
from datetime import datetime, timezone
from app.core.database import Base
from sqlalchemy.orm import relationship

class Evidence(Base):
    __tablename__ = "evidence"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    candidate_id = Column(UUID(as_uuid=True), ForeignKey("candidates.id"))
    requirement_id = Column(UUID(as_uuid=True), ForeignKey("requirements.id"))
    source = Column(String)
    source_reference = Column(Text)
    confidence = Column(Float)
    score = Column(Float)
    status = Column(String) # verified, needs_validation, missing
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
    
    history = relationship("EvidenceHistory", back_populates="evidence", cascade="all, delete")

class EvidenceHistory(Base):
    __tablename__ = "evidence_history"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    evidence_id = Column(UUID(as_uuid=True), ForeignKey("evidence.id"))
    event = Column(String)
    delta = Column(JSONB)
    actor = Column(String)
    timestamp = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    
    evidence = relationship("Evidence", back_populates="history")
