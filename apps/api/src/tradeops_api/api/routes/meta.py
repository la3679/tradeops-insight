"""Service metadata routes."""

from typing import Annotated

from fastapi import APIRouter, Depends
from pydantic import BaseModel, ConfigDict

from tradeops_api import __version__
from tradeops_api.config import Settings, get_settings

router = APIRouter(tags=["metadata"])


class VersionResponse(BaseModel):
    """Build and runtime identity safe for public diagnostics."""

    model_config = ConfigDict(frozen=True)

    service: str
    version: str
    environment: str


@router.get("/version", response_model=VersionResponse, summary="Service version")
async def service_version(
    settings: Annotated[Settings, Depends(get_settings)],
) -> VersionResponse:
    """Return non-secret service metadata."""

    return VersionResponse(
        service="tradeops-api",
        version=__version__,
        environment=settings.environment,
    )
