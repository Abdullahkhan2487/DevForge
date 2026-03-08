"""Project repository."""
from typing import List, Optional
from sqlalchemy import desc
from sqlalchemy.orm import Session
from repositories.base import BaseRepository
from database import Project
from core.constants import ProjectStatus
from core.logging import get_logger

logger = get_logger(__name__)


class ProjectRepository(BaseRepository[Project]):
    """Repository for Project model."""
    
    def __init__(self, db: Session):
        super().__init__(Project, db)
    
    def get_by_status(
        self,
        status: ProjectStatus,
        skip: int = 0,
        limit: int = 100
    ) -> List[Project]:
        """
        Get projects by status.
        
        Args:
            status: Project status
            skip: Number of records to skip
            limit: Maximum number of records to return
        
        Returns:
            List of projects
        """
        return self.get_all(skip=skip, limit=limit, filters={"status": status.value})
    
    def get_recent(self, limit: int = 10) -> List[Project]:
        """
        Get recent projects ordered by creation date.
        
        Args:
            limit: Maximum number of records to return
        
        Returns:
            List of recent projects
        """
        return (
            self.db.query(self.model)
            .order_by(desc(self.model.created_at))
            .limit(limit)
            .all()
        )
    
    def update_status(self, id: int, status: ProjectStatus) -> Project:
        """
        Update project status.
        
        Args:
            id: Project ID
            status: New status
        
        Returns:
            Updated project
        """
        return self.update(id, status=status.value)
    
    def search_by_name(self, name: str, skip: int = 0, limit: int = 100) -> List[Project]:
        """
        Search projects by name (case-insensitive).
        
        Args:
            name: Name to search for
            skip: Number of records to skip
            limit: Maximum number of records to return
        
        Returns:
            List of matching projects
        """
        return (
            self.db.query(self.model)
            .filter(self.model.name.ilike(f"%{name}%"))
            .offset(skip)
            .limit(limit)
            .all()
        )
