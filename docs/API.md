# API Reference

## Base URL

```
http://localhost:8000
```

## Authentication

Currently, no authentication is required. This is for development only.

## Endpoints

### Health Check

#### GET /health

Check if the API is running.

**Response**

```json
{
    "status": "healthy",
    "service": "devforge-api"
}
```

---

### Projects

#### POST /api/projects

Create a new project and start the agent workflow.

**Request Body**

```json
{
    "prompt": "Build an AI SaaS social media scheduling tool",
    "name": "Social Media Scheduler", // optional
    "description": "A tool for scheduling social media posts" // optional
}
```

**Response (201 Created)**

```json
{
    "id": 1,
    "name": "Social Media Scheduler",
    "description": "A tool for scheduling social media posts",
    "prompt": "Build an AI SaaS social media scheduling tool",
    "status": "pending",
    "created_at": "2024-01-15T10:30:00",
    "updated_at": "2024-01-15T10:30:00",
    "project_path": null,
    "metadata": {}
}
```

**Status Values**

- `pending`: Project created, workflow not started
- `in_progress`: Agents are working
- `completed`: All agents finished successfully
- `failed`: Workflow encountered an error

---

#### GET /api/projects

List all projects.

**Query Parameters**

- `skip`: Number of records to skip (default: 0)
- `limit`: Maximum records to return (default: 100)

**Response (200 OK)**

```json
[
    {
        "id": 1,
        "name": "Social Media Scheduler",
        "description": "A tool for scheduling social media posts",
        "prompt": "Build an AI SaaS social media scheduling tool",
        "status": "completed",
        "created_at": "2024-01-15T10:30:00",
        "updated_at": "2024-01-15T10:45:00",
        "project_path": "/path/to/generated/project",
        "metadata": {
            "agents_executed": 6,
            "total_artifacts": 25
        }
    }
]
```

---

#### GET /api/projects/{project_id}

Get details of a specific project.

**Path Parameters**

- `project_id`: The project ID

**Response (200 OK)**

```json
{
    "id": 1,
    "name": "Social Media Scheduler",
    "description": "A tool for scheduling social media posts",
    "prompt": "Build an AI SaaS social media scheduling tool",
    "status": "completed",
    "created_at": "2024-01-15T10:30:00",
    "updated_at": "2024-01-15T10:45:00",
    "project_path": "/path/to/generated/project",
    "metadata": {
        "agents_executed": 6,
        "total_artifacts": 25
    }
}
```

**Response (404 Not Found)**

```json
{
    "detail": "Project not found"
}
```

---

#### GET /api/projects/{project_id}/files

Get all files in a generated project.

**Path Parameters**

- `project_id`: The project ID

**Response (200 OK)**

```json
{
    "files": [
        {
            "path": "backend/main.py",
            "content": "from fastapi import FastAPI...",
            "size": 1024
        },
        {
            "path": "frontend/package.json",
            "content": "{\"name\": \"frontend\", ...}",
            "size": 512
        },
        {
            "path": "docs/architecture.md",
            "content": "# Architecture\n\n...",
            "size": 2048
        }
    ]
}
```

---

#### DELETE /api/projects/{project_id}

Delete a project and its generated files.

**Path Parameters**

- `project_id`: The project ID

**Response (200 OK)**

```json
{
    "message": "Project deleted successfully"
}
```

---

### Agents

#### GET /api/agents/logs

Get agent activity logs.

**Query Parameters**

- `project_id`: Filter by project ID (optional)
- `agent_name`: Filter by agent name (optional)
- `skip`: Number of records to skip (default: 0)
- `limit`: Maximum records to return (default: 100)

**Response (200 OK)**

```json
[
    {
        "id": 1,
        "project_id": 1,
        "agent_name": "ProductManagerAgent",
        "agent_role": "Product Manager",
        "status": "completed",
        "input_data": {
            "prompt": "Build an AI SaaS social media scheduling tool"
        },
        "output_data": {
            "product_name": "Social Media Scheduler",
            "prd_created": true,
            "features_count": 8,
            "summary": "PRD created successfully"
        },
        "logs": "[2024-01-15 10:30:00] Starting product analysis...\n[2024-01-15 10:30:15] PRD created successfully",
        "created_at": "2024-01-15T10:30:00",
        "completed_at": "2024-01-15T10:30:15"
    }
]
```

---

#### GET /api/agents/status

Get status of all available agents.

**Response (200 OK)**

```json
{
    "agents": [
        {
            "name": "ProductManagerAgent",
            "role": "Product Manager",
            "status": "available",
            "description": "Analyzes product ideas and creates PRD"
        },
        {
            "name": "SoftwareArchitectAgent",
            "role": "Software Architect",
            "status": "available",
            "description": "Designs system architecture and database schema"
        },
        {
            "name": "BackendDeveloperAgent",
            "role": "Backend Developer",
            "status": "available",
            "description": "Generates backend APIs and services"
        },
        {
            "name": "FrontendDeveloperAgent",
            "role": "Frontend Developer",
            "status": "available",
            "description": "Builds responsive frontend UI"
        },
        {
            "name": "QATesterAgent",
            "role": "QA Tester",
            "status": "available",
            "description": "Generates comprehensive tests"
        },
        {
            "name": "CodeReviewerAgent",
            "role": "Code Reviewer",
            "status": "available",
            "description": "Reviews and optimizes code"
        }
    ],
    "total": 6
}
```

---

## Error Responses

All endpoints may return the following error responses:

### 400 Bad Request

```json
{
    "detail": "Invalid request data"
}
```

### 404 Not Found

```json
{
    "detail": "Resource not found"
}
```

### 500 Internal Server Error

```json
{
    "detail": "Internal server error"
}
```

---

## Rate Limiting

Currently, no rate limiting is implemented. For production, consider:

- 100 requests per minute per IP
- 10 project creations per hour per user

---

## Webhooks (Future Feature)

Subscribe to project events:

```json
{
    "event": "project.completed",
    "project_id": 1,
    "timestamp": "2024-01-15T10:45:00",
    "data": {
        "status": "completed",
        "project_path": "/path/to/project"
    }
}
```

---

## Example Usage

### Create a Project with Python

```python
import requests

response = requests.post(
    "http://localhost:8000/api/projects",
    json={
        "prompt": "Build an AI-powered task management app",
        "name": "TaskMaster AI"
    }
)

project = response.json()
print(f"Project created with ID: {project['id']}")
```

### Create a Project with JavaScript

```javascript
const response = await fetch('http://localhost:8000/api/projects', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
        prompt: 'Build an AI-powered task management app',
        name: 'TaskMaster AI',
    }),
});

const project = await response.json();
console.log(`Project created with ID: ${project.id}`);
```

### Poll for Project Completion

```javascript
async function waitForCompletion(projectId) {
    while (true) {
        const response = await fetch(`http://localhost:8000/api/projects/${projectId}`);
        const project = await response.json();

        if (project.status === 'completed') {
            console.log('Project completed!');
            return project;
        } else if (project.status === 'failed') {
            console.error('Project failed');
            return null;
        }

        // Wait 5 seconds before checking again
        await new Promise((resolve) => setTimeout(resolve, 5000));
    }
}
```

---

## OpenAPI/Swagger Documentation

When the backend is running, visit:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

These provide interactive API documentation where you can test endpoints directly.
