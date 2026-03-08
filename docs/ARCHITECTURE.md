# DevForge Architecture

## System Overview

DevForge is a multi-agent AI system that autonomously builds complete SaaS applications from natural language descriptions. The system consists of a Python FastAPI backend orchestrating AI agents and a Next.js frontend for user interaction.

## High-Level Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                         Frontend                             │
│                   (Next.js 14 + React)                       │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐   │
│  │Dashboard │  │ Projects │  │  Agents  │  │   Logs   │   │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘   │
└─────────────────────┬───────────────────────────────────────┘
                      │ REST API
┌─────────────────────▼───────────────────────────────────────┐
│                    FastAPI Backend                           │
│  ┌────────────────────────────────────────────────────────┐ │
│  │              API Layer (routes)                         │ │
│  │  /projects  /agents  /health                           │ │
│  └────────────────────┬───────────────────────────────────┘ │
│  ┌────────────────────▼───────────────────────────────────┐ │
│  │         Workflow Orchestrator                           │ │
│  │  Manages agent execution pipeline                       │ │
│  └────────────────────┬───────────────────────────────────┘ │
│  ┌────────────────────▼───────────────────────────────────┐ │
│  │                AI Agents                                │ │
│  │  ┌─────────┐ ┌──────────┐ ┌─────────┐                 │ │
│  │  │   PM    │→│Architect │→│Backend  │                 │ │
│  │  └─────────┘ └──────────┘ └────┬────┘                 │ │
│  │  ┌─────────┐ ┌──────────┐ ┌────▼────┐                 │ │
│  │  │Reviewer │←│   QA     │←│Frontend │                 │ │
│  │  └─────────┘ └──────────┘ └─────────┘                 │ │
│  └────────────────────┬───────────────────────────────────┘ │
│  ┌────────────────────▼───────────────────────────────────┐ │
│  │         Project Generator                               │ │
│  │  Creates file structure from agent outputs              │ │
│  └────────────────────┬───────────────────────────────────┘ │
│  ┌────────────────────▼───────────────────────────────────┐ │
│  │    Database (SQLite/PostgreSQL)                         │ │
│  │  Projects | Agent Logs                                  │ │
│  └─────────────────────────────────────────────────────────┘ │
└─────────────────────┬───────────────────────────────────────┘
                      │
┌─────────────────────▼───────────────────────────────────────┐
│                  OpenAI API                                  │
│                (GPT-4 Turbo)                                 │
└──────────────────────────────────────────────────────────────┘
```

## Backend Architecture

### Core Components

#### 1. API Layer (`api/`)

- **Purpose**: Handle HTTP requests and responses
- **Components**:
    - `projects.py`: Project CRUD operations
    - `agents.py`: Agent status and logs
    - `health.py`: Health checks

#### 2. Agents (`agents/`)

- **Purpose**: AI agents that perform specialized tasks
- **Base Agent**: Abstract class defining agent interface
- **Specialized Agents**:
    - `ProductManagerAgent`: Creates PRD
    - `SoftwareArchitectAgent`: Designs architecture
    - `BackendDeveloperAgent`: Generates backend code
    - `FrontendDeveloperAgent`: Generates frontend code
    - `QATesterAgent`: Generates tests
    - `CodeReviewerAgent`: Reviews code

#### 3. Workflow Orchestrator (`workflows/`)

- **Purpose**: Manages sequential agent execution
- **Responsibilities**:
    - Initialize agents
    - Execute in order
    - Pass outputs between agents
    - Handle errors
    - Update project status

#### 4. Project Manager (`project_manager/`)

- **Purpose**: Generate project files from agent outputs
- **Responsibilities**:
    - Create directory structure
    - Write all generated files
    - Generate meta files (README, Docker, .gitignore)

#### 5. Database (`database.py`)

- **Models**:
    - `Project`: Stores project information
    - `AgentLog`: Stores agent execution logs

### Data Flow

1. **User submits prompt** → Frontend
2. **Frontend calls API** → `POST /api/projects`
3. **API creates project record** → Database
4. **Workflow starts in background** → WorkflowOrchestrator
5. **Agents execute sequentially**:
    - Each agent receives previous outputs
    - Each agent calls OpenAI API
    - Each agent produces artifacts
6. **Project generator creates files** → `generated_projects/`
7. **Frontend polls for updates** → `GET /api/projects/{id}`

## Frontend Architecture

### Technology Stack

- **Framework**: Next.js 14 (App Router)
- **Language**: TypeScript
- **Styling**: Tailwind CSS
- **HTTP Client**: Axios
- **Icons**: Lucide React

### Pages

```
app/
├── layout.tsx          # Root layout with navbar
├── page.tsx            # Dashboard/home page
├── projects/
│   ├── page.tsx        # All projects list
│   └── [id]/
│       └── page.tsx    # Project detail view
├── agents/
│   └── page.tsx        # Agents overview
└── logs/
    └── page.tsx        # Activity logs
