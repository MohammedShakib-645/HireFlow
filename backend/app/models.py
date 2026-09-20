"""Postgres-ready schema (SQLite-compatible dev). pgvector columns are optional: embedding stored as JSON text in dev, VECTOR in prod."""
from sqlalchemy import Column,String,Integer,Float,Text,DateTime,ForeignKey,JSON
from datetime import datetime
from .db import Base
import uuid
def nid():return uuid.uuid4().hex[:12]
class Org(Base):
    __tablename__="organizations";id=Column(String,primary_key=True,default=nid);name=Column(String,default="Demo Org");created_at=Column(DateTime,default=datetime.utcnow)
class User(Base):
    __tablename__="users";id=Column(String,primary_key=True,default=nid);org_id=Column(String,ForeignKey("organizations.id"));email=Column(String,unique=True);hashed_password=Column(String);role=Column(String,default="recruiter")
class Job(Base):
    __tablename__="jobs";id=Column(String,primary_key=True,default=nid);org_id=Column(String);title=Column(String);raw_jd=Column(Text);status=Column(String,default="draft");created_at=Column(DateTime,default=datetime.utcnow)
class Requirement(Base):
    __tablename__="requirements";id=Column(String,primary_key=True,default=nid);job_id=Column(String,ForeignKey("jobs.id"));label=Column(String);category=Column(String);weight=Column(Integer,default=3);created_at=Column(DateTime,default=datetime.utcnow)
class Candidate(Base):
    __tablename__="candidates";id=Column(String,primary_key=True,default=nid);org_id=Column(String);job_id=Column(String,ForeignKey("jobs.id"));name=Column(String);email=Column(String,default="");resume_file_url=Column(String,default="");resume_text=Column(Text,default="");status=Column(String,default="uploaded");created_at=Column(DateTime,default=datetime.utcnow)
class CandidateFact(Base):
    __tablename__="candidate_facts";id=Column(String,primary_key=True,default=nid);candidate_id=Column(String,ForeignKey("candidates.id"));fact_type=Column(String);text=Column(Text);source_span=Column(Text,default="");embedding=Column(JSON,default=list)
class Evidence(Base):
    __tablename__="evidence";id=Column(String,primary_key=True,default=nid);candidate_id=Column(String,ForeignKey("candidates.id"));requirement_id=Column(String,ForeignKey("requirements.id"));source=Column(String);source_reference=Column(Text,default="");confidence=Column(String,default="low");score=Column(Float,default=0);status=Column(String,default="missing");created_at=Column(DateTime,default=datetime.utcnow);updated_at=Column(DateTime,default=datetime.utcnow)
class EvidenceHistory(Base):
    __tablename__="evidence_history";id=Column(String,primary_key=True,default=nid);evidence_id=Column(String,ForeignKey("evidence.id"));event=Column(String);delta=Column(String,default="+0");actor=Column(String,default="agent");timestamp=Column(DateTime,default=datetime.utcnow)
class InterviewQ(Base):
    __tablename__="interview_questions";id=Column(String,primary_key=True,default=nid);evidence_id=Column(String,ForeignKey("evidence.id"));gap_type=Column(String);prompt=Column(Text);created_at=Column(DateTime,default=datetime.utcnow)
class InterviewR(Base):
    __tablename__="interview_responses";id=Column(String,primary_key=True,default=nid);question_id=Column(String,ForeignKey("interview_questions.id"));transcript=Column(Text);outcome=Column(String);created_at=Column(DateTime,default=datetime.utcnow)
class Report(Base):
    __tablename__="reports";id=Column(String,primary_key=True,default=nid);candidate_id=Column(String,ForeignKey("candidates.id"));job_id=Column(String,ForeignKey("jobs.id"));coverage_pct=Column(Float,default=0);payload=Column(JSON,default=dict);generated_at=Column(DateTime,default=datetime.utcnow)
class AuditLog(Base):
    __tablename__="audit_log";id=Column(String,primary_key=True,default=nid);org_id=Column(String,default="demo");agent_name=Column(String);input_ref=Column(String,default="");output_ref=Column(String,default="");model_used=Column(String,default="local");timestamp=Column(DateTime,default=datetime.utcnow)
