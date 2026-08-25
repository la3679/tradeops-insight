"""Authentication and authorization boundary tests."""

from collections.abc import Mapping

import pytest
from fastapi.testclient import TestClient

from tradeops.api.app import create_app
from tradeops.config import Settings


class FakeDecoder:
    def __init__(self, claims: Mapping[str, object]) -> None:
        self._claims = dict(claims)

    def decode(self, token: str) -> dict[str, object]:
        assert token == "signed-token"
        return self._claims


@pytest.fixture
def production_client() -> TestClient:
    app = create_app(Settings(environment="production"))
    app.state.token_decoder = FakeDecoder(
        {
            "sub": "oidc-user-1",
            "name": "Synthetic Reviewer",
            "realm_access": {"roles": ["reviewer"]},
        }
    )
    return TestClient(app)


def test_production_requires_bearer_token(production_client: TestClient) -> None:
    response = production_client.get("/api/v1/session/me")

    assert response.status_code == 401
    assert response.headers["www-authenticate"] == "Bearer"


def test_validated_claims_create_principal(production_client: TestClient) -> None:
    response = production_client.get(
        "/api/v1/session/me", headers={"Authorization": "Bearer signed-token"}
    )

    assert response.status_code == 200
    assert response.json() == {
        "subject": "oidc-user-1",
        "display_name": "Synthetic Reviewer",
        "role": "reviewer",
        "mode": "synthetic_demo",
    }


def test_token_without_application_role_is_denied(production_client: TestClient) -> None:
    del production_client
    app = create_app(Settings(environment="production"))
    app.state.token_decoder = FakeDecoder(
        {"sub": "oidc-user-2", "preferred_username": "roleless", "realm_access": {"roles": []}}
    )
    client = TestClient(app)

    response = client.get("/api/v1/session/me", headers={"Authorization": "Bearer signed-token"})

    assert response.status_code == 403
