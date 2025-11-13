from typing import Any

from fastapi import FastAPI
from opentelemetry import trace
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor

from app.core.config import settings
from app.core.logging import get_logger

logger = get_logger(__name__)


def setup_telemetry(app: FastAPI) -> None:
    """Configure OpenTelemetry tracing."""

    if not settings.OTEL_ENABLED:
        logger.info("OpenTelemetry disabled")
        return

    # Create resource with service metadata
    resource = Resource.create(
        {
            "service.name": settings.OTEL_SERVICE_NAME,
            "service.version": settings.VERSION,
        }
    )

    # Setup tracer provider
    provider = TracerProvider(resource=resource)

    # Configure OTLP exporter (Jaeger/Tempo)
    try:
        exporter = OTLPSpanExporter(
            endpoint=settings.OTEL_EXPORTER_OTLP_ENDPOINT,
            insecure=True,
        )
        provider.add_span_processor(BatchSpanProcessor(exporter))
        trace.set_tracer_provider(provider)

        # Instrument FastAPI
        FastAPIInstrumentor.instrument_app(app)

        logger.info(
            "OpenTelemetry configured",
            endpoint=settings.OTEL_EXPORTER_OTLP_ENDPOINT,
        )
    except Exception as e:
        logger.error("Failed to setup OpenTelemetry", error=str(e))


def get_tracer(name: str) -> Any:
    """Get a tracer instance."""
    return trace.get_tracer(name)
