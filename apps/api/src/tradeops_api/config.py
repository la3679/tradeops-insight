"""Typed process configuration."""

from functools import lru_cache
from typing import Literal

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Configuration read once at the application boundary."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        env_prefix="TRADEOPS_",
        extra="ignore",
        frozen=True,
    )

    app_name: str = "TradeOps Copilot API"
    environment: Literal["development", "test", "production"] = "development"
    api_v1_prefix: str = Field(default="/api/v1", pattern=r"^/[a-z0-9/]+$")


@lru_cache
def get_settings() -> Settings:
    """Return immutable process configuration."""

    return Settings()
