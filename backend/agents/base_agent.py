"""Base agent class and framework."""
from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional
from pydantic import BaseModel
import json
from datetime import datetime


class AgentConfig(BaseModel):
    """Configuration for an agent."""
    name: str
    role: str
    goal: str
    backstory: str
    tools: List[str] = []
    llm_model: str = "llama-3.3-70b-versatile"
    temperature: float = 0.7
    max_tokens: int = 4000


class AgentInput(BaseModel):
    """Input schema for agent execution."""
    task: str
    context: Dict[str, Any] = {}
    previous_outputs: Dict[str, Any] = {}


class AgentOutput(BaseModel):
    """Output schema for agent execution."""
    agent_name: str
    status: str  # success, failed, partial
    output: Dict[str, Any]
    artifacts: Dict[str, str] = {}  # filename -> content
    logs: List[str] = []
    error: Optional[str] = None
    execution_time: float = 0.0


class BaseAgent(ABC):
    """Base class for all AI agents."""
    
    def __init__(self, config: AgentConfig):
        from config import settings
        # Use Groq model from settings if not specified
        if not config.llm_model or config.llm_model == "llama-3.3-70b-versatile":
            config.llm_model = settings.groq_model
        self.config = config
        self.logs: List[str] = []
        
    def log(self, message: str):
        """Add a log message."""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] [{self.config.name}] {message}"
        self.logs.append(log_entry)
        print(log_entry)
    
    @abstractmethod
    async def execute(self, agent_input: AgentInput) -> AgentOutput:
        """Execute the agent's task."""
        pass
    
    async def call_llm(self, prompt: str, system_prompt: Optional[str] = None) -> str:
        """Call Groq LLM with a prompt."""
        from litellm import acompletion
        from config import settings
        
        # Always use Groq with proper model prefix
        model = self.config.llm_model
        if not model.startswith("groq/"):
            model = f"groq/{model}"
        
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})
        
        self.log(f"Calling Groq with model: {model}")
        
        try:
            response = await acompletion(
                model=model,
                messages=messages,
                temperature=self.config.temperature,
                max_tokens=self.config.max_tokens
            )
            
            # Return the response content
            if isinstance(response, dict):
                return response["choices"][0]["message"]["content"]
            return response.choices[0].message.content
        except Exception as e:
            self.log(f"Error calling Groq: {str(e)}")
            raise
    
    def create_output(
        self,
        status: str,
        output: Dict[str, Any],
        artifacts: Dict[str, str] = None,
        error: Optional[str] = None
    ) -> AgentOutput:
        """Create an agent output."""
        return AgentOutput(
            agent_name=self.config.name,
            status=status,
            output=output,
            artifacts=artifacts or {},
            logs=self.logs,
            error=error
        )
    
    def get_system_prompt(self) -> str:
        """Get the system prompt for this agent."""
        return f"""You are a {self.config.role}.

Role: {self.config.role}
Goal: {self.config.goal}
Backstory: {self.config.backstory}

You are part of an AI software company that builds complete applications.
Your job is to {self.config.goal}.

Be thorough, professional, and produce production-quality output.
Think step by step and explain your reasoning.
"""
