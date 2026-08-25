"""Versioned API success, authorization, conflict, and idempotency tests."""

from fastapi.testclient import TestClient

from tradeops.api.app import create_app
from tradeops.config import Settings


def _client() -> TestClient:
    return TestClient(create_app(Settings(environment="test", demo_dataset_size=24)))


def test_queue_detail_filters_and_security_headers() -> None:
    with _client() as client:
        response = client.get("/api/v1/exceptions?status=open", headers={"X-Demo-Role": "analyst"})
        body = response.json()
        detail = client.get(
            f"/api/v1/exceptions/{body['items'][0]['id']}", headers={"X-Demo-Role": "auditor"}
        )

    assert response.status_code == 200
    assert body["data_classification"] == "synthetic"
    assert all(item["status"] == "open" for item in body["items"])
    assert detail.json()["synthetic_trade_id"].startswith("TRD-DEMO-")
    assert response.headers["x-content-type-options"] == "nosniff"
    assert response.headers["cache-control"] == "no-store"


def test_workflow_and_approval_are_idempotent_and_audited() -> None:
    with _client() as client:
        queue = client.get("/api/v1/exceptions").json()["items"]
        exception = next(item for item in queue if item["status"] == "open")
        start_headers = {"X-Demo-Role": "analyst", "Idempotency-Key": "start-key-0001"}
        first = client.post(
            f"/api/v1/exceptions/{exception['id']}/workflows", headers=start_headers
        )
        replay = client.post(
            f"/api/v1/exceptions/{exception['id']}/workflows", headers=start_headers
        )
        workflow = first.json()
        approval_headers = {"X-Demo-Role": "reviewer", "Idempotency-Key": "approve-key-0001"}
        approved = client.post(
            f"/api/v1/workflows/{workflow['id']}/approvals",
            headers=approval_headers,
            json={"decision": "approve", "expected_exception_version": exception["version"]},
        )
        approval_replay = client.post(
            f"/api/v1/workflows/{workflow['id']}/approvals",
            headers=approval_headers,
            json={"decision": "approve", "expected_exception_version": exception["version"]},
        )
        audit = client.get("/api/v1/audit-events", headers={"X-Demo-Role": "auditor"})

    assert first.status_code == 202
    assert first.json()["id"] == replay.json()["id"]
    assert approved.json()["status"] == "resolved"
    assert approved.json() == approval_replay.json()
    assert {event["event_type"] for event in audit.json()} == {
        "workflow.started.v1",
        "workflow.resumed.v1",
        "resolution.applied.v1",
    }


def test_negative_authorization_and_stale_version_conflict() -> None:
    with _client() as client:
        exception = next(
            item
            for item in client.get("/api/v1/exceptions").json()["items"]
            if item["status"] == "open"
        )
        denied_start = client.post(
            f"/api/v1/exceptions/{exception['id']}/workflows",
            headers={"X-Demo-Role": "auditor", "Idempotency-Key": "denied-start"},
        )
        workflow = client.post(
            f"/api/v1/exceptions/{exception['id']}/workflows",
            headers={"X-Demo-Role": "analyst", "Idempotency-Key": "allowed-start"},
        ).json()
        denied_approval = client.post(
            f"/api/v1/workflows/{workflow['id']}/approvals",
            headers={"X-Demo-Role": "analyst", "Idempotency-Key": "denied-approval"},
            json={"decision": "approve", "expected_exception_version": 1},
        )
        stale = client.post(
            f"/api/v1/workflows/{workflow['id']}/approvals",
            headers={"X-Demo-Role": "reviewer", "Idempotency-Key": "stale-approval"},
            json={"decision": "approve", "expected_exception_version": 99},
        )
        denied_audit = client.get("/api/v1/audit-events", headers={"X-Demo-Role": "analyst"})

    assert denied_start.status_code == 403
    assert denied_approval.status_code == 403
    assert denied_audit.status_code == 403
    assert stale.status_code == 409
    assert stale.headers["content-type"].startswith("application/problem+json")


def test_identity_not_found_validation_and_production_authentication() -> None:
    with _client() as client:
        user = client.get("/api/v1/session/me", headers={"X-Demo-Role": "reviewer"})
        invalid = client.get("/api/v1/session/me", headers={"X-Demo-Role": "owner"})
        missing = client.get("/api/v1/exceptions/00000000-0000-0000-0000-000000000000")
        invalid_post = client.post(
            "/api/v1/exceptions/00000000-0000-0000-0000-000000000000/workflows",
            headers={"Idempotency-Key": "short"},
        )
    with TestClient(create_app(Settings(environment="production", demo_dataset_size=24))) as client:
        production = client.get("/api/v1/session/me")

    assert user.json()["mode"] == "synthetic_demo"
    assert invalid.status_code == 401
    assert missing.status_code == 404
    assert invalid_post.status_code == 422
    assert production.status_code == 401


def test_openapi_contains_versioned_operations_contracts() -> None:
    with _client() as client:
        schema = client.get("/openapi.json").json()

    assert "/api/v1/exceptions" in schema["paths"]
    assert "/api/v1/workflows/{workflow_id}/approvals" in schema["paths"]
    assert schema["info"]["title"] == "TradeOps Copilot API"


def test_websocket_snapshot_and_polling_fallback() -> None:
    with _client() as client:
        polled = client.get("/api/v1/events", headers={"X-Demo-Role": "analyst"})
        with client.websocket_connect("/api/v1/events/ws?role=analyst") as socket:
            snapshot = socket.receive_json()

    assert polled.status_code == 200
    assert snapshot["type"] == "queue.snapshot.v1"
    assert snapshot["events"] == []
