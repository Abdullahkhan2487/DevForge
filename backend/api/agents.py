"""Agents API endpoints."""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime

from database import get_db
from services import AgentLogService
from core.constants import AgentName
from core.logging import get_logger

logger = get_logger(__name__)
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


class AgentInfo(BaseModel):
    """Agent information model."""
    name: str
    role: str
    status: str
    description: str


class AgentsStatusResponse(BaseModel):
    """Response model for agents status."""
    agents: List[AgentInfo]
    total: int


@router.get("/logs", response_model=List[AgentLogResponse])
async def get_agent_logs(
    project_id: Optional[int] = None,
    agent_name: Optional[str] = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Get agent activity logs with optional filtering."""
    agent_log_service = AgentLogService(db)
    logs = agent_log_service.get_logs(
        project_id=project_id,
        agent_name=agent_name,
        skip=skip,
        limit=limit
    )
    return logs


@router.get("/status", response_model=AgentsStatusResponse)
async def get_agents_status():
    """Get status of all available agents."""
    agents_info = [
        AgentInfo(
            name=AgentName.PRODUCT_MANAGER.value,
            role="Product Manager",
            status="available",
            description="Analyzes product ideas and creates comprehensive PRD"
        ),
        AgentInfo(
            name=AgentName.SOFTWARE_ARCHITECT.value,
            role="Software Architect",
            status="available",
            description="Designs system architecture and database schema"
        ),
        AgentInfo(
            name=AgentName.BACKEND_DEVELOPER.value,
            role="Backend Developer",
            status="available",
            description="Generates backend APIs and services"
        ),
        AgentInfo(
            name=AgentName.FRONTEND_DEVELOPER.value,
            role="Frontend Developer",
            status="available",
            description="Builds responsive frontend UI with React/Next.js"
        ),
        AgentInfo(
            name=AgentName.QA_TESTER.value,
            role="QA Tester",
            status="available",
            description="Generates comprehensive test suites"
        ),
        AgentInfo(
            name=AgentName.CODE_REVIEWER.value,
            role="Code Reviewer",
            status="available",
            description="Reviews code quality and provides optimization suggestions"
        )
    ]
    
    return AgentsStatusResponse(agents=agents_info, total=len(agents_info))
