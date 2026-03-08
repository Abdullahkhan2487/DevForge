"""Workflow service for agent orchestration."""
from typing import Dict, Any
from sqlalchemy.orm import Session

from repositories import ProjectRepository, AgentLogRepository
from core.constants import ProjectStatus, AgentStatus
from core.logging import get_logger
from core.exceptions import WorkflowError
from agents import (
    ProductManagerAgent,
    SoftwareArchitectAgent,
    BackendDeveloperAgent,
    FrontendDeveloperAgent,
    QATesterAgent,
    CodeReviewerAgent,
    AgentInput
)
from project_manager.generator import ProjectGenerator
from datetime import datetime

logger = get_logger(__name__)


class WorkflowService:
    """Service for managing agent workflow execution."""
    
    def __init__(self, db: Session):
        """
        Initialize service.
        
        Args:
            db: Database session
        """
        self.db = db
        self.project_repo = ProjectRepository(db)
        self.agent_log_repo = AgentLogRepository(db)
        self.agent_outputs: Dict[str, Any] = {}
    
    def _initialize_agents(self):
        """Initialize all agents in execution order."""
        return [
            ProductManagerAgent(),
            SoftwareArchitectAgent(),
            BackendDeveloperAgent(),
            FrontendDeveloperAgent(),
            QATesterAgent(),
            CodeReviewerAgent()
        ]
    
    async def execute_workflow(self, project_id: int, prompt: str) -> None:
        """
        Execute the complete agent workflow for a project.
        
        Args:
            project_id: Project ID
            prompt: User prompt/idea
        
        Raises:
            WorkflowError: If workflow execution fails
        """
        try:
            # Update project status
            self.project_repo.update_status(project_id, ProjectStatus.IN_PROGRESS)
            
            logger.info(f"Starting workflow for project {project_id}")
            
            # Initialize agents
            agents = self._initialize_agents()
            
            # Execute agents sequentially
            for agent in agents:
                await self._execute_agent(agent, project_id, prompt)
            
            # Generate project files
            logger.info("Generating project files")
            project_path =await self._generate_project_files(project_id, prompt)
            
            # Update project with results
            self.project_repo.update(
                project_id,
                status=ProjectStatus.COMPLETED.value,
                project_path=project_path,
                project_metadata={
                    "agents_executed": len(agents),
                    "total_artifacts": sum(
                        len(output.get("artifacts", {}))
                        for output in self.agent_outputs.values()
                    ),
                    "completed_at": datetime.utcnow().isoformat()
                }
            )
            
            logger.info(f"Workflow completed successfully for project {project_id}")
            
        except Exception as e:
            logger.error(f"Workflow failed for project {project_id}: {str(e)}")
            self.project_repo.update_status(project_id, ProjectStatus.FAILED)
            raise WorkflowError(f"Workflow execution failed: {str(e)}")
    
    async def _execute_agent(self, agent, project_id: int, prompt: str) -> None:
        """
        Execute a single agent.
        
        Args:
            agent: Agent instance
            project_id: Project ID
            prompt: User prompt
        
        Raises:
            WorkflowError: If agent execution fails
        """
        agent_name = agent.config.name
        logger.info(f"Executing {agent_name}")
        
        # Create agent log
        agent_log = self.agent_log_repo.create(
            project_id=project_id,
            agent_name=agent_name,
            agent_role=agent.config.role,
            status=AgentStatus.IN_PROGRESS.value,
            input_data={"prompt": prompt}
        )
        
        start_time = datetime.utcnow()
        
        try:
            # Prepare agent input
            agent_input = AgentInput(
                task=prompt,
                previous_outputs=self.agent_outputs
            )
            
            # Execute agent
            output = await agent.execute(agent_input)
            
            if output.status != "success":
                error_message = output.error or f"{agent_name} returned status: {output.status}"
                raise WorkflowError(error_message, agent_name)
            
            # Store output
            self.agent_outputs[agent_name] = {
                "output": output.output,
                "artifacts": output.artifacts
            }
            
            # Update agent log
            execution_time = (datetime.utcnow() - start_time).total_seconds()
            self.agent_log_repo.update(
                agent_log.id,
                status=AgentStatus.COMPLETED.value,
                output_data=output.output,
                logs="\n".join(output.logs),
                completed_at=datetime.utcnow()
            )
            
            logger.info(
                f"{agent_name} completed in {execution_time:.2f}s, "
                f"generated {len(output.artifacts)} artifacts"
            )
            
        except Exception as e:
            # Update agent log with failure
            self.agent_log_repo.update(
                agent_log.id,
                status=AgentStatus.FAILED.value,
                logs=f"Error: {str(e)}",
                completed_at=datetime.utcnow()
            )
            
            logger.error(f"{agent_name} failed: {str(e)}")
            raise WorkflowError(f"{agent_name} execution failed: {str(e)}", agent_name)
    
    async def _generate_project_files(self, project_id: int, prompt: str) -> str:
        """
        Generate project files from agent outputs.
        
        Args:
            project_id: Project ID
            prompt: User prompt
        
        Returns:
            Path to generated project directory
        """
        generator = ProjectGenerator(project_id, prompt, self.agent_outputs)
        project_path = await generator.generate()
        logger.info(f"Generated project files at {project_path}")
        return project_path
