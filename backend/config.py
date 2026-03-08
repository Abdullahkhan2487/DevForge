"""Configuration settings for the application."""
from pydantic_settings import BaseSettings
from typing import Optional
import os


class Settings(BaseSettings):
    """Application settings."""
    
    # API Settings
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    debug: bool = True
    
    # Groq LLM Settings
    groq_api_key: str
    groq_model: str = "llama-3.3-70b-versatile"
    
    # Database Settings
    database_url: str = "sqlite:///./devforge.db"
    
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


# Global settings instance
settings = Settings()

# Set Groq API key as environment variable for LiteLLM
os.environ["GROQ_API_KEY"] = settings.groq_api_key

# Ensure projects directory exists
os.makedirs(settings.projects_dir, exist_ok=True)
