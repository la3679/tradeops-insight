"""Prometheus exposition tests."""

from fastapi.testclient import TestClient

from tradeops.api.app import create_app
from tradeops.config import Settings


def test_metrics_expose_low_cardinality_request_counts() -> None:
    client = TestClient(create_app(Settings(environment="test")))

    client.get("/api/v1/version")
    response = client.get("/metrics")

    assert response.status_code == 200
    assert "tradeops_http_requests_total" in response.text
    assert 'method="GET",status_class="2xx"' in response.text
    assert "TRD-DEMO" not in response.text
