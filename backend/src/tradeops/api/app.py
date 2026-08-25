"""FastAPI application factory."""

from fastapi import FastAPI

from tradeops import __version__
from tradeops.api.routes.health import router as health_router
from tradeops.config import Settings, get_settings


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
    app.include_router(health_router, prefix=resolved.api_prefix)
    return app


app = create_app()
