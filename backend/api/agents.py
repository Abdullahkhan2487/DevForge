"""Agents API endpoints."""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime

from database import get_db, AgentLog

router = APIRouter()


class AgentLogResponse(BaseModel):
    """Response model for agent log."""
    id: int
    project_id: int
    agent_name: str
    agent_role: str
    status: str
    input_data: Optional[dict]
    output_data: Optional[dict]
    logs: Optional[str]
    created_at: datetime
    completed_at: Optional[datetime]
    
    class Config:
        from_attributes = True


@router.get("/logs", response_model=List[AgentLogResponse])
async def get_agent_logs(
    project_id: Optional[int] = None,
    agent_name: Optional[str] = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Get agent activity logs."""
    query = db.query(AgentLog)
    
    if project_id:
        query = query.filter(AgentLog.project_id == project_id)
    
    if agent_name:
        query = query.filter(AgentLog.agent_name == agent_name)
    
    logs = query.order_by(AgentLog.created_at.desc()).offset(skip).limit(limit).all()
    return logs


@router.get("/status")
async def get_agents_status():
    """Get status of all available agents."""
    return {
        "agents": [
            {
                "name": "ProductManagerAgent",
                "role": "Product Manager",
                "status": "available",
                "description": "Analyzes product ideas and creates PRD"
            },
            {
                "name": "SoftwareArchitectAgent",
                "role": "Software Architect",
                "status": "available",
                "description": "Designs system architecture and database schema"
            },
            {
                "name": "BackendDeveloperAgent",
                "role": "Backend Developer",
                "status": "available",
                "description": "Generates backend APIs and services"
            },
            {
                "name": "FrontendDeveloperAgent",
                "role": "Frontend Developer",
                "status": "available",
                "description": "Builds responsive frontend UI"
            },
            {
                "name": "QATesterAgent",
                "role": "QA Tester",
                "status": "available",
                "description": "Generates comprehensive tests"
            },
            {
                "name": "CodeReviewerAgent",
                "role": "Code Reviewer",
                "status": "available",
                "description": "Reviews and optimizes code"
            }
        ],
        "total": 6
    }
