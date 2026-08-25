"""Persistence infrastructure unit tests."""

from pydantic import SecretStr
from sqlalchemy import Engine

from tradeops.adapters.persistence.session import create_engine, create_session_factory
from tradeops.config import Settings


def test_create_engine_uses_configured_database_url() -> None:
    settings = Settings(database_url=SecretStr("sqlite+pysqlite:///:memory:"))

    engine = create_engine(settings)

    assert isinstance(engine, Engine)
    assert str(engine.url) == "sqlite+pysqlite:///:memory:"


def test_session_factory_binds_engine_without_expiring_objects() -> None:
    engine = create_engine(Settings(database_url=SecretStr("sqlite+pysqlite:///:memory:")))

    factory = create_session_factory(engine)

    assert factory.kw["bind"] is engine
    assert factory.kw["expire_on_commit"] is False
