# AI Agents Guide

## Overview

DevForge uses 6 specialized AI agents that work together sequentially to build complete applications. Each agent has a specific role and expertise.

## Agent Architecture

```python
class BaseAgent(ABC):
    """Base class for all AI agents."""

    def __init__(self, config: AgentConfig):
        self.config = config  # name, role, goal, backstory
        self.logs = []

    async def execute(self, agent_input: AgentInput) -> AgentOutput:
        """Execute the agent's task."""
        pass

    async def call_llm(self, prompt: str) -> str:
        """Call OpenAI API."""
        pass
```

## The Six Agents

### 1. Product Manager Agent

**Role**: Analyze product ideas and create comprehensive PRDs

**Input**:

- User's product idea/prompt

**Output**:

- `product_requirements.md` - Detailed PRD

**Process**:

1. Analyze the product idea
2. Define problem statement and target users
3. List core features and nice-to-haves
4. Create user stories
5. Define success metrics

**Example Output Structure**:

```markdown
# Product Requirements Document

## Executive Summary

- Product vision
- Problem statement
- Target audience

## Product Goals

- Primary objectives
- Success metrics (KPIs)

## User Personas

- Primary user types
- Needs and pain points

## Feature Requirements

### Core Features (MVP)

- Feature 1
- Feature 2

### Nice-to-Have Features

- Feature A
- Feature B

## User Stories

- As a [user], I want [goal], so that [benefit]

## Technical Considerations

- Platform requirements
- Integration needs

## Success Criteria

- KPIs and metrics
```

---

### 2. Software Architect Agent

**Role**: Design scalable system architecture

**Input**:

- Product idea
- PRD from Product Manager

**Output**:

- `architecture.md` - System architecture document
- `database_schema.sql` - Complete database schema
- `api_spec.yaml` - OpenAPI specification

**Process**:

1. Read and understand PRD
2. Design system architecture
3. Create database schema
4. Define API endpoints
5. Plan scalability strategy

**Example Database Schema**:

```sql
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE posts (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    content TEXT NOT NULL,
    scheduled_time TIMESTAMP,
    status VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

---

### 3. Backend Developer Agent

**Role**: Generate production-ready backend code

**Input**:

- Product idea
- Architecture documents
- Database schema
- API specification

**Output**:

- `backend/main.py` - FastAPI application
- `backend/models.py` - SQLAlchemy models
- `backend/routes.py` - API endpoints
- `backend/schemas.py` - Pydantic schemas
- `backend/requirements.txt` - Dependencies
- `backend/.env.example` - Environment template

**Process**:

1. Generate FastAPI application structure
2. Create database models based on schema
3. Implement API endpoints
4. Add request/response validation
5. Include error handling

**Example Output** (`main.py`):

```python
from fastapi import FastAPI
from routes import router

app = FastAPI(title="Generated App")
app.include_router(router)

@app.get("/")
async def root():
    return {"message": "Welcome to the API"}
```

---

### 4. Frontend Developer Agent

**Role**: Build responsive frontend UI

**Input**:

- Product idea
- Backend API specification
- Architecture documents

**Output**:

- `frontend/app/page.tsx` - Main page
- `frontend/app/layout.tsx` - Layout
- `frontend/components/*.tsx` - React components
- `frontend/lib/api.ts` - API client
- `frontend/package.json` - Dependencies
- `frontend/tailwind.config.js` - Styling config

**Process**:

1. Design component structure
2. Create main pages
3. Build reusable components
4. Implement API integration
5. Add responsive styling

**Example Component**:

```tsx
'use client';

export default function Dashboard() {
    const [data, setData] = useState([]);

    useEffect(() => {
        fetchData();
    }, []);

    return (
        <div className="container mx-auto">
            <h1>Dashboard</h1>
            {/* Component content */}
        </div>
    );
}
```

---

### 5. QA Tester Agent

**Role**: Generate comprehensive tests

**Input**:

- Product idea
- Backend code
- Frontend code
- Architecture

**Output**:

- `tests/backend/test_models.py` - Model tests
- `tests/backend/test_api.py` - API tests
- `tests/frontend/components.test.tsx` - Component tests
- `tests/e2e/user_flow.spec.ts` - E2E tests
- `tests/pytest.ini` - Pytest config
- `tests/jest.config.js` - Jest config

**Process**:

1. Analyze backend code
2. Generate unit tests for models
3. Generate API integration tests
4. Create frontend component tests
5. Write E2E test scenarios

**Example Test**:

```python
import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_create_user():
    response = client.post(
        "/users",
        json={"email": "test@example.com", "password": "secret123"}
    )
    assert response.status_code == 201
    assert "id" in response.json()
```

---

### 6. Code Reviewer Agent

**Role**: Review and optimize generated code

**Input**:

- All generated code
- Architecture
- Tests

**Output**:

- `code_review_report.md` - Comprehensive review
- `improvement_suggestions.md` - Actionable suggestions

**Process**:

1. Analyze all generated code
2. Check for best practices
3. Identify security issues
4. Find performance bottlenecks
5. Suggest improvements

**Example Review Report**:

```markdown
# Code Review Report

## Executive Summary

Overall Quality: 8/10

## Backend Review

### ✅ Strengths

- Clean code structure
- Proper error handling
- Good type hints

### ❌ Issues Found

