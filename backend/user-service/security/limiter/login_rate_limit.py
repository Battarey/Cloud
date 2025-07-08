from fastapi import Request, HTTPException, status
from starlette.middleware.base import BaseHTTPMiddleware
import time
from collections import defaultdict

LOGIN_RATE_LIMIT = 10  # попыток
LOGIN_RATE_PERIOD = 60  # секунд

class LoginRateLimiter(BaseHTTPMiddleware):
    def __init__(self, app):
        super().__init__(app)
        self.attempts = defaultdict(list)

    async def dispatch(self, request: Request, call_next):
        if request.url.path == "/auth/login":
            client_ip = request.client.host
            now = time.time()
            self.attempts[client_ip] = [t for t in self.attempts[client_ip] if now - t < LOGIN_RATE_PERIOD]
            if len(self.attempts[client_ip]) >= LOGIN_RATE_LIMIT:
                raise HTTPException(status_code=status.HTTP_429_TOO_MANY_REQUESTS, detail="Too many login attempts")
            self.attempts[client_ip].append(now)
        response = await call_next(request)
        return response
