from sqlalchemy import Column, String, Text, DateTime, ForeignKey, Float
from sqlalchemy.dialects.postgresql import UUID
from pgvector.sqlalchemy import Vector
import uuid
from datetime import datetime, timezone
from app.core.database import Base
from sqlalchemy.orm import relationship

class Job(Base):
    __tablename__ = "jobs"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    org_id = Column(UUID(as_uuid=True), ForeignKey("organizations.id"))
    title = Column(String, nullable=False)
    raw_jd = Column(Text, nullable=False)
    status = Column(String, default="open")
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    
    requirements = relationship("Requirement", back_populates="job", cascade="all, delete")

class Requirement(Base):
    __tablename__ = "requirements"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    job_id = Column(UUID(as_uuid=True), ForeignKey("jobs.id"))
    label = Column(String, nullable=False)
    category = Column(String, nullable=False)
    weight = Column(Float, nullable=False)
    embedding = Column(Vector(1536))
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    
    job = relationship("Job", back_populates="requirements")
