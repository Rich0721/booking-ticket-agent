import time
from collections import defaultdict, deque

from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse

from src.core.CSettings import settings


class CRateLimitMiddleware(BaseHTTPMiddleware):
    def __init__(self, app) -> None:
        super().__init__(app)
        self.__request_logs: dict[str, deque[float]] = defaultdict(deque)

    async def dispatch(self, request: Request, call_next):
        client_ip: str = request.client.host if request.client else "unknown"
        now: float = time.time()

        logs: deque[float] = self.__request_logs[client_ip]
        while logs and logs[0] < now - 60:
            logs.popleft()

        if len(logs) >= settings.rate_limit_per_minute:
            return JSONResponse(status_code=429, content={"info": {"message": "請求過於頻繁"}})

        logs.append(now)
        return await call_next(request)
