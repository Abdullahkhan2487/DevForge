"""Agent log repository."""
from typing import List, Optional
from sqlalchemy import desc
from sqlalchemy.orm import Session
from repositories.base import BaseRepository
from database import AgentLog
from core.constants import AgentStatus
from core.logging import get_logger

logger = get_logger(__name__)


class AgentLogRepository(BaseRepository[AgentLog]):
    """Repository for AgentLog model."""
    
    def __init__(self, db: Session):
        super().__init__(AgentLog, db)
    
    def get_by_project(
        self,
        project_id: int,
        skip: int = 0,
        limit: int = 100
    ) -> List[AgentLog]:
        """
        Get logs for a specific project.
        
        Args:
            project_id: Project ID
            skip: Number of records to skip
            limit: Maximum number of records to return
        
        Returns:
            List of agent logs
        """
        return self.get_all(
            skip=skip,
            limit=limit,
            filters={"project_id": project_id}
        )
    
    def get_by_agent_name(
        self,
        agent_name: str,
        skip: int = 0,
        limit: int = 100
    ) -> List[AgentLog]:
        """
        Get logs for a specific agent.
        
        Args:
            agent_name: Agent name
            skip: Number of records to skip
            limit: Maximum number of records to return
        
        Returns:
            List of agent logs
        """
        return self.get_all(
            skip=skip,
            limit=limit,
            filters={"agent_name": agent_name}
        )
    
    def get_failed_logs(self, skip: int = 0, limit: int = 100) -> List[AgentLog]:
        """
        Get failed agent executions.
        
        Args:
            skip: Number of records to skip
            limit: Maximum number of records to return
        
        Returns:
            List of failed agent logs
        """
        return self.get_all(
            skip=skip,
            limit=limit,
            filters={"status": AgentStatus.FAILED.value}
        )
    
    def get_recent_for_project(self, project_id: int, limit: int = 10) -> List[AgentLog]:
        """
        Get recent logs for a project.
        
        Args:
            project_id: Project ID
            limit: Maximum number of records to return
        
        Returns:
            List of recent agent logs
        """
        return (
            self.db.query(self.model)
            .filter(self.model.project_id == project_id)
            .order_by(desc(self.model.created_at))
            .limit(limit)
            .all()
        )
