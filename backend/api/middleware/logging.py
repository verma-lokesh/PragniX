import time
from starlette.middleware.base import BaseHTTPMiddleware
from config.logging import get_logger

logger = get_logger("navora.api")


class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        start = time.perf_counter()
        response = await call_next(request)
        duration_ms = round((time.perf_counter() - start) * 1000, 2)
        logger.info(
            f"{request.method} {request.url.path} -> {response.status_code}",
            extra={
                "request_id": getattr(request.state, "request_id", None),
                "duration_ms": duration_ms,
                "status": response.status_code,
            },
        )
        return response
