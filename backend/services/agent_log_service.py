"""Agent log service for business logic."""
from typing import List, Optional
from sqlalchemy.orm import Session

from repositories import AgentLogRepository
from database import AgentLog
from core.logging import get_logger

logger = get_logger(__name__)


class AgentLogService:
    """Service for agent log-related business logic."""
    
    def __init__(self, db: Session):
        """
        Initialize service.
        
        Args:
            db: Database session
        """
        self.db = db
        self.repository = AgentLogRepository(db)
    
    def get_logs(
        self,
        project_id: Optional[int] = None,
        agent_name: Optional[str] = None,
        skip: int = 0,
        limit: int = 100
    ) -> List[AgentLog]:
        """
        Get agent logs with optional filtering.
        
        Args:
            project_id: Optional project ID filter
            agent_name: Optional agent name filter
            skip: Number of records to skip
            limit: Maximum number of records
        
        Returns:
            List of agent logs
        """
        if project_id:
            return self.repository.get_by_project(project_id, skip, limit)
        elif agent_name:
            return self.repository.get_by_agent_name(agent_name, skip, limit)
        else:
            return self.repository.get_all(skip, limit)
    
    def get_project_logs(self, project_id: int, limit: int = 10) -> List[AgentLog]:
        """
        Get recent logs for a specific project.
        
        Args:
            project_id: Project ID
            limit: Maximum number of records
        
        Returns:
            List of agent logs
        """
        return self.repository.get_recent_for_project(project_id, limit)
    
    def get_failed_logs(self, skip: int = 0, limit: int = 100) -> List[AgentLog]:
        """
        Get failed agent executions.
        
        Args:
            skip: Number of records to skip
            limit: Maximum number of records
        
        Returns:
            List of failed agent logs
        """
        return self.repository.get_failed_logs(skip, limit)
