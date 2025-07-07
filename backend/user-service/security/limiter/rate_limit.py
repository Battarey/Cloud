from fastapi import Request, HTTPException, status
from starlette.middleware.base import BaseHTTPMiddleware
import time
from collections import defaultdict

RATE_LIMIT = 10  # запросов
RATE_PERIOD = 60  # секунд

class RateLimiter(BaseHTTPMiddleware):
    def __init__(self, app):
        super().__init__(app)
        self.requests = defaultdict(list)

    async def dispatch(self, request: Request, call_next):
        client_ip = request.client.host
        now = time.time()
        self.requests[client_ip] = [t for t in self.requests[client_ip] if now - t < RATE_PERIOD]
        if len(self.requests[client_ip]) >= RATE_LIMIT:
            raise HTTPException(status_code=status.HTTP_429_TOO_MANY_REQUESTS, detail="Too many requests")
        self.requests[client_ip].append(now)
        response = await call_next(request)
        return response
