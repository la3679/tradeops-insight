"""Cross-cutting request correlation and error-envelope tests."""

import re

import pytest
from fastapi import Query
from httpx import ASGITransport, AsyncClient

from tradeops_api.api.errors import AppError, ErrorItem
from tradeops_api.config import Settings
from tradeops_api.main import create_app


@pytest.fixture
def anyio_backend() -> str:
    return "asyncio"


@pytest.mark.anyio
async def test_returns_safe_client_request_id() -> None:
    transport = ASGITransport(app=create_app(Settings(environment="test")))
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/health/live", headers={"X-Request-ID": "demo.request-42"})

    assert response.headers["X-Request-ID"] == "demo.request-42"


@pytest.mark.anyio
async def test_replaces_unsafe_request_id() -> None:
    transport = ASGITransport(app=create_app(Settings(environment="test")))
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/health/live", headers={"X-Request-ID": "line\nbreak"})

    assert re.fullmatch(
        r"[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}",
        response.headers["X-Request-ID"],
    )


@pytest.mark.anyio
async def test_expected_error_uses_stable_envelope() -> None:
    application = create_app(Settings(environment="test"))

    @application.get("/test/conflict")
    async def conflict() -> None:
        raise AppError(
            code="VERSION_CONFLICT",
            message="The exception changed after it was loaded.",
            status_code=409,
            details=(ErrorItem(field="version", reason="stale"),),
        )

    transport = ASGITransport(app=application)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/test/conflict", headers={"X-Request-ID": "request-7"})

    assert response.status_code == 409
    assert response.json() == {
        "error": {
            "code": "VERSION_CONFLICT",
            "details": [{"field": "version", "reason": "stale"}],
            "message": "The exception changed after it was loaded.",
            "request_id": "request-7",
        }
    }


@pytest.mark.anyio
async def test_validation_error_uses_stable_envelope() -> None:
    application = create_app(Settings(environment="test"))

    @application.get("/test/limited")
    async def limited(value: int = Query(ge=1, le=10)) -> dict[str, int]:
        return {"value": value}

    transport = ASGITransport(app=application)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get(
            "/test/limited?value=11",
            headers={"X-Request-ID": "request-8"},
        )

    assert response.status_code == 422
    body = response.json()["error"]
    assert body["code"] == "VALIDATION_ERROR"
    assert body["request_id"] == "request-8"
    assert body["details"] == [{"field": "query.value", "reason": "less_than_equal"}]
