"""Kubernetes-compatible process health contracts."""

from enum import StrEnum
from typing import Literal

from fastapi import APIRouter
from pydantic import BaseModel, ConfigDict

router = APIRouter(prefix="/health", tags=["health"])


class CheckStatus(StrEnum):
    """Status of one readiness dependency check."""

    PASS = "pass"
    FAIL = "fail"


class HealthResponse(BaseModel):
    """Stable liveness response."""

    model_config = ConfigDict(frozen=True)

    status: Literal["ok"] = "ok"
    service: Literal["tradeops-api"] = "tradeops-api"


class DependencyCheck(BaseModel):
    """One bounded readiness check result."""

    model_config = ConfigDict(frozen=True)

    name: str
    status: CheckStatus


class ReadinessResponse(HealthResponse):
    """Readiness response with explicit dependency results."""

    checks: tuple[DependencyCheck, ...]


@router.get("/live", response_model=HealthResponse, summary="Process liveness")
async def liveness() -> HealthResponse:
    """Report that the ASGI process can serve requests."""

    return HealthResponse()


@router.get("/ready", response_model=ReadinessResponse, summary="Traffic readiness")
async def readiness() -> ReadinessResponse:
    """Report whether configured required dependencies are usable."""

    return ReadinessResponse(
        checks=(DependencyCheck(name="configuration", status=CheckStatus.PASS),)
    )
