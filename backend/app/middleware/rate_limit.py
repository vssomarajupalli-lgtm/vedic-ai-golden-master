import time
from typing import Dict, Optional
from collections import defaultdict
from fastapi import Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response
from app.core.config import settings


class RateLimitMiddleware(BaseHTTPMiddleware):
    """
    In-memory rate limiting middleware.
    For production, replace with Redis-backed implementation.
    """

    def __init__(self, app, requests_per_minute: int = 60, burst: int = 10):
        super().__init__(app)
        self.requests_per_minute = requests_per_minute
        self.burst = burst
        # Store: {client_ip: [(timestamp, count)]}
        self.requests: Dict[str, list] = defaultdict(list)
        self.blocked_ips: Dict[str, float] = {}

    async def dispatch(self, request: Request, call_next):
        # Skip rate limiting for health checks
        if request.url.path in ["/api/v1/health", "/health", "/"]:
            return await call_next(request)

        if not settings.RATE_LIMIT_ENABLED:
            return await call_next(request)

        client_ip = self._get_client_ip(request)
        current_time = time.time()

        # Check if IP is temporarily blocked
        if client_ip in self.blocked_ips:
            if current_time < self.blocked_ips[client_ip]:
                raise HTTPException(
                    status_code=429,
                    detail="Rate limit exceeded. Please try again later.",
                    headers={"Retry-After": str(int(self.blocked_ips[client_ip] - current_time))}
                )
            else:
                del self.blocked_ips[client_ip]

        # Clean old requests (older than 1 minute)
        minute_ago = current_time - 60
        self.requests[client_ip] = [
            (ts, count) for ts, count in self.requests[client_ip]
            if ts > minute_ago
        ]

        # Count requests in current window
        request_count = sum(count for _, count in self.requests[client_ip])

        # Check burst limit
        if request_count >= self.burst:
            # Block for 60 seconds
            self.blocked_ips[client_ip] = current_time + 60
            raise HTTPException(
                status_code=429,
                detail="Burst limit exceeded. Please slow down.",
                headers={"Retry-After": "60"}
            )

        # Check per-minute limit
        if request_count >= self.requests_per_minute:
            raise HTTPException(
                status_code=429,
                detail=f"Rate limit exceeded. Max {self.requests_per_minute} requests per minute.",
                headers={"Retry-After": "60"}
            )

        # Record this request
        self.requests[client_ip].append((current_time, 1))

        # Add rate limit headers
        response: Response = await call_next(request)
        response.headers["X-RateLimit-Limit"] = str(self.requests_per_minute)
        response.headers["X-RateLimit-Remaining"] = str(
            max(0, self.requests_per_minute - request_count - 1)
        )
        response.headers["X-RateLimit-Reset"] = str(int(current_time + 60))

        return response

    def _get_client_ip(self, request: Request) -> str:
        """Extract client IP considering proxies."""
        forwarded = request.headers.get("X-Forwarded-For")
        if forwarded:
            return forwarded.split(",")[0].strip()
        real_ip = request.headers.get("X-Real-IP")
        if real_ip:
            return real_ip
        return request.client.host if request.client else "unknown"