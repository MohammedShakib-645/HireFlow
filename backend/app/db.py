"""HireFlow backend: 7 separable agent stages + audit trail. SQLite default, Postgres via DATABASE_URL."""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os
DB_URL=os.environ.get("DATABASE_URL","sqlite:///./hireflow.db")
KW={"check_same_thread":False} if DB_URL.startswith("sqlite") else {}
engine=create_engine(DB_URL,connect_args=KW,pool_pre_ping=True)
Session=sessionmaker(bind=engine,autoflush=False,autocommit=False)
Base=declarative_base()
def get_db():
    db=Session()
    try:yield db
    finally:db.close()
