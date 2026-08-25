"""FastAPI application factory."""

from fastapi import FastAPI

from tradeops_api import __version__
from tradeops_api.api.errors import install_exception_handlers
from tradeops_api.api.http import install_http_middleware
from tradeops_api.api.router import api_router
from tradeops_api.api.routes.health import router as health_router
from tradeops_api.config import Settings, get_settings


def create_app(settings: Settings | None = None) -> FastAPI:
    """Build an application without mutable module-level clients."""

    resolved = settings or get_settings()
    docs_enabled = resolved.environment != "production"
    application = FastAPI(
        title=resolved.app_name,
        version=__version__,
        docs_url="/docs" if docs_enabled else None,
        redoc_url=None,
        openapi_url="/openapi.json" if docs_enabled else None,
    )
    application.dependency_overrides[get_settings] = lambda: resolved
    install_http_middleware(application)
    install_exception_handlers(application)
    application.include_router(health_router)
    application.include_router(api_router, prefix=resolved.api_v1_prefix)
    return application


app = create_app()
