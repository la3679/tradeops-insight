"""Process health contracts that do not probe unconfigured infrastructure."""

from typing import Literal

from fastapi import APIRouter, Request
from pydantic import BaseModel, ConfigDict

from tradeops import __version__
from tradeops.config import Settings

router = APIRouter(prefix="/health", tags=["health"])


class HealthResponse(BaseModel):
    model_config = ConfigDict(frozen=True)

    status: Literal["ok"] = "ok"
    service: str
    version: str
    environment: Literal["local", "test", "production"]


def _response(request: Request) -> HealthResponse:
    settings: Settings = request.app.state.settings
    return HealthResponse(
        service=settings.app_name, version=__version__, environment=settings.environment
    )


@router.get("/live", response_model=HealthResponse)
def liveness(request: Request) -> HealthResponse:
    """Confirm that the API process can serve requests."""

    return _response(request)


@router.get("/ready", response_model=HealthResponse)
def readiness(request: Request) -> HealthResponse:
    """Confirm readiness for the currently dependency-free API."""

    return _response(request)