```

### Components

```
components/
├── Navbar.tsx                  # Navigation bar
├── CreateProjectDialog.tsx     # Project creation modal
└── ProjectCard.tsx             # Project display card
```

### State Management

- **Local State**: React useState for component state
- **Data Fetching**: Direct API calls with axios
- **Real-time Updates**: Polling every 5 seconds for in-progress projects

## Agent System

### Agent Lifecycle

```
┌─────────────────────────────────────────────────┐
│                Agent Execution                   │
│                                                  │
│  1. Initialize Agent                             │
│     - Load configuration                         │
│     - Prepare tools                              │
│                                                  │
│  2. Receive Input                                │
│     - Task description                           │
│     - Previous agent outputs                     │
│     - Context data                               │
│                                                  │
│  3. Process with LLM                             │
│     - Build system prompt                        │
│     - Build user prompt with context             │
│     - Call OpenAI API                            │
│     - Parse response                             │
│                                                  │
│  4. Generate Artifacts                           │
│     - Create output files                        │
│     - Format code/documentation                  │
│     - Validate output                            │
│                                                  │
│  5. Return Output                                │
│     - Status                                     │
│     - Artifacts (files)                          │
│     - Metadata                                   │
│     - Logs                                       │
└─────────────────────────────────────────────────┘
```

### Agent Pipeline

```
User Prompt
    ↓
[Product Manager Agent]
    - Analyzes prompt
    - Creates PRD with features, user stories
    - Output: product_requirements.md
    ↓
[Software Architect Agent]
    - Reads PRD
    - Designs system architecture
    - Creates database schema
    - Defines APIs
    - Output: architecture.md, database_schema.sql, api_spec.yaml
    ↓
[Backend Developer Agent]
    - Reads architecture
    - Generates FastAPI code
    - Creates models, routes, schemas
    - Output: backend/*.py, requirements.txt
    ↓
[Frontend Developer Agent]
    - Reads backend spec
    - Generates Next.js code
    - Creates components and pages
    - Output: frontend/*.tsx, package.json
    ↓
[QA Tester Agent]
    - Reads all code
    - Generates unit tests
    - Generates integration tests
    - Output: tests/*.py, tests/*.tsx
    ↓
[Code Reviewer Agent]
    - Reviews all generated code
    - Identifies issues
    - Suggests improvements
    - Output: code_review_report.md
    ↓
Complete Project
```

## Database Schema

### Projects Table

```sql
CREATE TABLE projects (
    id INTEGER PRIMARY KEY,
    name VARCHAR,
    description TEXT,
    prompt TEXT,
    status VARCHAR,  -- pending, in_progress, completed, failed
    created_at DATETIME,
    updated_at DATETIME,
    project_path VARCHAR,
    metadata JSON
);
```

### Agent Logs Table

```sql
CREATE TABLE agent_logs (
    id INTEGER PRIMARY KEY,
    project_id INTEGER,
    agent_name VARCHAR,
    agent_role VARCHAR,
    status VARCHAR,
    input_data JSON,
    output_data JSON,
    logs TEXT,
    created_at DATETIME,
    completed_at DATETIME
);
```

## API Endpoints

### Projects

- `POST /api/projects` - Create new project
- `GET /api/projects` - List all projects
- `GET /api/projects/{id}` - Get project details
- `GET /api/projects/{id}/files` - Get project files
- `DELETE /api/projects/{id}` - Delete project

### Agents

- `GET /api/agents/logs` - Get agent activity logs
- `GET /api/agents/status` - Get agent availability

### Health

- `GET /health` - Health check

## Security Considerations

### Current Implementation

- CORS enabled for localhost
- No authentication (for development)
- API keys in environment variables

### Production Requirements

- Add authentication (JWT tokens)
- Implement rate limiting
- Add input validation
- Sanitize outputs
- Use HTTPS
- Implement proper CORS
- Add API key rotation
- Set up monitoring

## Scalability

### Current Limitations

- Sequential agent execution (not parallel)
- SQLite database (single file)
- No caching
- No queue system

### Future Improvements

- Parallel agent execution where possible
- PostgreSQL for production
- Redis for caching and sessions
- Celery for background tasks
- Load balancing
- Horizontal scaling

## Deployment Architecture

```
┌──────────────────────────────────────────────┐
│              Load Balancer                    │
└──────────┬───────────────────────────────────┘
           │
    ┌──────┴──────┐
    │             │
┌───▼───┐    ┌───▼───┐
│Frontend│    │Frontend│
│  (3000)│    │  (3000)│
└───┬───┘    └───┬───┘
    │            │
    └──────┬─────┘
           │
    ┌──────▼──────┐
    │   Backend   │
    │    (8000)   │
    └──────┬──────┘
           │
    ┌──────▼──────┐
    │  Database   │
    │ (PostgreSQL)│
    └─────────────┘
```

## Performance Considerations

### Bottlenecks

1. **OpenAI API calls**: 10-30 seconds per agent
2. **Sequential execution**: Total time = sum of all agents
3. **File generation**: I/O operations

### Optimizations

1. **Caching**: Cache similar prompts
2. **Streaming**: Stream agent outputs
3. **Parallel execution**: Run independent agents in parallel
4. **Database indexing**: Index frequently queried fields
5. **CDN**: Serve frontend assets via CDN

## Monitoring and Logging

### Metrics to Track

- Project creation rate
- Agent execution time
- Success/failure rates
- API response times
- OpenAI API costs

### Logging Strategy

- Agent execution logs in database
- Application logs to file
- Error tracking (Sentry)
- Performance monitoring (New Relic)

## Future Enhancements

1. **Multi-model support**: Claude, Llama, etc.
2. **Agent memory**: Persistent context across projects
3. **Custom agents**: User-defined agents
4. **Real-time collaboration**: Multiple users per project
5. **Version control**: Git integration
6. **Deployment**: Auto-deploy to Vercel/AWS
7. **CI/CD**: Automated testing and deployment
8. **Templates**: Pre-built project templates
9. **Plugins**: Extensible agent system
10. **Marketplace**: Share and sell generated projects
