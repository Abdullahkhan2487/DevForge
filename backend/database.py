"""Database configuration and models."""
from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from config import settings

# Create engine
engine = create_engine(
    settings.database_url,
    connect_args={"check_same_thread": False} if "sqlite" in settings.database_url else {}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


class Project(Base):
    """Project model."""
    __tablename__ = "projects"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(Text)
    prompt = Column(Text)
    status = Column(String, default="pending")  # pending, in_progress, completed, failed
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    project_path = Column(String)
    project_metadata = Column("metadata", JSON, default={})


class AgentLog(Base):
    """Agent activity log model."""
    __tablename__ = "agent_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, index=True)
    agent_name = Column(String)
    agent_role = Column(String)
    status = Column(String)  # started, in_progress, completed, failed
    input_data = Column(JSON)
    output_data = Column(JSON)
    logs = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime, nullable=True)


async def init_db():
    """Initialize database tables."""
    Base.metadata.create_all(bind=engine)


def get_db():
    """Get database session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
