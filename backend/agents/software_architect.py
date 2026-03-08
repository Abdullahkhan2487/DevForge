"""Software Architect Agent - Designs system architecture."""
from agents.base_agent import BaseAgent, AgentConfig, AgentInput, AgentOutput


class SoftwareArchitectAgent(BaseAgent):
    """Software Architect Agent that designs system architecture."""
    
    def __init__(self):
        config = AgentConfig(
            name="SoftwareArchitectAgent",
            role="Software Architect",
            goal="Design scalable system architecture and database schemas",
            backstory="You are a senior software architect with expertise in microservices, cloud architecture, and database design. You create robust, scalable systems.",
            tools=["diagram_creator", "schema_designer"],
            temperature=0.6
        )
        super().__init__(config)
    
    async def execute(self, agent_input: AgentInput) -> AgentOutput:
        """Execute the architect's task."""
        self.log("Starting architecture design...")
        
        try:
            # Get PRD from previous output
            prd = agent_input.previous_outputs.get("ProductManagerAgent", {}).get("artifacts", {}).get("product_requirements.md", "")
            
            # Create architecture documents
            architecture_doc = await self.create_architecture(agent_input.task, prd)
            database_schema = await self.create_database_schema(agent_input.task, prd)
            api_spec = await self.create_api_spec(agent_input.task, prd)
            
            output_data = {
                "architecture_designed": True,
                "database_tables": database_schema.count("CREATE TABLE"),
                "api_endpoints": api_spec.count("path:"),
                "summary": "System architecture designed"
            }
            
            artifacts = {
                "architecture.md": architecture_doc,
                "database_schema.sql": database_schema,
                "api_spec.yaml": api_spec
            }
            
            self.log("Architecture design completed")
            
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
    
    async def create_architecture(self, product_idea: str, prd: str) -> str:
        """Create architecture document."""
        
        prompt = f"""Based on this product idea and PRD, design a comprehensive system architecture:

Product Idea: {product_idea}

PRD Summary: {prd[:1000]}...

Create an architecture document that includes:

1. **System Overview**
   - High-level architecture diagram description
   - Technology stack decisions and rationale

2. **Architecture Components**
   - Frontend architecture
   - Backend services
   - Database design
   - External integrations
   - Caching strategy

3. **API Design**
   - RESTful API structure
   - Authentication/Authorization
   - Rate limiting

4. **Data Flow**
   - How data moves through the system
   - State management

5. **Scalability Considerations**
   - Horizontal scaling strategy
   - Caching layers
   - CDN usage

6. **Security Architecture**
   - Authentication mechanisms
   - Data encryption
   - API security

7. **Deployment Architecture**
   - Environment setup (dev, staging, prod)
   - CI/CD pipeline
   - Monitoring and logging

Format in clear Markdown with detailed explanations.
"""
        
        return await self.call_llm(prompt, self.get_system_prompt())
    
    async def create_database_schema(self, product_idea: str, prd: str) -> str:
        """Create database schema."""
        
        prompt = f"""Design a complete database schema for: {product_idea}

PRD Context: {prd[:800]}...

Create SQL schema with:
- All necessary tables
- Proper relationships (foreign keys)
- Indexes for performance
- Timestamps (created_at, updated_at)
- Soft deletes where appropriate

Use PostgreSQL syntax.
Include comments explaining each table's purpose.
Follow best practices and normalization principles.
"""
        
        return await self.call_llm(prompt, self.get_system_prompt())
    
    async def create_api_spec(self, product_idea: str, prd: str) -> str:
        """Create OpenAPI specification."""
        
        prompt = f"""Create an OpenAPI 3.0 specification for: {product_idea}

PRD Context: {prd[:800]}...

Include:
- All RESTful endpoints
- Request/response schemas
- Authentication
- Error responses
- Query parameters

Format as valid OpenAPI YAML.
"""
        
        return await self.call_llm(prompt, self.get_system_prompt())
