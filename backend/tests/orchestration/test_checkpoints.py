"""Durable-checkpoint configuration tests."""

import pytest
from pydantic import SecretStr

from tradeops.config import Settings
from tradeops.orchestration.checkpoints import checkpoint_connection_string


def test_checkpoint_url_uses_psycopg_compatible_scheme() -> None:
    settings = Settings(
        database_url=SecretStr("postgresql+psycopg://user:password@database:5432/tradeops")
    )

    assert (
        checkpoint_connection_string(settings)
        == "postgresql://user:password@database:5432/tradeops"
    )


def test_checkpoint_url_rejects_non_postgresql_database() -> None:
    with pytest.raises(ValueError, match="PostgreSQL checkpoints"):
        checkpoint_connection_string(
            Settings(database_url=SecretStr("sqlite+pysqlite:///:memory:"))
        )
