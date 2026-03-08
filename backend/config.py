"""Configuration settings for the application."""
from pydantic_settings import BaseSettings
from typing import Optional
import os
from core.security import validate_secret_key
from core.exceptions import ConfigurationError
from core.logging import get_logger

logger = get_logger(__name__)


class Settings(BaseSettings):
    """Application settings."""
    
    # API Settings
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    debug: bool = False
    
    # Groq LLM Settings
    groq_api_key: str
    groq_model: str = "llama-3.3-70b-versatile"
    
    # Database Settings
    database_url: str = "sqlite:///./devforge.db"
    pool_size: int = 5
    max_overflow: int = 10
    pool_timeout: int = 30
    
    # Redis Settings (Optional)
    redis_url: Optional[str] = None
    
    # Project Generation
    projects_dir: str = "../generated_projects"
    
    # Security
    secret_key: str = "dev-secret-key-change-in-production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    
    class Config:
        env_file = ".env"
        case_sensitive = False
    
    def validate_settings(self):
        """Validate critical settings on startup."""
        # Validate secret key
        if not validate_secret_key(self.secret_key):
            if self.debug:
                logger.warning("Using weak secret key - NOT RECOMMENDED for production!")
            else:
                raise ConfigurationError(
                    "SECRET_KEY must be at least 32 characters in production mode. "
                    "Set DEBUG=True to run with weak key for development."
                )
        
        # Validate Groq API key
        if not self.groq_api_key or len(self.groq_api_key.strip()) == 0:
            raise ConfigurationError("GROQ_API_KEY is required")
        
        if not self.groq_api_key.startswith("gsk_"):
            logger.warning("GROQ_API_KEY does not start with 'gsk_' - verify it's correct")
        
        logger.info("Configuration validated successfully")


# Global settings instance
settings = Settings()

# Validate settings on startup
settings.validate_settings()

# Set Groq API key as environment variable for LiteLLM
os.environ["GROQ_API_KEY"] = settings.groq_api_key

# Ensure projects directory exists
os.makedirs(settings.projects_dir, exist_ok=True)
