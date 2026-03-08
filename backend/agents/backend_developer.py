"""Backend Developer Agent - Generates backend code."""
from agents.base_agent import BaseAgent, AgentConfig, AgentInput, AgentOutput


class BackendDeveloperAgent(BaseAgent):
    """Backend Developer Agent that generates backend code."""
    
    def __init__(self):
        config = AgentConfig(
            name="BackendDeveloperAgent",
            role="Backend Developer",
            goal="Generate production-ready backend APIs and services",
            backstory="You are a senior backend developer expert in Python, FastAPI, and database design. You write clean, efficient, and well-documented code.",
            tools=["code_generator", "file_writer"],
            temperature=0.5
        )
        super().__init__(config)
    
    async def execute(self, agent_input: AgentInput) -> AgentOutput:
        """Execute backend development task."""
        self.log("Starting backend development...")
        
        try:
            # Get previous outputs
            architecture = agent_input.previous_outputs.get("SoftwareArchitectAgent", {})
            arch_artifacts = architecture.get("artifacts", {})
            
            # Generate backend files
            main_py = await self.generate_main_file(agent_input.task, arch_artifacts)
            models_py = await self.generate_models(agent_input.task, arch_artifacts)
            routes_py = await self.generate_routes(agent_input.task, arch_artifacts)
            schemas_py = await self.generate_schemas(agent_input.task, arch_artifacts)
            requirements = await self.generate_requirements()
            
            output_data = {
                "backend_generated": True,
                "files_created": 5,
                "api_endpoints": routes_py.count("@router."),
                "summary": "Backend code generated successfully"
            }
            
            artifacts = {
                "backend/main.py": main_py,
                "backend/models.py": models_py,
                "backend/routes.py": routes_py,
                "backend/schemas.py": schemas_py,
                "backend/requirements.txt": requirements,
                "backend/.env.example": self.generate_env_example()
            }
            
            self.log("Backend development completed")
            
            return self.create_output(
                status="success",
                output=output_data,
                artifacts=artifacts
            )
            
        except Exception as e:
            self.log(f"Error: {str(e)}")
            return self.create_output(
                status="failed",
                output={},
                error=str(e)
            )
    
    async def generate_main_file(self, product_idea: str, architecture: dict) -> str:
        """Generate main FastAPI application file."""
        
        prompt = f"""Generate a production-ready FastAPI main.py file for: {product_idea}

Architecture context:
{architecture.get('architecture.md', '')[:1000]}

The file should include:
- FastAPI app initialization
- CORS middleware
- Database connection
- Router inclusions
- Lifespan events
- Error handling
- Logging configuration

Use modern FastAPI patterns and best practices.
Include proper type hints and docstrings.
"""
        
        return await self.call_llm(prompt, self.get_system_prompt())
    
    async def generate_models(self, product_idea: str, architecture: dict) -> str:
        """Generate SQLAlchemy models."""
        
        db_schema = architecture.get('database_schema.sql', '')
        
        prompt = f"""Generate SQLAlchemy models for: {product_idea}

Database schema:
{db_schema}

Create models.py with:
- All database models
- Proper relationships
- Indexes
- Timestamps
- String representations
- SQLAlchemy 2.0 syntax

Include proper imports and configuration.
"""
        
        return await self.call_llm(prompt, self.get_system_prompt())
    
    async def generate_routes(self, product_idea: str, architecture: dict) -> str:
        """Generate API routes."""
        
        api_spec = architecture.get('api_spec.yaml', '')
        
        prompt = f"""Generate FastAPI routes for: {product_idea}

API Specification:
{api_spec[:1500]}

Create routes.py with:
- RESTful endpoints
- CRUD operations
- Request validation
- Response models
- Error handling
- Database queries
- Proper HTTP status codes

Use APIRouter and follow REST conventions.
"""
        
        return await self.call_llm(prompt, self.get_system_prompt())
    
    async def generate_schemas(self, product_idea: str, architecture: dict) -> str:
        """Generate Pydantic schemas."""
        
        prompt = f"""Generate Pydantic schemas (request/response models) for: {product_idea}

Create schemas.py with:
- Request models
- Response models
- Validation rules
- Field descriptions
- Example values
- Config classes

Use Pydantic v2 syntax.
"""
        
        return await self.call_llm(prompt, self.get_system_prompt())
    
    async def generate_requirements(self) -> str:
        """Generate requirements.txt."""
        return """fastapi==0.109.0
uvicorn[standard]==0.27.0
sqlalchemy==2.0.25
pydantic==2.5.3
pydantic-settings==2.1.0
python-dotenv==1.0.0
python-multipart==0.0.6
python-jose[cryptography]==3.3.0
passlib[bcrypt]==1.7.4
alembic==1.13.1
aiosqlite==0.19.0
httpx==0.26.0
"""
    
    def generate_env_example(self) -> str:
        """Generate .env.example file."""
        return """DATABASE_URL=sqlite:///./app.db
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
"""
