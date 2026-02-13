import time
import logging
from typing import Callable
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from models.rate_limit_model import RateLimitInfo

logger = logging.getLogger(__name__)


class RequestLoggingMiddleware(BaseHTTPMiddleware):

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        start_time = time.time()
        
        logger.info(f"Incoming: {request.method} {request.url.path}")
        
        response = await call_next(request)
        
        process_time = time.time() - start_time
        
        response.headers["X-Process-Time"] = str(process_time)
        
        logger.info(
            f"Completed: {request.method} {request.url.path} "
            f"Status: {response.status_code} Time: {process_time:.3f}s"
        )
        
        return response


class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        response = await call_next(request)
        
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        response.headers["Strict-Transport-Security"] = "max-age=120; includeSubDomains"
        
        return response

rate_limiter = RateLimitInfo(max_requests=100, window_seconds=60)


class RateLimitMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        client_ip = request.client.host if request.client else "unknown"
        
        excluded_paths = ["/docs", "/openapi.json", "/redoc"]
        if request.url.path in excluded_paths:
            return await call_next(request)
        
        allowed, remaining = rate_limiter.is_allowed(client_ip)
        
        if not allowed:
            logger.warning(f"Rate limit exceeded for {client_ip}")
            return Response(
                content='{"error": "Rate limit exceeded. Please try again later."}',
                status_code=429,
                media_type="application/json",
                headers={
                    "X-RateLimit-Limit": str(rate_limiter.max_requests),
                    "X-RateLimit-Remaining": "0",
                    "X-RateLimit-Reset": str(int(time.time() + rate_limiter.window_seconds))
                }
            )
        
        response = await call_next(request)
        
        response.headers["X-RateLimit-Limit"] = str(rate_limiter.max_requests)
        response.headers["X-RateLimit-Remaining"] = str(remaining)
        
        return response
