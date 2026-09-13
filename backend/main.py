from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from config.settings import get_settings
from config.logging import configure_logging
from api.routes import api_router
from api.middleware.request_id import RequestIDMiddleware
from api.middleware.logging import LoggingMiddleware
from api.middleware.error_handler import navora_error_handler, unhandled_error_handler
from core.exceptions import NavoraError

settings = get_settings()
configure_logging("DEBUG" if settings.DEBUG else "INFO")

app = FastAPI(
    title="AnchorIQ API",
    description="Intelligent maritime freight decision-support platform.",
    version="0.1.0",
)

app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])
app.add_middleware(LoggingMiddleware)
app.add_middleware(RequestIDMiddleware)

app.add_exception_handler(NavoraError, navora_error_handler)
app.add_exception_handler(Exception, unhandled_error_handler)

app.include_router(api_router)


@app.get("/")
def root():
    return {"app": settings.APP_NAME, "status": "running"}
