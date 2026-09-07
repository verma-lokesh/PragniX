from fastapi import Request
from fastapi.responses import JSONResponse
from core.exceptions import NavoraError
from config.logging import get_logger

logger = get_logger("navora.errors")


async def navora_error_handler(request: Request, exc: NavoraError):
    request_id = getattr(request.state, "request_id", None)
    logger.error(f"{exc.code}: {exc.message}", extra={"request_id": request_id})
    status_map = {
        "VALIDATION_ERROR": 422,
        "NOT_FOUND": 404,
        "GUARDRAIL_VIOLATION": 422,
    }
    status_code = status_map.get(exc.code, 500)
    return JSONResponse(
        status_code=status_code,
        content={"error": {"code": exc.code, "message": exc.message, "request_id": request_id}},
    )


async def unhandled_error_handler(request: Request, exc: Exception):
    request_id = getattr(request.state, "request_id", None)
    logger.error(f"UNHANDLED_ERROR: {exc}", extra={"request_id": request_id})
    return JSONResponse(
        status_code=500,
        content={"error": {"code": "INTERNAL_ERROR", "message": "An internal error occurred.", "request_id": request_id}},
    )
