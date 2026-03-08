# DevForge Setup Guide

## Prerequisites

Before you begin, ensure you have the following installed:

- **Python 3.11+** - [Download here](https://www.python.org/downloads/)
- **Node.js 18+** - [Download here](https://nodejs.org/)
- **Git** - [Download here](https://git-scm.com/)
- **Docker** (Optional) - [Download here](https://www.docker.com/)
- **OpenAI API Key** - [Get one here](https://platform.openai.com/)

## Quick Start

### Method 1: Docker (Recommended)

1. Clone the repository:

```bash
git clone <repository-url>
cd DevForge
```

2. Create environment file:

```bash
cp .env.example .env
```

3. Edit `.env` and add your OpenAI API key:

```
OPENAI_API_KEY=sk-your-actual-key-here
```

4. Start the application:

```bash
docker-compose up --build
```

5. Open your browser:

- Frontend: http://localhost:3000
- API Docs: http://localhost:8000/docs

### Method 2: Manual Setup

#### Backend Setup

1. Navigate to backend directory:

```bash
cd backend
```

2. Create virtual environment:

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Create `.env` file:

```bash
cp .env.example .env
```

5. Edit `.env` with your configuration:

```
OPENAI_API_KEY=sk-your-actual-key-here
DATABASE_URL=sqlite:///./devforge.db
DEBUG=True
```

6. Start the backend server:

```bash
python main.py
# or
uvicorn main:app --reload
```

The backend will start at http://localhost:8000

#### Frontend Setup

1. Open a new terminal and navigate to frontend directory:

```bash
cd frontend
```

2. Install dependencies:

```bash
npm install
```

3. Create `.env.local` file:

```bash
cp .env.local.example .env.local
```

4. Start the development server:

```bash
npm run dev
```

The frontend will start at http://localhost:3000

## Configuration

### Backend Configuration

Edit `backend/.env`:

```bash
# OpenAI Configuration
OPENAI_API_KEY=your_key_here
OPENAI_MODEL=gpt-4-turbo-preview

# Database
DATABASE_URL=sqlite:///./devforge.db

# API Settings
API_HOST=0.0.0.0
API_PORT=8000
DEBUG=True

# Project Generation
PROJECTS_DIR=../generated_projects
```

### Frontend Configuration

Edit `frontend/.env.local`:

```bash
NEXT_PUBLIC_API_URL=http://localhost:8000
```

## Verifying Installation

### Test Backend

1. Visit http://localhost:8000/docs
2. You should see the FastAPI Swagger documentation
3. Try the `/health` endpoint

### Test Frontend

1. Visit http://localhost:3000
2. You should see the DevForge dashboard
3. Try creating a new project

## Troubleshooting

### Backend Issues

**Import errors**:

```bash
# Make sure virtual environment is activated
# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate

# Reinstall dependencies
pip install -r requirements.txt
```

**Database errors**:

```bash
# Delete the database and let it recreate
rm devforge.db
# Restart the backend
```

**OpenAI API errors**:

- Verify your API key is correct in `.env`
- Check you have API credits: https://platform.openai.com/usage
- Ensure the key has permission to use GPT-4

### Frontend Issues

**Module not found**:

```bash
# Clear node_modules and reinstall
rm -rf node_modules package-lock.json
npm install
```

**Build errors**:

```bash
# Clear Next.js cache
rm -rf .next
npm run dev
```

**API connection errors**:

- Verify backend is running at http://localhost:8000
- Check `NEXT_PUBLIC_API_URL` in `.env.local`
- Check browser console for CORS errors

### Docker Issues

**Port already in use**:

```bash
# Stop any existing containers
docker-compose down

# Or change ports in docker-compose.yml
```

**Build fails**:

```bash
# Clean rebuild
docker-compose down -v
docker-compose build --no-cache
docker-compose up
```

## Production Deployment

### Environment Variables

For production, update these settings:

**Backend**:

```bash
DEBUG=False
SECRET_KEY=generate-a-strong-random-key
DATABASE_URL=postgresql://user:pass@host/db  # Use PostgreSQL
```

**Frontend**:

```bash
NEXT_PUBLIC_API_URL=https://your-backend-domain.com
```

### Security Checklist

- [ ] Change `SECRET_KEY` to a strong random value
- [ ] Set `DEBUG=False` in production
- [ ] Use PostgreSQL instead of SQLite
- [ ] Enable HTTPS
- [ ] Set up proper CORS origins
- [ ] Implement rate limiting
- [ ] Set up monitoring and logging
- [ ] Backup database regularly

## Next Steps

1. **Read the Architecture Guide**: `docs/ARCHITECTURE.md`
2. **Learn about Agents**: `docs/AGENTS.md`
3. **API Reference**: `docs/API.md`
4. **Try the Examples**: Create your first project!

## Getting Help

- **Issues**: Open an issue on GitHub
- **Documentation**: Check `docs/` folder
- **API Docs**: http://localhost:8000/docs (when running)

## System Requirements

### Minimum:

- 4GB RAM
- 2 CPU cores
- 10GB disk space

### Recommended:

- 8GB+ RAM
- 4+ CPU cores
- 20GB+ disk space
- Fast internet connection (for OpenAI API)

## Development Tips

### Backend Development

```bash
# Run with auto-reload
uvicorn main:app --reload

# Run tests (when implemented)
pytest

# Format code
black .
```

### Frontend Development

```bash
# Run development server
npm run dev

# Build for production
npm run build
npm start

# Lint code
npm run lint
```

Happy building! 🚀
