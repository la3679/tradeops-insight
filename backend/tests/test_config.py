import pytest
from pydantic import ValidationError

from tradeops.config import Settings


def test_settings_accept_prefixed_environment_overrides(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("TRADEOPS_ENVIRONMENT", "test")
    monkeypatch.setenv("TRADEOPS_API_PREFIX", "/api/v2")

    settings = Settings()

    assert settings.environment == "test"
    assert settings.api_prefix == "/api/v2"


def test_settings_reject_invalid_api_prefix() -> None:
    with pytest.raises(ValidationError):
        Settings(api_prefix="api/v1")
