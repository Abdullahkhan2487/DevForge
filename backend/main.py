"""Main FastAPI application entry point."""
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager

from config import settings
from api import projects, agents, health
from database import init_db
from core.logging import setup_logging, get_logger
from core.exceptions import DevForgeException
from middleware.security import (
    SecurityHeadersMiddleware,
    RequestSizeLimitMiddleware,
    RateLimitMiddleware,
    RequestLoggingMiddleware
)
from middleware.error_handlers import (
    devforge_exception_handler,
    general_exception_handler,
    validation_exception_handler
)
from fastapi.exceptions import RequestValidationError

# Setup logging
setup_logging(level="DEBUG" if settings.debug else "INFO")
logger = get_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup and shutdown events."""
    # Startup
    await init_db()
    logger.info("🚀 DevForge AI Software Company started!")
    logger.info(f"📊 Projects directory: {settings.projects_dir}")
    logger.info(f"🔧 Debug mode: {settings.debug}")
    logger.info(f"🤖 Using Groq model: {settings.groq_model}")
    yield
    # Shutdown
    logger.info("👋 Shutting down...")


app = FastAPI(
    title="Autonomous AI Software Company",
    description="AI agents that build complete SaaS applications",
    version="1.0.0",
    lifespan=lifespan
)

# Add security middleware (order matters - added in reverse execution order)
app.add_middleware(RequestLoggingMiddleware)
app.add_middleware(RateLimitMiddleware, requests_per_minute=100)
app.add_middleware(RequestSizeLimitMiddleware, max_size=10 * 1024 * 1024)  # 10 MB
app.add_middleware(SecurityHeadersMiddleware)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:3001"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add exception handlers
app.add_exception_handler(DevForgeException, devforge_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(Exception, general_exception_handler)

# Include routers
app.include_router(health.router, tags=["Health"])
app.include_router(projects.router, prefix="/api/projects", tags=["Projects"])
app.include_router(agents.router, prefix="/api/agents", tags=["Agents"])


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "Autonomous AI Software Company API",
        "version": "1.0.0",
        "docs": "/docs"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host=settings.api_host,
        port=settings.api_port,
        reload=settings.debug
    )
