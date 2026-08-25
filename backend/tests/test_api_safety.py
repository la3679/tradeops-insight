"""HTTP envelope, request-size, and rate-limit safety tests."""

from fastapi.testclient import TestClient

from tradeops.api.app import create_app
from tradeops.config import Settings


def test_validation_errors_use_stable_problem_envelope() -> None:
    client = TestClient(create_app(Settings(environment="test")))

    response = client.get("/api/v1/trades?limit=1000", headers={"X-Request-ID": "request-123"})

    assert response.status_code == 422
    assert response.headers["content-type"].startswith("application/problem+json")
    assert response.json()["code"] == "validation_error"
    assert response.json()["request_id"] == "request-123"


def test_request_size_limit_rejects_before_body_processing() -> None:
    client = TestClient(create_app(Settings(environment="test", max_request_bytes=1024)))

    response = client.post(
        "/api/v1/imports/synthetic",
        content="x" * 1025,
        headers={"X-Demo-Role": "administrator", "Idempotency-Key": "large-request-01"},
    )

    assert response.status_code == 413
    assert response.json()["code"] == "request_too_large"


def test_rate_limit_returns_retry_contract() -> None:
    client = TestClient(create_app(Settings(environment="test", rate_limit_per_minute=1)))

    assert client.get("/api/v1/version").status_code == 200
    response = client.get("/api/v1/version")

    assert response.status_code == 429
    assert response.headers["retry-after"] == "60"
    assert response.json()["code"] == "rate_limited"
