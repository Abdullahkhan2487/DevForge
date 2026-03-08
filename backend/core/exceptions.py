"""Core exceptions for the application."""
from typing import Optional, Any, Dict


class DevForgeException(Exception):
    """Base exception for DevForge application."""
    
    def __init__(
        self,
        message: str,
        status_code: int = 500,
        details: Optional[Dict[str, Any]] = None
    ):
        self.message = message
        self.status_code = status_code
        self.details = details or {}
        super().__init__(self.message)


class ValidationError(DevForgeException):
    """Raised when input validation fails."""
    
    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(message, status_code=400, details=details)


class NotFoundError(DevForgeException):
    """Raised when a resource is not found."""
    
    def __init__(self, resource: str, identifier: Any):
        message = f"{resource} with identifier '{identifier}' not found"
        super().__init__(message, status_code=404)


class DatabaseError(DevForgeException):
    """Raised when database operations fail."""
    
    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(message, status_code=500, details=details)


class WorkflowError(DevForgeException):
    """Raised when agent workflow execution fails."""
    
    def __init__(self, message: str, agent_name: Optional[str] = None):
        details = {"agent_name": agent_name} if agent_name else {}
        super().__init__(message, status_code=500, details=details)


class SecurityError(DevForgeException):
    """Raised when security validation fails."""
    
    def __init__(self, message: str):
        super().__init__(message, status_code=403)


class ConfigurationError(DevForgeException):
    """Raised when configuration is invalid."""
    
    def __init__(self, message: str):
        super().__init__(message, status_code=500)


class RateLimitError(DevForgeException):
    """Raised when rate limit is exceeded."""
    
    def __init__(self, message: str = "Rate limit exceeded"):
        super().__init__(message, status_code=429)
