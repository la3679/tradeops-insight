"""Structured logging and OpenTelemetry setup without recording domain payloads."""

import logging

import structlog
from fastapi import FastAPI
from opentelemetry import trace
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor

from tradeops.config import Settings


def configure_observability(app: FastAPI, settings: Settings) -> TracerProvider | None:
    """Instrument non-test API processes and export traces through the local collector."""

    structlog.configure(
        processors=(
            structlog.processors.TimeStamper(fmt="iso", utc=True),
            structlog.processors.add_log_level,
            structlog.processors.JSONRenderer(),
        ),
        wrapper_class=structlog.make_filtering_bound_logger(logging.INFO),
    )
    if settings.environment == "test":
        return None
    provider = TracerProvider(
        resource=Resource.create(
            {
                "service.name": "tradeops-api",
                "deployment.environment.name": settings.environment,
            }
        )
    )
    provider.add_span_processor(
        BatchSpanProcessor(
            OTLPSpanExporter(endpoint=settings.otel_exporter_endpoint, insecure=True)
        )
    )
    trace.set_tracer_provider(provider)
    FastAPIInstrumentor.instrument_app(app, tracer_provider=provider)
    return provider
