"""Security middleware for the application."""
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse
from typing import Callable
import time
from collections import defaultdict
from datetime import datetime, timedelta
from core.constants import SECURE_HEADERS, RATE_LIMIT_DEFAULT, MAX_REQUEST_SIZE
from core.exceptions import RateLimitError
from core.logging import get_logger

logger = get_logger(__name__)


class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    """Add security headers to all responses."""
    
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        """Add security headers to response."""
        response = await call_next(request)
        
        # Add security headers
        for header_name, header_value in SECURE_HEADERS.items():
            response.headers[header_name] = header_value
        
        return response


class RequestSizeLimitMiddleware(BaseHTTPMiddleware):
    """Limit request body size to prevent DOS attacks."""
    
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        """Check request size before processing."""
        if request.headers.get("content-length"):
            content_length = int(request.headers["content-length"])
            if content_length > MAX_REQUEST_SIZE:
                logger.warning(
                    f"Request too large: {content_length} bytes",
                    extra={"ip": request.client.host, "path": request.url.path}
                )
                return JSONResponse(
                    status_code=413,
                    content={
                        "error": "Request Entity Too Large",
                        "message": f"Request body must be less than {MAX_REQUEST_SIZE} bytes"
                    }
                )
        
        return await call_next(request)


class RateLimitMiddleware(BaseHTTPMiddleware):
    """Rate limit requests based on IP address."""
    
    def __init__(self, app, requests_per_minute: int = RATE_LIMIT_DEFAULT):
        super().__init__(app)
        self.requests_per_minute = requests_per_minute
        self.request_counts: dict = defaultdict(list)
        self.cleanup_interval = 60  # Clean up old entries every 60 seconds
        self.last_cleanup = time.time()
    
    def _cleanup_old_requests(self) -> None:
        """Remove old request timestamps."""
        current_time = time.time()
        if current_time - self.last_cleanup > self.cleanup_interval:
            cutoff_time = datetime.now() - timedelta(minutes=1)
            for ip in list(self.request_counts.keys()):
                self.request_counts[ip] = [
                    ts for ts in self.request_counts[ip]
                    if ts > cutoff_time
                ]
                if not self.request_counts[ip]:
                    del self.request_counts[ip]
            self.last_cleanup = current_time
    
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        """Check rate limit before processing request."""
        # Skip rate limiting for health checks
        if request.url.path == "/health":
            return await call_next(request)
        
        # Get client IP
        client_ip = request.client.host if request.client else "unknown"
        
        # Clean up old entries periodically
        self._cleanup_old_requests()
        
        # Check rate limit
        current_time = datetime.now()
        one_minute_ago = current_time - timedelta(minutes=1)
        
        # Count requests in the last minute
        recent_requests = [
            ts for ts in self.request_counts[client_ip]
            if ts > one_minute_ago
        ]
        
        if len(recent_requests) >= self.requests_per_minute:
            logger.warning(
                f"Rate limit exceeded for IP: {client_ip}",
                extra={"ip": client_ip, "path": request.url.path}
            )
            return JSONResponse(
                status_code=429,
                content={
                    "error": "Rate Limit Exceeded",
                    "message": f"Too many requests. Limit: {self.requests_per_minute} requests per minute"
                }
            )
        
        # Add current request timestamp
        self.request_counts[client_ip].append(current_time)
        
        return await call_next(request)


class RequestLoggingMiddleware(BaseHTTPMiddleware):
    """Log all incoming requests."""
    
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        """Log request and response."""
        start_time = time.time()
        
        # Log request
        logger.info(
            f"Request: {request.method} {request.url.path}",
            extra={
                "method": request.method,
                "path": request.url.path,
                "ip": request.client.host if request.client else "unknown",
                "user_agent": request.headers.get("user-agent", "unknown")
            }
        )
        
        # Process request
        response = await call_next(request)
        
        # Calculate duration
        duration = time.time() - start_time
        
        # Log response
        logger.info(
            f"Response: {response.status_code} ({duration:.3f}s)",
            extra={
                "status_code": response.status_code,
                "duration": duration,
                "path": request.url.path
            }
        )
        
        return response
