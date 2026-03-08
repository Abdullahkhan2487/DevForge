"""Projects API endpoints."""
from fastapi import APIRouter, Depends, BackgroundTasks
from sqlalchemy.orm import Session
from typing import List, Optional
from pydantic import BaseModel, Field
from datetime import datetime

from database import get_db
from services import ProjectService, WorkflowService
from core.constants import ProjectStatus, MAX_PROMPT_LENGTH, MAX_PROJECT_NAME_LENGTH, MAX_DESCRIPTION_LENGTH
from core.logging import get_logger

logger = get_logger(__name__)
router = APIRouter()


class CreateProjectRequest(BaseModel):
    """Request model for creating a project."""
    prompt: str = Field(..., max_length=MAX_PROMPT_LENGTH, description="Project idea/prompt")
    name: Optional[str] = Field(None, max_length=MAX_PROJECT_NAME_LENGTH, description="Project name")
    description: Optional[str] = Field(None, max_length=MAX_DESCRIPTION_LENGTH, description="Project description")


class ProjectResponse(BaseModel):
    """Response model for project."""
    id: int
    name: str
    description: Optional[str]
    prompt: str
    status: str
    created_at: datetime
    updated_at: datetime
    project_path: Optional[str]
    metadata: dict
    
    class Config:
        from_attributes = True


class ProjectFileResponse(BaseModel):
    """Response model for project files."""
    path: str
    content: Optional[str]
    size: int
    error: Optional[str] = None


@router.post("", response_model=ProjectResponse, status_code=201)
async def create_project(
    request: CreateProjectRequest,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    """Create a new project and start the agent workflow."""
    project_service = ProjectService(db)
    
    # Create project
    project = project_service.create_project(
        prompt=request.prompt,
        name=request.name,
        description=request.description
    )
    
    # Start workflow in background
    def run_workflow_wrapper():
        """Wrapper to create new DB session for background task."""
        from database import SessionLocal
        db_session = SessionLocal()
        try:
            workflow_service = WorkflowService(db_session)
            import asyncio
            asyncio.run(workflow_service.execute_workflow(project.id, request.prompt))
        finally:
            db_session.close()
    
    background_tasks.add_task(run_workflow_wrapper)
    
    logger.info(f"Project {project.id} created and workflow started")
    return project


@router.get("", response_model=List[ProjectResponse])
async def list_projects(
    skip: int = 0,
    limit: int = 100,
    status: Optional[ProjectStatus] = None,
    db: Session = Depends(get_db)
):
    """List all projects with optional status filter."""
    project_service = ProjectService(db)
    projects = project_service.list_projects(skip=skip, limit=limit, status=status)
    return projects


@router.get("/{project_id}", response_model=ProjectResponse)
async def get_project(project_id: int, db: Session = Depends(get_db)):
    """Get a specific project by ID."""
    project_service = ProjectService(db)
    project = project_service.get_project(project_id)
    return project


@router.get("/{project_id}/files", response_model=List[ProjectFileResponse])
async def get_project_files(project_id: int, db: Session = Depends(get_db)):
    """Get all files in a project."""
    project_service = ProjectService(db)
    files = project_service.get_project_files(project_id)
    return files


@router.delete("/{project_id}", status_code=204)
async def delete_project(project_id: int, db: Session = Depends(get_db)):
    """Delete a project and its files."""
    project_service = ProjectService(db)
    project_service.delete_project(project_id)
    return None
    
    # Delete project files
    if project.project_path and os.path.exists(project.project_path):
        shutil.rmtree(project.project_path)
    
    # Delete from database
    db.delete(project)
    db.commit()
    
    return {"message": "Project deleted successfully"}
