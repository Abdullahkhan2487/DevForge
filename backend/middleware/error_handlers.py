"""Error handling middleware."""
from fastapi import Request
from fastapi.responses import JSONResponse
from core.exceptions import DevForgeException
from core.logging import get_logger
import traceback

logger = get_logger(__name__)


async def devforge_exception_handler(request: Request, exc: DevForgeException) -> JSONResponse:
    """Handle custom DevForge exceptions."""
    logger.warning(
        f"DevForge exception: {exc.message}",
        extra={
            "status_code": exc.status_code,
            "details": exc.details,
            "path": request.url.path
        }
    )
    
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": exc.__class__.__name__,
            "message": exc.message,
            "details": exc.details
        }
    )


async def general_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """Handle unexpected exceptions."""
    logger.error(
        f"Unexpected error: {str(exc)}",
        extra={
            "path": request.url.path,
            "traceback": traceback.format_exc()
        }
    )
    
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal Server Error",
            "message": "An unexpected error occurred. Please try again later."
        }
    )


async def validation_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """Handle Pydantic validation exceptions."""
    logger.warning(
        f"Validation error: {str(exc)}",
        extra={"path": request.url.path}
    )
    
    return JSONResponse(
        status_code=422,
        content={
            "error": "Validation Error",
            "message": "Invalid request data",
            "details": str(exc)
        }
    )
