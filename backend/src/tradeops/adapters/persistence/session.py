"""Explicit SQLAlchemy engine and session construction."""

from sqlalchemy import Engine
from sqlalchemy import create_engine as sqlalchemy_create_engine
from sqlalchemy.orm import Session, sessionmaker

from tradeops.config import Settings, get_settings


def create_engine(settings: Settings | None = None) -> Engine:
    resolved = settings or get_settings()
    return sqlalchemy_create_engine(
        resolved.database_url.get_secret_value(),
        pool_pre_ping=True,
    )


def create_session_factory(engine: Engine) -> sessionmaker[Session]:
    return sessionmaker(bind=engine, expire_on_commit=False)
