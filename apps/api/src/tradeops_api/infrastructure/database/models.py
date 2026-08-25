"""Core PostgreSQL-oriented persistence models."""

from datetime import date, datetime
from decimal import Decimal
from typing import Any
from uuid import UUID, uuid4

from sqlalchemy import (
    JSON,
    Boolean,
    CheckConstraint,
    Column,
    Date,
    DateTime,
    ForeignKey,
    Index,
    Integer,
    Numeric,
    String,
    Table,
    Text,
    UniqueConstraint,
)
from sqlalchemy.orm import Mapped, mapped_column

from tradeops_api.infrastructure.database.base import Base, TimestampMixin, UUIDPrimaryKeyMixin

user_roles = Table(
    "user_roles",
    Base.metadata,
    Column("user_id", ForeignKey("users.id", ondelete="CASCADE"), primary_key=True),
    Column("role_id", ForeignKey("roles.id", ondelete="CASCADE"), primary_key=True),
)


class UserModel(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    """OIDC subject mapped to application roles."""

    __tablename__ = "users"

    issuer: Mapped[str] = mapped_column(String(500), nullable=False)
    subject: Mapped[str] = mapped_column(String(255), nullable=False)
    display_name: Mapped[str] = mapped_column(String(200), nullable=False)
    email: Mapped[str | None] = mapped_column(String(320))
    active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    __table_args__ = (UniqueConstraint("issuer", "subject", name="uq_users_issuer_subject"),)


class RoleModel(UUIDPrimaryKeyMixin, Base):
    """Stable application role, independent of provider claim names."""

    __tablename__ = "roles"

    name: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    description: Mapped[str] = mapped_column(String(500), nullable=False)


class CounterpartyModel(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    """Versioned legal-entity reference record."""

    __tablename__ = "counterparties"

    lei: Mapped[str | None] = mapped_column(String(20), unique=True)
    legal_name: Mapped[str] = mapped_column(String(200), nullable=False)
    status: Mapped[str] = mapped_column(String(30), nullable=False)
    source_id: Mapped[str] = mapped_column(String(64), nullable=False)
    source_version: Mapped[str] = mapped_column(String(100), nullable=False)
    retrieved_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    version: Mapped[int] = mapped_column(Integer, default=1, nullable=False)

    __table_args__ = (
        CheckConstraint("version >= 1", name="version_positive"),
        Index("ix_counterparties_status_legal_name", "status", "legal_name"),
    )


class IssuerModel(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    """Optional issuer reference linked to a legal entity."""

    __tablename__ = "issuers"

    legal_name: Mapped[str] = mapped_column(String(200), nullable=False)
    lei: Mapped[str | None] = mapped_column(String(20))
    cik: Mapped[str | None] = mapped_column(String(10))
    source_id: Mapped[str] = mapped_column(String(64), nullable=False)
    source_version: Mapped[str] = mapped_column(String(100), nullable=False)

    __table_args__ = (UniqueConstraint("source_id", "source_version", name="uq_issuers_source"),)


class InstrumentModel(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    """Synthetic instrument; never a licensed security identifier."""

    __tablename__ = "instruments"

    instrument_id: Mapped[str] = mapped_column(String(30), unique=True, nullable=False)
    issuer_id: Mapped[UUID | None] = mapped_column(ForeignKey("issuers.id", ondelete="SET NULL"))
    product_type: Mapped[str] = mapped_column(String(50), nullable=False)
    currency: Mapped[str] = mapped_column(String(3), nullable=False)
    source_id: Mapped[str] = mapped_column(String(64), nullable=False)
    source_version: Mapped[str] = mapped_column(String(100), nullable=False)
    retrieved_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)

    __table_args__ = (
        CheckConstraint("instrument_id LIKE 'INST-DEMO-%'", name="demo_identifier"),
        CheckConstraint("char_length(currency) = 3", name="currency_length"),
    )


class TradeModel(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    """Synthetic trade aggregate identity and concurrency version."""

    __tablename__ = "trades"

    trade_id: Mapped[str] = mapped_column(String(30), unique=True, nullable=False)
    latest_version: Mapped[int] = mapped_column(Integer, default=1, nullable=False)
    status: Mapped[str] = mapped_column(String(30), default="open", nullable=False)

    __table_args__ = (
        CheckConstraint("trade_id LIKE 'TRD-DEMO-%'", name="demo_identifier"),
        CheckConstraint("latest_version >= 1", name="latest_version_positive"),
    )


class TradeEventModel(UUIDPrimaryKeyMixin, Base):
    """Immutable imported/generated event with idempotency key."""

    __tablename__ = "trade_events"

    trade_id: Mapped[UUID] = mapped_column(ForeignKey("trades.id", ondelete="CASCADE"))
    event_id: Mapped[str] = mapped_column(String(30), unique=True, nullable=False)
    event_type: Mapped[str] = mapped_column(String(50), nullable=False)
    idempotency_key: Mapped[str] = mapped_column(String(200), unique=True, nullable=False)
    payload: Mapped[dict[str, Any]] = mapped_column(JSON, nullable=False)
    occurred_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    received_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)

    __table_args__ = (CheckConstraint("event_id LIKE 'EVT-DEMO-%'", name="demo_identifier"),)


class TradeVersionModel(UUIDPrimaryKeyMixin, Base):
    """Immutable normalized values for one aggregate version."""

    __tablename__ = "trade_versions"

    trade_id: Mapped[UUID] = mapped_column(ForeignKey("trades.id", ondelete="CASCADE"))
    source_event_id: Mapped[UUID] = mapped_column(ForeignKey("trade_events.id"))
    version: Mapped[int] = mapped_column(Integer, nullable=False)
    counterparty_id: Mapped[UUID | None] = mapped_column(ForeignKey("counterparties.id"))
    counterparty_lei: Mapped[str | None] = mapped_column(String(64))
    counterparty_name: Mapped[str] = mapped_column(String(200), nullable=False)
    instrument_id: Mapped[UUID | None] = mapped_column(ForeignKey("instruments.id"))
    synthetic_instrument_id: Mapped[str] = mapped_column(String(30), nullable=False)
    product_type: Mapped[str] = mapped_column(String(100), nullable=False)
    side: Mapped[str] = mapped_column(String(10), nullable=False)
    currency: Mapped[str] = mapped_column(String(8), nullable=False)
    quantity: Mapped[Decimal] = mapped_column(Numeric(28, 8), nullable=False)
    notional: Mapped[Decimal] = mapped_column(Numeric(28, 8), nullable=False)
    price: Mapped[Decimal] = mapped_column(Numeric(20, 8), nullable=False)
    trade_date: Mapped[date] = mapped_column(Date, nullable=False)
    settlement_date: Mapped[date] = mapped_column(Date, nullable=False)
    confirmation_received: Mapped[bool] = mapped_column(Boolean, nullable=False)
    memo: Mapped[str | None] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)

    __table_args__ = (
        UniqueConstraint("trade_id", "version", name="uq_trade_versions_trade_version"),
        CheckConstraint("version >= 1", name="version_positive"),
        CheckConstraint("quantity > 0", name="quantity_positive"),
        CheckConstraint("notional > 0", name="notional_positive"),
        CheckConstraint("price > 0", name="price_positive"),
        CheckConstraint("settlement_date >= trade_date", name="settlement_not_before_trade"),
    )


class ExceptionModel(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    """Mutable case record with optimistic concurrency version."""

    __tablename__ = "exceptions"

    trade_id: Mapped[UUID] = mapped_column(ForeignKey("trades.id", ondelete="CASCADE"))
    trade_version: Mapped[int] = mapped_column(Integer, nullable=False)
    exception_type: Mapped[str] = mapped_column(String(80), nullable=False)
    severity: Mapped[str] = mapped_column(String(20), nullable=False)
    risk: Mapped[str] = mapped_column(String(20), nullable=False)
    status: Mapped[str] = mapped_column(String(30), default="open", nullable=False)
    explanation: Mapped[str] = mapped_column(Text, nullable=False)
    suggested_actions: Mapped[list[str]] = mapped_column(JSON, nullable=False)
    version: Mapped[int] = mapped_column(Integer, default=1, nullable=False)

    __table_args__ = (
        CheckConstraint("trade_version >= 1", name="trade_version_positive"),
        CheckConstraint("version >= 1", name="version_positive"),
        Index("ix_exceptions_queue", "status", "severity", "created_at", "id"),
    )


class ExceptionEvidenceModel(UUIDPrimaryKeyMixin, Base):
    """Bounded evidence attached to an exception."""

    __tablename__ = "exception_evidence"

    exception_id: Mapped[UUID] = mapped_column(ForeignKey("exceptions.id", ondelete="CASCADE"))
    evidence_type: Mapped[str] = mapped_column(String(50), nullable=False)
    code: Mapped[str] = mapped_column(String(100), nullable=False)
    summary: Mapped[str] = mapped_column(String(1000), nullable=False)
    facts: Mapped[dict[str, Any]] = mapped_column(JSON, nullable=False)
    source_id: Mapped[str | None] = mapped_column(String(64))
    source_locator: Mapped[str | None] = mapped_column(String(2000))
    content_sha256: Mapped[str | None] = mapped_column(String(64))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)


class AuditEventModel(UUIDPrimaryKeyMixin, Base):
    """Append-only application audit event."""

    __tablename__ = "audit_events"

    actor_user_id: Mapped[UUID | None] = mapped_column(ForeignKey("users.id", ondelete="SET NULL"))
    action: Mapped[str] = mapped_column(String(100), nullable=False)
    resource_type: Mapped[str] = mapped_column(String(100), nullable=False)
    resource_id: Mapped[str] = mapped_column(String(100), nullable=False)
    correlation_id: Mapped[str] = mapped_column(String(128), nullable=False)
    payload: Mapped[dict[str, Any]] = mapped_column(JSON, nullable=False)
    occurred_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)

    __table_args__ = (
        Index("ix_audit_events_search", "resource_type", "resource_id", "occurred_at"),
    )


class OutboxMessageModel(UUIDPrimaryKeyMixin, Base):
    """Transactional publication intent leased by the worker."""

    __tablename__ = "outbox_messages"

    event_id: Mapped[UUID] = mapped_column(unique=True, nullable=False, default=uuid4)
    aggregate_type: Mapped[str] = mapped_column(String(100), nullable=False)
    aggregate_id: Mapped[str] = mapped_column(String(100), nullable=False)
    schema_name: Mapped[str] = mapped_column(String(100), nullable=False)
    schema_version: Mapped[int] = mapped_column(Integer, nullable=False)
    correlation_id: Mapped[str] = mapped_column(String(128), nullable=False)
    payload: Mapped[dict[str, Any]] = mapped_column(JSON, nullable=False)
    occurred_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    available_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    dispatched_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    attempts: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    last_error_code: Mapped[str | None] = mapped_column(String(100))

    __table_args__ = (
        CheckConstraint("schema_version >= 1", name="schema_version_positive"),
        CheckConstraint("attempts >= 0", name="attempts_nonnegative"),
        Index("ix_outbox_dispatch", "dispatched_at", "available_at", "id"),
    )


class IdempotencyRecordModel(UUIDPrimaryKeyMixin, Base):
    """Recorded command outcome bound to a request digest."""

    __tablename__ = "idempotency_records"

    scope: Mapped[str] = mapped_column(String(100), nullable=False)
    key: Mapped[str] = mapped_column(String(200), nullable=False)
    request_sha256: Mapped[str] = mapped_column(String(64), nullable=False)
    response_status: Mapped[int] = mapped_column(Integer, nullable=False)
    response_body: Mapped[dict[str, Any]] = mapped_column(JSON, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)

    __table_args__ = (
        UniqueConstraint("scope", "key", name="uq_idempotency_scope_key"),
        CheckConstraint(
            "response_status >= 100 AND response_status <= 599",
            name="response_status_valid",
        ),
    )
