"""Validated process configuration with safe local defaults."""

from functools import lru_cache
from typing import Literal

from pydantic import Field, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Environment-backed settings shared by API and worker composition roots."""

    model_config = SettingsConfigDict(env_prefix="TRADEOPS_", extra="forbid", frozen=True)

    app_name: str = "TradeOps Copilot API"
    environment: Literal["local", "test", "production"] = "local"
    api_prefix: str = Field(default="/api/v1", pattern=r"^/[a-z0-9/-]+$")
    database_url: SecretStr = SecretStr(
        "postgresql+psycopg://tradeops:tradeops-local-only@127.0.0.1:5432/tradeops"
    )
    worker_broker_url: SecretStr = SecretStr("redis://127.0.0.1:6379/0")
    worker_result_backend_url: SecretStr = SecretStr("redis://127.0.0.1:6379/1")
    otel_exporter_endpoint: str = "http://127.0.0.1:4317"
    oidc_issuer: str = "http://127.0.0.1:8080/realms/tradeops"
    demo_dataset_size: int = Field(default=120, ge=24, le=5000)


@lru_cache
def get_settings() -> Settings:
    """Build and cache immutable process settings."""

    return Settings()
