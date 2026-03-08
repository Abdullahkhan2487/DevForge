# Autonomous AI Software Company

A production-grade system that simulates a complete software company run by AI agents. Each agent performs a specialized role in the software development lifecycle.

## Overview

This platform accepts a product idea from a user and automatically generates a complete SaaS application including planning, architecture, backend, frontend, tests, and documentation.

## Features

- **Multi-Agent System**: Product Manager, Software Architect, Backend Developer, Frontend Developer, QA Tester, and Code Reviewer agents
- **Automated Code Generation**: Full-stack application generation from a single prompt
- **Real-time Monitoring**: Watch agents collaborate in real-time
- **Project Dashboard**: Manage and view all generated projects
- **Production-Ready Code**: Generated code follows best practices and industry standards

## Technology Stack

### Backend

- Python 3.11+
- FastAPI
- LightAgent framework
- OpenAI API
- SQLite/PostgreSQL
- Redis (optional)

### Frontend

- Next.js 14
- TypeScript
- Tailwind CSS
- Shadcn UI

### Infrastructure

- Docker
- Git

## Project Structure

```
autonomous-ai-company/
├── backend/                 # Python FastAPI backend
│   ├── agents/             # AI agent implementations
│   ├── workflows/          # Orchestration logic
│   ├── memory/             # Shared memory system
│   ├── tools/              # Agent tools
│   ├── project_manager/    # Project generation
│   └── api/                # REST API endpoints
├── frontend/               # Next.js frontend
│   ├── app/                # App router pages
│   ├── components/         # React components
│   └── lib/                # Utilities
├── generated_projects/     # Auto-generated projects
└── docs/                   # Documentation
```

## Getting Started

### Prerequisites

- Python 3.11+
- Node.js 18+
- Docker (optional)

### Installation

1. Clone the repository:

```bash
git clone <repository-url>
cd DevForge
```

2. Setup backend:

```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

3. Setup frontend:

```bash
cd frontend
npm install
```

4. Configure environment variables:

```bash
# Backend (.env)
OPENAI_API_KEY=your_key_here
DATABASE_URL=sqlite:///./devforge.db

# Frontend (.env.local)
NEXT_PUBLIC_API_URL=http://localhost:8000
```

### Running the Application

1. Start backend:

```bash
cd backend
uvicorn main:app --reload
```

2. Start frontend:

```bash
cd frontend
npm run dev
```

3. Open http://localhost:3000

## Usage

1. Navigate to the dashboard
2. Click "Create New Project"
3. Enter your product idea: "Build an AI SaaS social media scheduling tool"
4. Watch the agents collaborate to build your application
5. Download or deploy the generated project

## Agent Workflow

```
User Prompt
     ↓
Product Manager Agent (creates PRD)
     ↓
Software Architect Agent (designs system)
     ↓
Backend Developer Agent (generates APIs)
     ↓
Frontend Developer Agent (builds UI)
     ↓
QA Tester Agent (writes tests)
     ↓
Code Reviewer Agent (reviews & optimizes)
     ↓
Complete Project
```

## API Endpoints

- `POST /api/create-project` - Start agent workflow
- `GET /api/project/{id}` - Get project details
- `GET /api/projects` - List all projects
- `GET /api/agents/logs` - Get agent activity logs
- `GET /api/project/{id}/files` - Get project files

## Contributing

Contributions are welcome! Please read our contributing guidelines.

## License

MIT License

## Support

For issues and questions, please open a GitHub issue.
