"""Constants and enums for the application."""
from enum import Enum


class ProjectStatus(str, Enum):
    """Project status values."""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"


class AgentStatus(str, Enum):
    """Agent execution status values."""
    STARTED = "started"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"


class AgentName(str, Enum):
    """Available agent names."""
    PRODUCT_MANAGER = "ProductManagerAgent"
    SOFTWARE_ARCHITECT = "SoftwareArchitectAgent"
    BACKEND_DEVELOPER = "BackendDeveloperAgent"
    FRONTEND_DEVELOPER = "FrontendDeveloperAgent"
    QA_TESTER = "QATesterAgent"
    CODE_REVIEWER = "CodeReviewerAgent"


# Request limits
MAX_PROMPT_LENGTH = 5000
MAX_PROJECT_NAME_LENGTH = 200
MAX_DESCRIPTION_LENGTH = 1000
MAX_REQUEST_SIZE = 10 * 1024 * 1024  # 10MB

# Pagination
DEFAULT_PAGE_SIZE = 20
MAX_PAGE_SIZE = 100

# File operations
ALLOWED_FILE_READ_EXTENSIONS = {
    ".py", ".js", ".jsx", ".ts", ".tsx", ".json", ".md", ".txt",
    ".yaml", ".yml", ".toml", ".css", ".html", ".sh", ".env.example"
}

MAX_FILE_READ_SIZE = 5 * 1024 * 1024  # 5MB

# Security
MIN_SECRET_KEY_LENGTH = 32
SECURE_HEADERS = {
    "X-Content-Type-Options": "nosniff",
    "X-Frame-Options": "DENY",
    "X-XSS-Protection": "1; mode=block",
    "Strict-Transport-Security": "max-age=31536000; includeSubDomains",
}

# Rate limiting (requests per minute)
RATE_LIMIT_PROJECT_CREATE = 10
RATE_LIMIT_PROJECT_LIST = 60
RATE_LIMIT_DEFAULT = 100
