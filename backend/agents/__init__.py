"""Agents package - AI agents for software development."""
from agents.base_agent import BaseAgent, AgentConfig, AgentInput, AgentOutput
from agents.product_manager import ProductManagerAgent
from agents.software_architect import SoftwareArchitectAgent
from agents.backend_developer import BackendDeveloperAgent
from agents.frontend_developer import FrontendDeveloperAgent
from agents.qa_tester import QATesterAgent
from agents.code_reviewer import CodeReviewerAgent

__all__ = [
    "BaseAgent",
    "AgentConfig",
    "AgentInput",
    "AgentOutput",
    "ProductManagerAgent",
    "SoftwareArchitectAgent",
    "BackendDeveloperAgent",
    "FrontendDeveloperAgent",
    "QATesterAgent",
    "CodeReviewerAgent"
]
