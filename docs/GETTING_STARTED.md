# Getting Started Guide

This guide will help you set up and run the Autonomous AI Software Company (DevForge) on your local machine.

## Prerequisites

Before you begin, ensure you have the following installed:

- **Python 3.11 or higher**
- **Node.js 18 or higher**
- **Git**
- **OpenAI API Key** (required for AI agents)

Optional:

- **Docker** & **Docker Compose** (for containerized deployment)

## Installation

### 1. Clone the Repository

```bash
git clone <repository-url>
cd DevForge
```

### 2. Backend Setup

Navigate to the backend directory:

```bash
cd backend
```

Create a virtual environment:

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Set up environment variables:

```bash
# Copy the example file
copy .env.example .env  # Windows
cp .env.example .env    # macOS/Linux
```

Edit `.env` and add your OpenAI API key:

```
OPENAI_API_KEY=sk-your-api-key-here
OPENAI_MODEL=gpt-4-turbo-preview
DATABASE_URL=sqlite:///./devforge.db
```

### 3. Frontend Setup

Open a new terminal and navigate to the frontend directory:

```bash
cd frontend
```

Install dependencies:

```bash
npm install
```

Set up environment variables:

```bash
# Copy the example file
copy .env.local.example .env.local  # Windows
cp .env.local.example .env.local    # macOS/Linux
```

The default configuration should work:

```
NEXT_PUBLIC_API_URL=http://localhost:8000
```

## Running the Application

### Option 1: Run Locally

#### Start the Backend

In the backend directory with your virtual environment activated:

```bash
python main.py
```

Or using uvicorn directly:

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

The backend API will be available at: http://localhost:8000

API Documentation:

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

#### Start the Frontend

In the frontend directory:

```bash
npm run dev
```

The frontend will be available at: http://localhost:3000

### Option 2: Run with Docker

Make sure Docker and Docker Compose are installed.

Create a `.env` file in the root directory:

```bash
OPENAI_API_KEY=sk-your-api-key-here
```

Build and start the containers:

```bash
docker-compose up --build
```

Services will be available at:

- Frontend: http://localhost:3000
- Backend API: http://localhost:8000

To run in detached mode:

```bash
docker-compose up -d
```

To stop the containers:

```bash
docker-compose down
```

## Using the Application

### Creating Your First Project

1. Open http://localhost:3000 in your browser
2. Click **"Create New Project"**
3. Enter your product idea, for example:
    ```
    Build an AI SaaS social media scheduling tool that helps users
    plan and automate their social media posts across multiple platforms
    like Twitter, LinkedIn, and Facebook.
    ```
4. Click **"Start Building"**
5. Watch the AI agents collaborate to build your application!

### Monitoring Progress

- **Dashboard**: View all projects and system statistics
- **Projects**: Browse and filter all projects
- **Agents**: See available AI agents and their workflow
- **Logs**: Monitor detailed agent activity logs

### Viewing Generated Code

1. Navigate to a completed project
2. Click on the **"Files"** tab
3. Browse through the generated code
4. Click **"Download Project"** to get the complete codebase

## Project Structure

```
DevForge/
├── backend/                 # Python FastAPI backend
│   ├── agents/             # AI agent implementations
│   │   ├── base_agent.py
│   │   ├── product_manager.py
│   │   ├── software_architect.py
│   │   ├── backend_developer.py
│   │   ├── frontend_developer.py
│   │   ├── qa_tester.py
│   │   └── code_reviewer.py
│   ├── api/                # REST API endpoints
│   ├── workflows/          # Orchestration logic
│   ├── project_manager/    # Project generation
│   ├── main.py             # FastAPI application
│   ├── database.py         # Database models
│   └── config.py           # Configuration
├── frontend/               # Next.js frontend
│   ├── app/                # App router pages
│   ├── components/         # React components
│   └── lib/                # Utilities and API client
├── generated_projects/     # Auto-generated projects
└── docs/                   # Documentation
```

## Agent Workflow

The system uses 6 specialized AI agents that work sequentially:

1. **Product Manager Agent** → Creates Product Requirements Document
2. **Software Architect Agent** → Designs system architecture and database schema
3. **Backend Developer Agent** → Generates FastAPI backend code
4. **Frontend Developer Agent** → Creates Next.js frontend
5. **QA Tester Agent** → Generates comprehensive tests
6. **Code Reviewer Agent** → Reviews and optimizes code

## Configuration

### Backend Configuration

Edit `backend/.env`:

```bash
# API Settings
API_HOST=0.0.0.0
API_PORT=8000
DEBUG=True

# OpenAI Settings
OPENAI_API_KEY=your-key-here
OPENAI_MODEL=gpt-4-turbo-preview

# Database
DATABASE_URL=sqlite:///./devforge.db

# Projects Directory
PROJECTS_DIR=../generated_projects
```

### Frontend Configuration

Edit `frontend/.env.local`:

```bash
NEXT_PUBLIC_API_URL=http://localhost:8000
```

## Troubleshooting

### Backend Issues

**Problem**: `ModuleNotFoundError: No module named 'X'`

**Solution**: Make sure your virtual environment is activated and dependencies are installed:

```bash
pip install -r requirements.txt
```

**Problem**: `OpenAI API key not found`

**Solution**: Verify your `.env` file contains a valid `OPENAI_API_KEY`

**Problem**: Database errors

**Solution**: Delete the database file and let it recreate:

```bash
rm devforge.db
```

### Frontend Issues

**Problem**: `Cannot connect to backend`

**Solution**:

1. Verify the backend is running on port 8000
2. Check `NEXT_PUBLIC_API_URL` in `.env.local`
3. Ensure CORS is configured correctly

**Problem**: Module not found errors

**Solution**: Reinstall dependencies:

```bash
rm -rf node_modules package-lock.json
npm install
```

### Docker Issues

**Problem**: Container fails to start

**Solution**: Check logs:

```bash
docker-compose logs backend
docker-compose logs frontend
```

**Problem**: Port already in use

**Solution**: Change ports in `docker-compose.yml` or stop conflicting services

## Development Tips

### Hot Reload

Both backend and frontend support hot reload:

- **Backend**: Changes to Python files automatically reload the server
- **Frontend**: Changes to React components update instantly

### API Documentation

FastAPI provides interactive API documentation:

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

### Database Inspection

To inspect the SQLite database:

```bash
sqlite3 backend/devforge.db
.tables
SELECT * FROM projects;
.quit
```

### Viewing Generated Projects

Generated projects are stored in `generated_projects/`. Each project contains:

- Complete backend code
- Complete frontend code
- Tests
- Documentation
- Docker configuration

## Next Steps

- Explore the generated projects
- Modify agent prompts to customize output
- Add new agents for additional functionality
- Integrate with GitHub for automatic repo creation
- Deploy to production

## Getting Help

- Check the [README.md](../README.md) for overview
- Review API documentation at `/docs`
- Check agent logs for debugging
- Open an issue on GitHub

## Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Next.js Documentation](https://nextjs.org/docs)
- [OpenAI API Documentation](https://platform.openai.com/docs)
- [Tailwind CSS](https://tailwindcss.com/docs)
