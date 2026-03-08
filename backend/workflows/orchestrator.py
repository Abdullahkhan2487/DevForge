"""Workflow orchestrator - Manages agent execution pipeline."""
from typing import Dict, Any
from sqlalchemy.orm import Session
from datetime import datetime
import asyncio

from agents import (
    ProductManagerAgent,
    SoftwareArchitectAgent,
    BackendDeveloperAgent,
    FrontendDeveloperAgent,
    QATesterAgent,
    CodeReviewerAgent,
    AgentInput
)
from database import Project, AgentLog
from project_manager.generator import ProjectGenerator


class WorkflowOrchestrator:
    """Orchestrates the execution of multiple agents in sequence."""
    
    def __init__(self, project_id: int, db: Session):
        self.project_id = project_id
        self.db = db
        self.agents = self._initialize_agents()
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
    
    async def execute(self, user_prompt: str):
        """Execute the complete workflow."""
        try:
            # Update project status
            project = self.db.query(Project).filter(Project.id == self.project_id).first()
            project.status = "in_progress"
            self.db.commit()
            
            print(f"\n🚀 Starting workflow for project {self.project_id}")
            print(f"📝 Prompt: {user_prompt}\n")
            
            # Execute agents sequentially
            for agent in self.agents:
                await self._execute_agent(agent, user_prompt)
            
            # Generate project files
            print("\n📦 Generating project files...")
            project_path = await self._generate_project_files(user_prompt)
            
            # Update project with results
            project.status = "completed"
            project.project_path = project_path
            project.project_metadata = {
                "agents_executed": len(self.agents),
                "total_artifacts": sum(len(output.get("artifacts", {})) for output in self.agent_outputs.values())
            }
            self.db.commit()
            
            print(f"\n✅ Project completed successfully!")
            print(f"📁 Project path: {project_path}\n")
            
        except Exception as e:
            print(f"\n❌ Workflow failed: {str(e)}\n")
            
            # Update project status
            project = self.db.query(Project).filter(Project.id == self.project_id).first()
            project.status = "failed"
            self.db.commit()
            
            raise
    
    async def _execute_agent(self, agent, user_prompt: str):
        """Execute a single agent."""
        print(f"🤖 Executing {agent.config.name}...")
        
        # Create agent log
        agent_log = AgentLog(
            project_id=self.project_id,
            agent_name=agent.config.name,
            agent_role=agent.config.role,
            status="in_progress",
            input_data={"prompt": user_prompt}
        )
        self.db.add(agent_log)
        self.db.commit()
        
        start_time = datetime.utcnow()
        
        try:
            # Prepare agent input
            agent_input = AgentInput(
                task=user_prompt,
                previous_outputs=self.agent_outputs
            )
            
            # Execute agent
            output = await agent.execute(agent_input)

            if output.status != "success":
                error_message = output.error or f"{agent.config.name} returned status: {output.status}"
                raise RuntimeError(error_message)
            
            # Store output
            self.agent_outputs[agent.config.name] = {
                "output": output.output,
                "artifacts": output.artifacts
            }
            
            # Update agent log
            agent_log.status = "completed"
            agent_log.output_data = output.output
            agent_log.logs = "\n".join(output.logs)
            agent_log.completed_at = datetime.utcnow()
            
            execution_time = (datetime.utcnow() - start_time).total_seconds()
            print(f"   ✓ Completed in {execution_time:.2f}s")
            print(f"   📄 Generated {len(output.artifacts)} artifacts\n")
            
        except Exception as e:
            agent_log.status = "failed"
            combined_logs = "\n".join(getattr(output, "logs", [])) if "output" in locals() else ""
            if combined_logs:
                agent_log.logs = f"{combined_logs}\nError: {str(e)}"
            else:
                agent_log.logs = f"Error: {str(e)}"
            agent_log.completed_at = datetime.utcnow()
            
            print(f"   ✗ Failed: {str(e)}\n")
            raise
        
        finally:
            self.db.commit()
    
    async def _generate_project_files(self, user_prompt: str) -> str:
        """Generate the complete project structure."""
        generator = ProjectGenerator(self.project_id, user_prompt, self.agent_outputs)
        project_path = await generator.generate()
        return project_path
