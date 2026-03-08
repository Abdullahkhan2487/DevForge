"""Projects API endpoints."""
from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime

from database import get_db, Project
from workflows.orchestrator import WorkflowOrchestrator

router = APIRouter()


class CreateProjectRequest(BaseModel):
    """Request model for creating a project."""
    prompt: str
    name: Optional[str] = None
    description: Optional[str] = None


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


def serialize_project(project: Project) -> ProjectResponse:
    """Map ORM model to API response schema explicitly."""
    return ProjectResponse(
        id=project.id,
        name=project.name,
        description=project.description,
        prompt=project.prompt,
        status=project.status,
        created_at=project.created_at,
        updated_at=project.updated_at,
        project_path=project.project_path,
        metadata=project.project_metadata or {}
    )


@router.post("", response_model=ProjectResponse)
async def create_project(
    request: CreateProjectRequest,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    """Create a new project and start the agent workflow."""
    
    # Create project record
    project = Project(
        name=request.name or f"Project {datetime.utcnow().strftime('%Y%m%d_%H%M%S')}",
        description=request.description,
        prompt=request.prompt,
        status="pending"
    )
    
    db.add(project)
    db.commit()
    db.refresh(project)
    
    # Start workflow in background
    background_tasks.add_task(run_workflow, project.id, request.prompt, db)
    
    return serialize_project(project)


async def run_workflow(project_id: int, prompt: str, db: Session):
    """Run the agent workflow for a project."""
    orchestrator = WorkflowOrchestrator(project_id, db)
    await orchestrator.execute(prompt)


@router.get("", response_model=List[ProjectResponse])
async def list_projects(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """List all projects."""
    projects = db.query(Project).order_by(Project.created_at.desc()).offset(skip).limit(limit).all()
    return [serialize_project(project) for project in projects]


@router.get("/{project_id}", response_model=ProjectResponse)
async def get_project(project_id: int, db: Session = Depends(get_db)):
    """Get a specific project by ID."""
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return serialize_project(project)


@router.get("/{project_id}/files")
async def get_project_files(project_id: int, db: Session = Depends(get_db)):
    """Get all files in a project."""
    import os
    from pathlib import Path
    
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    if not project.project_path or not os.path.exists(project.project_path):
        return {"files": []}
    
    files = []
    project_path = Path(project.project_path)
    
    for file_path in project_path.rglob('*'):
        if file_path.is_file():
            relative_path = file_path.relative_to(project_path)
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                files.append({
                    "path": str(relative_path),
                    "content": content,
                    "size": file_path.stat().st_size
                })
            except:
                files.append({
                    "path": str(relative_path),
                    "content": None,
                    "size": file_path.stat().st_size,
                    "binary": True
                })
    
    return {"files": files}


@router.delete("/{project_id}")
async def delete_project(project_id: int, db: Session = Depends(get_db)):
    """Delete a project."""
    import os
    import shutil
    
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    # Delete project files
    if project.project_path and os.path.exists(project.project_path):
        shutil.rmtree(project.project_path)
    
    # Delete from database
    db.delete(project)
    db.commit()
    
    return {"message": "Project deleted successfully"}
