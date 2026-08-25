"""Platform API contract and privileged-operation tests."""

from fastapi.testclient import TestClient

from tradeops.api.app import create_app
from tradeops.config import Settings


def _client() -> TestClient:
    return TestClient(create_app(Settings(environment="test", demo_dataset_size=24)))


def test_dashboard_trades_knowledge_and_evaluation_contracts() -> None:
    client = _client()

    summary = client.get("/api/v1/dashboard/summary")
    trades = client.get("/api/v1/trades?limit=5")
    documents = client.get("/api/v1/knowledge/documents")
    cases = client.get("/api/v1/evaluations/cases")
    version = client.get("/api/v1/version")

    assert summary.status_code == 200
    assert summary.json()["data_classification"] == "synthetic"
    assert trades.status_code == 200
    assert len(trades.json()["items"]) == 5
    assert documents.status_code == 200
    assert len(documents.json()) == 4
    assert cases.status_code == 200
    assert len(cases.json()) == 50
    assert version.json()["api_version"] == "v1"


def test_import_is_admin_only_and_idempotent() -> None:
    client = _client()
    headers = {"X-Demo-Role": "administrator", "Idempotency-Key": "import-key-001"}

    denied = client.post(
        "/api/v1/imports/synthetic",
        headers={"X-Demo-Role": "analyst", "Idempotency-Key": "import-key-001"},
    )
    first = client.post("/api/v1/imports/synthetic", headers=headers)
    replay = client.post("/api/v1/imports/synthetic", headers=headers)

    assert denied.status_code == 403
    assert first.status_code == 202
    assert first.json()["status"] == "accepted"
    assert replay.json()["status"] == "duplicate"
    assert replay.json()["import_id"] == first.json()["import_id"]


def test_source_sync_and_evaluation_runs_require_admin() -> None:
    client = _client()
    analyst_headers = {"X-Demo-Role": "analyst", "Idempotency-Key": "operation-key-001"}
    admin_headers = {"X-Demo-Role": "administrator", "Idempotency-Key": "operation-key-001"}

    assert client.post("/api/v1/sources/gleif/sync", headers=analyst_headers).status_code == 403
    assert client.post("/api/v1/evaluations/runs", headers=analyst_headers).status_code == 403
    synced = client.post("/api/v1/sources/gleif/sync", headers=admin_headers)
    evaluated = client.post("/api/v1/evaluations/runs", headers=admin_headers)

    assert synced.status_code == 200
    assert synced.json()["status"] == "fixture_verified"
    assert evaluated.status_code == 200
    assert evaluated.json()["total"] == evaluated.json()["passed"] == 50


def test_non_allowlisted_source_is_rejected() -> None:
    response = _client().post(
        "/api/v1/sources/private-bank/sync",
        headers={"X-Demo-Role": "administrator", "Idempotency-Key": "operation-key-002"},
    )

    assert response.status_code == 404
