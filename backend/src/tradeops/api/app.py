"""FastAPI application factory and cross-cutting HTTP safety contracts."""

from time import perf_counter
from uuid import uuid4

import structlog
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, Response
from starlette.middleware.base import RequestResponseEndpoint
from starlette.middleware.cors import CORSMiddleware

from tradeops import __version__
from tradeops.api.routes.health import router as health_router
from tradeops.api.routes.operations import router as operations_router
from tradeops.api.security import OidcTokenDecoder
from tradeops.application.demo_operations import (
    DemoConflictError,
    DemoNotFoundError,
    DemoOperationsService,
)
from tradeops.config import Settings, get_settings
from tradeops.observability import configure_observability


def create_app(settings: Settings | None = None) -> FastAPI:
    """Create an API process without opening external connections."""

    resolved = settings or get_settings()
    app = FastAPI(
        title=resolved.app_name,
        version=__version__,
        docs_url="/docs" if resolved.environment != "production" else None,
        redoc_url=None,
    )
    app.state.settings = resolved
    app.state.token_decoder = OidcTokenDecoder(
        issuer=resolved.oidc_issuer, audience=resolved.oidc_audience
    )
    app.state.operations = DemoOperationsService(dataset_size=resolved.demo_dataset_size)
    if resolved.environment != "production":
        app.add_middleware(
            CORSMiddleware,
            allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
            allow_methods=["GET", "POST", "OPTIONS"],
            allow_headers=["Content-Type", "Idempotency-Key", "X-Demo-Role", "X-Request-ID"],
        )
    app.include_router(health_router, prefix=resolved.api_prefix)
    app.include_router(operations_router, prefix=resolved.api_prefix)
    app.state.tracer_provider = configure_observability(app, resolved)

    @app.middleware("http")
    async def request_context(request: Request, call_next: RequestResponseEndpoint) -> Response:
        request_id = request.headers.get("X-Request-ID", str(uuid4()))
        started = perf_counter()
        response = await call_next(request)
        response.headers["X-Request-ID"] = request_id
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["Referrer-Policy"] = "no-referrer"
        response.headers["Cache-Control"] = "no-store"
        structlog.get_logger("tradeops.api").info(
            "request.completed",
            environment=resolved.environment,
            request_id=request_id,
            method=request.method,
            route=request.url.path,
            status_code=response.status_code,
            duration_ms=round((perf_counter() - started) * 1000, 2),
        )
        return response

    @app.exception_handler(DemoNotFoundError)
    async def not_found(request: Request, error: DemoNotFoundError) -> JSONResponse:
        return _problem(request, 404, "Not Found", str(error))

    @app.exception_handler(DemoConflictError)
    async def conflict(request: Request, error: DemoConflictError) -> JSONResponse:
        return _problem(request, 409, "Conflict", str(error))

    return app


def _problem(request: Request, status_code: int, title: str, detail: str) -> JSONResponse:
    return JSONResponse(
        status_code=status_code,
        media_type="application/problem+json",
        content={
            "type": "about:blank",
            "title": title,
            "status": status_code,
            "detail": detail,
            "instance": request.url.path,
        },
    )


app = create_app()