- Missing input validation on endpoint X
- No rate limiting implemented

### 💡 Suggestions

- Add request validation middleware
- Implement caching for expensive queries

## Security Review

- Missing CORS configuration
- Need to add rate limiting
- Consider adding API key authentication
```

---

## Agent Configuration

Each agent is configured with:

```python
AgentConfig(
    name="BackendDeveloperAgent",
    role="Backend Developer",
    goal="Generate production-ready backend code",
    backstory="You are a senior backend developer...",
    tools=["code_generator", "file_writer"],
    llm_model="gpt-4-turbo-preview",
    temperature=0.5,  # Lower = more deterministic
    max_tokens=4000
)
```

## Agent Communication

Agents communicate through structured outputs:

```python
class AgentOutput(BaseModel):
    agent_name: str
    status: str  # success, failed, partial
    output: Dict[str, Any]  # Structured data
    artifacts: Dict[str, str]  # filename -> content
    logs: List[str]  # Execution logs
    error: Optional[str] = None
```

## Execution Pipeline

```python
# Workflow Orchestrator
async def execute(self, user_prompt: str):
    for agent in self.agents:
        # Prepare input with previous outputs
        agent_input = AgentInput(
            task=user_prompt,
            previous_outputs=self.agent_outputs
        )

        # Execute agent
        output = await agent.execute(agent_input)

        # Store output for next agent
        self.agent_outputs[agent.config.name] = output
```

## Customizing Agents

### Modify Agent Behavior

Edit the agent's system prompt:

```python
def get_system_prompt(self) -> str:
    return f"""You are a {self.config.role}.

Your goal: {self.config.goal}

Additional instructions:
- Use modern best practices
- Write clean, documented code
- Consider scalability
"""
```

### Add New Tools

```python
class CustomAgent(BaseAgent):
    async def execute(self, agent_input: AgentInput):
        # Use custom tools
        result = await self.custom_tool(agent_input.task)

        return self.create_output(
            status="success",
            output={"result": result},
            artifacts={"output.txt": result}
        )

    async def custom_tool(self, task: str):
        # Custom tool implementation
        pass
```

### Change Execution Order

Modify the orchestrator:

```python
def _initialize_agents(self):
    return [
        ProductManagerAgent(),
        SoftwareArchitectAgent(),
        # Add your custom agent here
        CustomAgent(),
        BackendDeveloperAgent(),
        # ... rest of agents
    ]
```

## Agent Best Practices

### 1. Keep Prompts Clear

- Be specific about requirements
- Provide examples when possible
- Set clear expectations

### 2. Handle Errors Gracefully

```python
try:
    result = await agent.execute(input_data)
except Exception as e:
    log_error(e)
    # Decide: retry, skip, or fail
```

### 3. Validate Outputs

```python
def validate_output(self, output: AgentOutput) -> bool:
    # Check if required artifacts are present
    required = ["main.py", "models.py"]
    return all(f in output.artifacts for f in required)
```

### 4. Log Everything

```python
self.log("Starting code generation...")
self.log(f"Generated {len(files)} files")
self.log("Code generation completed")
```

## Monitoring Agent Performance

Track these metrics:

```python
{
    "agent_name": "BackendDeveloperAgent",
    "execution_time": 25.3,  # seconds
    "tokens_used": 3500,
    "artifacts_generated": 6,
    "status": "success"
}
```

## Future Enhancements

1. **Parallel Execution**: Run independent agents in parallel
2. **Agent Memory**: Agents remember past projects
3. **Custom Agents**: Users can define their own agents
4. **Agent Marketplace**: Share and download community agents
5. **Multi-Model Support**: Use different LLMs per agent
6. **Feedback Loop**: Agents can request clarification
7. **Incremental Output**: Stream results as they're generated
8. **Agent Collaboration**: Agents can talk to each other
9. **Version Control**: Track agent output versions
10. **A/B Testing**: Compare different agent configurations

## Troubleshooting

### Agent Times Out

- Increase `max_tokens`
- Simplify the prompt
- Break task into smaller steps

### Poor Quality Output

- Lower `temperature` for more consistent results
- Provide more context in prompt
- Add examples to system prompt

### Agent Fails

- Check OpenAI API key
- Verify API rate limits
- Review error logs
- Ensure previous outputs are valid

## Example: Adding a New Agent

```python
# 1. Create agent class
class DevOpsAgent(BaseAgent):
    def __init__(self):
        config = AgentConfig(
            name="DevOpsAgent",
            role="DevOps Engineer",
            goal="Create deployment configurations",
            backstory="Expert in CI/CD and infrastructure",
            temperature=0.4
        )
        super().__init__(config)

    async def execute(self, agent_input: AgentInput):
        # Generate CI/CD configs
        github_actions = await self.generate_github_actions()
        dockerfile = await self.generate_dockerfile()

        return self.create_output(
            status="success",
            output={"ci_cd_configured": True},
            artifacts={
                ".github/workflows/ci.yml": github_actions,
                "Dockerfile": dockerfile
            }
        )

# 2. Add to orchestrator
def _initialize_agents(self):
    return [
        ProductManagerAgent(),
        SoftwareArchitectAgent(),
        BackendDeveloperAgent(),
        FrontendDeveloperAgent(),
        QATesterAgent(),
        DevOpsAgent(),  # Your new agent
        CodeReviewerAgent()
    ]
```
