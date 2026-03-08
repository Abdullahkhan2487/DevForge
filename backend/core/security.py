"""Core security utilities."""
import re
from pathlib import Path
from typing import Optional
from core.exceptions import SecurityError, ValidationError
from core.constants import (
    MIN_SECRET_KEY_LENGTH,
    MAX_PROMPT_LENGTH,
    MAX_PROJECT_NAME_LENGTH,
    MAX_DESCRIPTION_LENGTH,
    ALLOWED_FILE_READ_EXTENSIONS,
    MAX_FILE_READ_SIZE
)


def validate_secret_key(secret_key: str) -> None:
    """
    Validate that secret key meets security requirements.
    
    Args:
        secret_key: Secret key to validate
    
    Raises:
        SecurityError: If secret key is invalid
    """
    if len(secret_key) < MIN_SECRET_KEY_LENGTH:
        raise SecurityError(
            f"Secret key must be at least {MIN_SECRET_KEY_LENGTH} characters long"
        )
    
    if secret_key in ["dev-secret-key-change-in-production", "your-secret-key-here"]:
        raise SecurityError(
            "Default secret key detected. Please set a secure SECRET_KEY in .env"
        )


def sanitize_filename(filename: str) -> str:
    """
    Sanitize filename to prevent path traversal attacks.
    
    Args:
        filename: Filename to sanitize
    
    Returns:
        Sanitized filename
    
    Raises:
        SecurityError: If filename contains invalid characters
    """
    # Remove any path separators
    filename = Path(filename).name
    
    # Check for path traversal attempts
    if ".." in filename or filename.startswith("/") or "\\" in filename:
        raise SecurityError("Invalid filename: path traversal detected")
    
    # Remove any non-alphanumeric characters except dots, dashes, and underscores
    sanitized = re.sub(r'[^a-zA-Z0-9._-]', '_', filename)
    
    if not sanitized or sanitized in [".", ".."]:
        raise SecurityError("Invalid filename")
    
    return sanitized


def validate_file_path(file_path: Path, base_path: Path) -> Path:
    """
    Validate that file path is within base directory.
    
    Args:
        file_path: File path to validate
        base_path: Base directory path
    
    Returns:
        Resolved absolute file path
    
    Raises:
        SecurityError: If path is outside base directory
    """
    try:
        resolved_file = file_path.resolve()
        resolved_base = base_path.resolve()
        
        # Check if file is within base directory
        if not str(resolved_file).startswith(str(resolved_base)):
            raise SecurityError("Access denied: path outside allowed directory")
        
        return resolved_file
    except (OSError, ValueError) as e:
        raise SecurityError(f"Invalid file path: {str(e)}")


def validate_file_extension(file_path: Path) -> None:
    """
    Validate that file extension is allowed.
    
    Args:
        file_path: File path to validate
    
    Raises:
        SecurityError: If file extension is not allowed
    """
    if file_path.suffix.lower() not in ALLOWED_FILE_READ_EXTENSIONS:
        raise SecurityError(f"File type not allowed: {file_path.suffix}")


def validate_file_size(file_path: Path) -> None:
    """
    Validate that file size is within limits.
    
    Args:
        file_path: File path to validate
    
    Raises:
        SecurityError: If file is too large
    """
    if file_path.stat().st_size > MAX_FILE_READ_SIZE:
        raise SecurityError("File too large to read")


def sanitize_input(text: str, max_length: Optional[int] = None) -> str:
    """
    Sanitize user input text.
    
    Args:
        text: Text to sanitize
        max_length: Maximum allowed length
    
    Returns:
        Sanitized text
    
    Raises:
        ValidationError: If input is invalid
    """
    if not text or not isinstance(text, str):
        raise ValidationError("Invalid input: must be non-empty string")
    
    # Strip whitespace
    text = text.strip()
    
    if not text:
        raise ValidationError("Invalid input: cannot be empty or whitespace only")
    
    if max_length and len(text) > max_length:
        raise ValidationError(f"Input too long: maximum {max_length} characters")
    
    return text


def validate_project_prompt(prompt: str) -> str:
    """Validate and sanitize project prompt."""
    return sanitize_input(prompt, MAX_PROMPT_LENGTH)


def validate_project_name(name: Optional[str]) -> Optional[str]:
    """Validate and sanitize project name."""
    if name:
        return sanitize_input(name, MAX_PROJECT_NAME_LENGTH)
    return None


def validate_project_description(description: Optional[str]) -> Optional[str]:
    """Validate and sanitize project description."""
    if description:
        return sanitize_input(description, MAX_DESCRIPTION_LENGTH)
    return None
