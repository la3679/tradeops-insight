"""Validated process configuration with safe local defaults."""

from functools import lru_cache
from typing import Literal

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Environment-backed settings shared by API and worker composition roots."""

    model_config = SettingsConfigDict(env_prefix="TRADEOPS_", extra="forbid", frozen=True)

    app_name: str = "TradeOps Copilot API"
    environment: Literal["local", "test", "production"] = "local"
    api_prefix: str = Field(default="/api/v1", pattern=r"^/[a-z0-9/-]+$")
    worker_broker_url: str = "redis://127.0.0.1:6379/0"
    worker_result_backend_url: str = "redis://127.0.0.1:6379/1"


@lru_cache
def get_settings() -> Settings:
    """Build and cache immutable process settings."""

    return Settings()
