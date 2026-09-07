"""Lightweight OpenTelemetry-compatible tracing shim.
Uses OTEL SDK if installed and OTEL_ENDPOINT is set; otherwise no-ops so the
app runs without an external collector.
"""
import contextlib
from config.settings import get_settings


@contextlib.contextmanager
def trace_span(name: str, **attrs):
    settings = get_settings()
    if not settings.OTEL_ENDPOINT:
        yield
        return
    try:
        from opentelemetry import trace
        tracer = trace.get_tracer("navora")
        with tracer.start_as_current_span(name, attributes=attrs):
            yield
    except ImportError:
        yield
