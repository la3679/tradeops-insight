from fastapi.testclient import TestClient

from tradeops.api.app import create_app
from tradeops.config import Settings


def test_health_contracts_are_deterministic() -> None:
    client = TestClient(create_app(Settings(environment="test")))
    expected = {
        "status": "ok",
        "service": "TradeOps Copilot API",
        "version": "0.1.0",
        "environment": "test",
    }

    assert client.get("/api/v1/health/live").json() == expected
    assert client.get("/api/v1/health/ready").json() == expected


def test_production_disables_interactive_api_documentation() -> None:
    client = TestClient(create_app(Settings(environment="production")))

    assert client.get("/docs").status_code == 404
    assert client.get("/openapi.json").status_code == 200
