"""API process-health and metadata contract tests."""

import pytest
from httpx import ASGITransport, AsyncClient

from tradeops_api.config import Settings
from tradeops_api.main import create_app


@pytest.fixture
def anyio_backend() -> str:
    """Keep the suite independent of an optional Trio installation."""

    return "asyncio"


@pytest.mark.anyio
async def test_liveness_contract() -> None:
    transport = ASGITransport(app=create_app(Settings(environment="test")))
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/health/live")

    assert response.status_code == 200
    assert response.json() == {"service": "tradeops-api", "status": "ok"}


@pytest.mark.anyio
async def test_readiness_reports_named_checks() -> None:
    transport = ASGITransport(app=create_app(Settings(environment="test")))
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/health/ready")

    assert response.status_code == 200
    assert response.json() == {
        "checks": [{"name": "configuration", "status": "pass"}],
        "service": "tradeops-api",
        "status": "ok",
    }


@pytest.mark.anyio
async def test_version_reports_test_environment() -> None:
    transport = ASGITransport(app=create_app(Settings(environment="test")))
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/api/v1/meta/version")

    assert response.status_code == 200
    assert response.json() == {
        "environment": "test",
        "service": "tradeops-api",
        "version": "0.1.0",
    }


@pytest.mark.anyio
async def test_production_disables_interactive_schema_routes() -> None:
    transport = ASGITransport(app=create_app(Settings(environment="production")))
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        docs_response = await client.get("/docs")
        schema_response = await client.get("/openapi.json")

    assert docs_response.status_code == 404
    assert schema_response.status_code == 404
