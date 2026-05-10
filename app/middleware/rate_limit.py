"""Rate Limiting Middleware - API Key based"""

from fastapi import Request
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from datetime import datetime, timedelta
import hashlib


class RateLimitMiddleware(BaseHTTPMiddleware):
    """API Key based rate limiter"""

    def __init__(self, app, calls: int = 60, period: int = 60):
        super().__init__(app)
        self.calls = calls
        self.period = period
        self._buckets: dict = {}

    def _get_key(self, request: Request) -> str | None:
        """Extract API key hash from Authorization header"""
        auth = request.headers.get("authorization", "")
        if auth.startswith("Bearer "):
            key = auth[7:]
            return hashlib.sha256(key.encode()).hexdigest()[:16]
        elif auth.startswith("sk-"):
            return hashlib.sha256(auth.encode()).hexdigest()[:16]
        return None

    def _clean_old(self, key: str):
        cutoff = datetime.utcnow() - timedelta(seconds=self.period)
        if key in self._buckets:
            self._buckets[key] = [t for t in self._buckets[key] if t > cutoff]

    async def dispatch(self, request: Request, call_next):
        # Skip for public endpoints
        if request.url.path in [
            "/",
            "/health",
            "/docs",
            "/openapi.json",
            "/auth",
            "/api/keys",
        ]:
            return await call_next(request)

        key = self._get_key(request)
        if not key:
            # No auth = let pass (will be rejected by endpoint auth)
            return await call_next(request)

        self._clean_old(key)
        bucket = self._buckets.setdefault(key, [])

        if len(bucket) >= self.calls:
            return JSONResponse(
                status_code=429,
                content={"detail": "Rate limit exceeded", "retry_after": self.period},
            )

        bucket.append(datetime.utcnow())

        response = await call_next(request)
        response.headers["X-RateLimit-Limit"] = str(self.calls)
        response.headers["X-RateLimit-Remaining"] = str(self.calls - len(bucket))
        return response
