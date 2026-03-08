"""Project service for business logic."""
from typing import List, Optional
from pathlib import Path
from datetime import datetime
from sqlalchemy.orm import Session

from repositories import ProjectRepository
from database import Project
from core.constants import ProjectStatus
from core.logging import get_logger
from core.security import (
    validate_project_prompt,
    validate_project_name,
    validate_project_description,
    validate_file_path,
    validate_file_extension,
    validate_file_size
)
from core.exceptions import NotFoundError, ValidationError

logger = get_logger(__name__)


class ProjectService:
    """Service for project-related business logic."""
    
    def __init__(self, db: Session):
        """
        Initialize service.
        
        Args:
            db: Database session
        """
        self.db = db
        self.repository = ProjectRepository(db)
    
    def create_project(
        self,
        prompt: str,
        name: Optional[str] = None,
        description: Optional[str] = None
    ) -> Project:
        """
        Create a new project with validation.
        
        Args:
            prompt: Project prompt/idea
            name: Optional project name
            description: Optional project description
        
        Returns:
            Created project
        
        Raises:
            ValidationError: If input validation fails
        """
        # Validate and sanitize inputs
        prompt = validate_project_prompt(prompt)
        name = validate_project_name(name) if name else None
        description = validate_project_description(description) if description else None
        
        # Generate default name if not provided
        if not name:
            name = f"Project {datetime.utcnow().strftime('%Y%m%d_%H%M%S')}"
        
        # Create project
        project = self.repository.create(
            name=name,
            description=description,
            prompt=prompt,
            status=ProjectStatus.PENDING.value
        )
        
        logger.info(f"Project created successfully: {project.id}")
        return project
    
    def get_project(self, project_id: int) -> Project:
        """
        Get project by ID.
        
        Args:
            project_id: Project ID
        
        Returns:
            Project
        
        Raises:
            NotFoundError: If project not found
        """
        return self.repository.get_or_404(project_id)
    
    def list_projects(
        self,
        skip: int = 0,
        limit: int = 100,
        status: Optional[ProjectStatus] = None
    ) -> List[Project]:
        """
        List projects with optional filtering.
        
        Args:
            skip: Number of records to skip
            limit: Maximum number of records
            status: Optional status filter
        
        Returns:
            List of projects
        """
        if status:
            return self.repository.get_by_status(status, skip, limit)
        return self.repository.get_all(skip, limit)
    
    def update_project_status(self, project_id: int, status: ProjectStatus) -> Project:
        """
        Update project status.
        
        Args:
            project_id: Project ID
            status: New status
        
        Returns:
            Updated project
        
        Raises:
            NotFoundError: If project not found
        """
        project = self.repository.update_status(project_id, status)
        logger.info(f"Project {project_id} status updated to {status.value}")
        return project
    
    def update_project_path(self, project_id: int, path: str) -> Project:
        """
        Update project path after generation.
        
        Args:
            project_id: Project ID
            path: Project directory path
        
        Returns:
            Updated project
        
        Raises:
            NotFoundError: If project not found
        """
        project = self.repository.update(project_id, project_path=path)
        logger.info(f"Project {project_id} path updated")
        return project
    
    def update_project_metadata(
        self,
        project_id: int,
        metadata: dict
    ) -> Project:
        """
        Update project metadata.
        
        Args:
            project_id: Project ID
            metadata: Metadata dictionary
        
        Returns:
            Updated project
        
        Raises:
            NotFoundError: If project not found
        """
        project = self.repository.update(project_id, project_metadata=metadata)
        logger.info(f"Project {project_id} metadata updated")
        return project
    
    def delete_project(self, project_id: int) -> bool:
        """
        Delete a project.
        
        Args:
            project_id: Project ID
        
        Returns:
            True if deleted successfully
        
        Raises:
            NotFoundError: If project not found
        """
        # Get project to check if it exists and get path
        project = self.repository.get_or_404(project_id)
        
        # Delete from database
        self.repository.delete(project_id)
        
        # Optionally delete project files
        if project.project_path:
            try:
                import shutil
                project_path = Path(project.project_path)
                if project_path.exists():
                    shutil.rmtree(project_path)
                    logger.info(f"Deleted project files at {project_path}")
            except Exception as e:
                logger.warning(f"Failed to delete project files: {str(e)}")
        
        logger.info(f"Project {project_id} deleted successfully")
        return True
    
    def get_project_files(self, project_id: int) -> List[dict]:
        """
        Get all files in a project with security validation.
        
        Args:
            project_id: Project ID
        
        Returns:
            List of file information dicts
        
        Raises:
            NotFoundError: If project not found
            ValidationError: If project has no files
        """
        project = self.repository.get_or_404(project_id)
        
        if not project.project_path:
            raise ValidationError("Project has no generated files")
        
        base_path = Path(project.project_path)
        if not base_path.exists():
            raise ValidationError("Project directory does not exist")
        
        files = []
        for file_path in base_path.rglob('*'):
            if file_path.is_file():
                try:
                    # Validate file path (prevent path traversal)
                    validated_path = validate_file_path(file_path, base_path)
                    
                    # Validate file extension
                    validate_file_extension(validated_path)
                    
                    # Validate file size
                    validate_file_size(validated_path)
                    
                    # Read files content
                    relative_path = validated_path.relative_to(base_path)
                    with open(validated_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    files.append({
                        "path": str(relative_path),
                        "content": content,
                        "size": validated_path.stat().st_size
                    })
                except Exception as e:
                    # Log error but continue with other files
                    logger.warning(
                        f"Skipping file {file_path}: {str(e)}",
                        extra={"project_id": project_id}
                    )
                    files.append({
                        "path": str(file_path.relative_to(base_path)),
                        "content": None,
                        "size": file_path.stat().st_size,
                        "error": "File not readable or not allowed"
                    })
        
        return files
    
    def search_projects(self, name: str, skip: int = 0, limit: int = 100) -> List[Project]:
        """
        Search projects by name.
        
        Args:
            name: Name to search for
            skip: Number of records to skip
            limit: Maximum number of records
        
        Returns:
            List of matching projects
        """
        return self.repository.search_by_name(name, skip, limit)
