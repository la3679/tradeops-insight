"""Relational persistence model; domain behavior remains outside this module."""

from datetime import date, datetime
from decimal import Decimal
from uuid import UUID, uuid4

from sqlalchemy import (
    JSON,
    Boolean,
    Date,
    DateTime,
    ForeignKey,
    Index,
    Integer,
    Numeric,
    String,
    Text,
    UniqueConstraint,
    func,
)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    """Base metadata for the TradeOps schema."""


class IdentityMixin:
    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)


class TimestampMixin:
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False
    )


class UserRecord(IdentityMixin, TimestampMixin, Base):
    __tablename__ = "users"

    oidc_subject: Mapped[str] = mapped_column(String(255), unique=True)
    display_name: Mapped[str] = mapped_column(String(200))
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)


class RoleRecord(IdentityMixin, Base):
    __tablename__ = "roles"

    name: Mapped[str] = mapped_column(String(64), unique=True)


class UserRoleRecord(Base):
    __tablename__ = "user_roles"

    user_id: Mapped[UUID] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), primary_key=True
    )
    role_id: Mapped[UUID] = mapped_column(
        ForeignKey("roles.id", ondelete="CASCADE"), primary_key=True
    )


class CounterpartyRecord(IdentityMixin, TimestampMixin, Base):
    __tablename__ = "counterparties"

    synthetic_lei: Mapped[str] = mapped_column(String(32), unique=True)
    legal_name: Mapped[str] = mapped_column(String(255))
    status: Mapped[str] = mapped_column(String(32), index=True)
    reference_as_of: Mapped[datetime] = mapped_column(DateTime(timezone=True))


class IssuerRecord(IdentityMixin, TimestampMixin, Base):
    __tablename__ = "issuers"

    synthetic_issuer_id: Mapped[str] = mapped_column(String(32), unique=True)
    legal_name: Mapped[str] = mapped_column(String(255))


class InstrumentRecord(IdentityMixin, TimestampMixin, Base):
    __tablename__ = "instruments"

    synthetic_instrument_id: Mapped[str] = mapped_column(String(32), unique=True)
    issuer_id: Mapped[UUID | None] = mapped_column(ForeignKey("issuers.id"), index=True)
    product_type: Mapped[str] = mapped_column(String(64), index=True)
    currency: Mapped[str] = mapped_column(String(3))
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    reference_as_of: Mapped[datetime] = mapped_column(DateTime(timezone=True))


class TradeRecord(IdentityMixin, TimestampMixin, Base):
    __tablename__ = "trades"

    synthetic_trade_id: Mapped[str] = mapped_column(String(32), unique=True)
    current_version: Mapped[int] = mapped_column(Integer, default=1)


class TradeVersionRecord(IdentityMixin, Base):
    __tablename__ = "trade_versions"
    __table_args__ = (UniqueConstraint("trade_id", "version", name="uq_trade_version"),)

    trade_id: Mapped[UUID] = mapped_column(ForeignKey("trades.id", ondelete="CASCADE"), index=True)
    version: Mapped[int] = mapped_column(Integer)
    instrument_id: Mapped[UUID] = mapped_column(ForeignKey("instruments.id"), index=True)
    counterparty_id: Mapped[UUID] = mapped_column(ForeignKey("counterparties.id"), index=True)
    side: Mapped[str] = mapped_column(String(8))
    currency: Mapped[str] = mapped_column(String(3))
    notional: Mapped[Decimal] = mapped_column(Numeric(24, 6))
    price: Mapped[Decimal] = mapped_column(Numeric(18, 8))
    trade_date: Mapped[date] = mapped_column(Date)
    settlement_date: Mapped[date] = mapped_column(Date, index=True)
    memo: Mapped[str | None] = mapped_column(Text)
    observed_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))


class TradeEventRecord(IdentityMixin, Base):
    __tablename__ = "trade_events"

    trade_id: Mapped[UUID] = mapped_column(ForeignKey("trades.id", ondelete="CASCADE"), index=True)
    event_type: Mapped[str] = mapped_column(String(80), index=True)
    idempotency_key: Mapped[str] = mapped_column(String(160), unique=True)
    payload: Mapped[dict[str, object]] = mapped_column(JSON)
    occurred_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), index=True)


class ExceptionRecord(IdentityMixin, TimestampMixin, Base):
    __tablename__ = "exceptions"
    __table_args__ = (Index("ix_exceptions_queue", "status", "severity", "created_at"),)

    trade_id: Mapped[UUID] = mapped_column(ForeignKey("trades.id"), index=True)
    exception_type: Mapped[str] = mapped_column(String(80), index=True)
    severity: Mapped[str] = mapped_column(String(16), index=True)
    status: Mapped[str] = mapped_column(String(32), index=True)
    explanation: Mapped[str] = mapped_column(Text)
    rule_version: Mapped[str] = mapped_column(String(80))
    finding_key: Mapped[str] = mapped_column(String(255), unique=True)
    version: Mapped[int] = mapped_column(Integer, default=1)


class ExceptionEvidenceRecord(IdentityMixin, TimestampMixin, Base):
    __tablename__ = "exception_evidence"

    exception_id: Mapped[UUID] = mapped_column(
        ForeignKey("exceptions.id", ondelete="CASCADE"), index=True
    )
    source_type: Mapped[str] = mapped_column(String(64))
    source_reference: Mapped[str] = mapped_column(String(500))
    content: Mapped[dict[str, object]] = mapped_column(JSON)


class DocumentRecord(IdentityMixin, TimestampMixin, Base):
    __tablename__ = "documents"

    title: Mapped[str] = mapped_column(String(300))
    source_type: Mapped[str] = mapped_column(String(64), index=True)
    source_url: Mapped[str | None] = mapped_column(String(1000))
    license_name: Mapped[str | None] = mapped_column(String(200))
    content_sha256: Mapped[str] = mapped_column(String(64), unique=True)
    observed_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))


class DocumentChunkRecord(IdentityMixin, Base):
    __tablename__ = "document_chunks"
    __table_args__ = (UniqueConstraint("document_id", "ordinal", name="uq_document_chunk"),)

    document_id: Mapped[UUID] = mapped_column(
        ForeignKey("documents.id", ondelete="CASCADE"), index=True
    )
    ordinal: Mapped[int] = mapped_column(Integer)
    content: Mapped[str] = mapped_column(Text)
    token_count: Mapped[int] = mapped_column(Integer)
    metadata_json: Mapped[dict[str, object]] = mapped_column("metadata", JSON)


class WorkflowRunRecord(IdentityMixin, TimestampMixin, Base):
    __tablename__ = "workflow_runs"

    exception_id: Mapped[UUID] = mapped_column(ForeignKey("exceptions.id"), index=True)
    status: Mapped[str] = mapped_column(String(32), index=True)
    graph_version: Mapped[str] = mapped_column(String(80))
    idempotency_key: Mapped[str] = mapped_column(String(160), unique=True)
    state: Mapped[dict[str, object]] = mapped_column(JSON)


class WorkflowStepRecord(IdentityMixin, TimestampMixin, Base):
    __tablename__ = "workflow_steps"

    workflow_run_id: Mapped[UUID] = mapped_column(
        ForeignKey("workflow_runs.id", ondelete="CASCADE"), index=True
    )
    node_name: Mapped[str] = mapped_column(String(100))
    status: Mapped[str] = mapped_column(String(32))
    input_json: Mapped[dict[str, object]] = mapped_column(JSON)
    output_json: Mapped[dict[str, object]] = mapped_column(JSON)


class ToolCallRecord(IdentityMixin, TimestampMixin, Base):
    __tablename__ = "tool_calls"

    workflow_step_id: Mapped[UUID] = mapped_column(
        ForeignKey("workflow_steps.id", ondelete="CASCADE"), index=True
    )
    tool_name: Mapped[str] = mapped_column(String(100))
    status: Mapped[str] = mapped_column(String(32))
    arguments: Mapped[dict[str, object]] = mapped_column(JSON)
    result: Mapped[dict[str, object] | None] = mapped_column(JSON)


class ApprovalRecord(IdentityMixin, TimestampMixin, Base):
    __tablename__ = "approvals"

    exception_id: Mapped[UUID] = mapped_column(ForeignKey("exceptions.id"), index=True)
    reviewer_user_id: Mapped[UUID] = mapped_column(ForeignKey("users.id"), index=True)
    decision: Mapped[str] = mapped_column(String(32))
    rationale: Mapped[str] = mapped_column(Text)
    exception_version: Mapped[int] = mapped_column(Integer)
    idempotency_key: Mapped[str] = mapped_column(String(160), unique=True)


class ResolutionActionRecord(IdentityMixin, TimestampMixin, Base):
    __tablename__ = "resolution_actions"

    exception_id: Mapped[UUID] = mapped_column(ForeignKey("exceptions.id"), index=True)
    approval_id: Mapped[UUID] = mapped_column(ForeignKey("approvals.id"), unique=True)
    action_type: Mapped[str] = mapped_column(String(80))
    status: Mapped[str] = mapped_column(String(32))
    requested_changes: Mapped[dict[str, object]] = mapped_column(JSON)
    idempotency_key: Mapped[str] = mapped_column(String(160), unique=True)


class AuditEventRecord(IdentityMixin, Base):
    __tablename__ = "audit_events"

    event_type: Mapped[str] = mapped_column(String(100), index=True)
    actor_id: Mapped[UUID | None] = mapped_column(ForeignKey("users.id"), index=True)
    subject_type: Mapped[str] = mapped_column(String(80))
    subject_id: Mapped[UUID] = mapped_column(index=True)
    occurred_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), index=True)
    correlation_id: Mapped[UUID] = mapped_column(index=True)
    payload: Mapped[dict[str, object]] = mapped_column(JSON)


class OutboxEventRecord(IdentityMixin, Base):
    """Application event committed in the same transaction as domain state."""

    __tablename__ = "outbox_events"
    __table_args__ = (Index("ix_outbox_delivery", "published_at", "occurred_at"),)

    event_type: Mapped[str] = mapped_column(String(100), index=True)
    schema_version: Mapped[int] = mapped_column(Integer, default=1)
    aggregate_type: Mapped[str] = mapped_column(String(80))
    aggregate_id: Mapped[UUID] = mapped_column(index=True)
    payload: Mapped[dict[str, object]] = mapped_column(JSON)
    occurred_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), index=True)
    published_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    attempts: Mapped[int] = mapped_column(Integer, default=0)


class EvaluationCaseRecord(IdentityMixin, TimestampMixin, Base):
    __tablename__ = "evaluation_cases"

    name: Mapped[str] = mapped_column(String(200), unique=True)
    case_type: Mapped[str] = mapped_column(String(80), index=True)
    input_json: Mapped[dict[str, object]] = mapped_column(JSON)
    expected_json: Mapped[dict[str, object]] = mapped_column(JSON)


class EvaluationRunRecord(IdentityMixin, TimestampMixin, Base):
    __tablename__ = "evaluation_runs"

    status: Mapped[str] = mapped_column(String(32), index=True)
    configuration: Mapped[dict[str, object]] = mapped_column(JSON)


class EvaluationResultRecord(IdentityMixin, Base):
    __tablename__ = "evaluation_results"
    __table_args__ = (
        UniqueConstraint("evaluation_run_id", "evaluation_case_id", name="uq_evaluation_result"),
    )

    evaluation_run_id: Mapped[UUID] = mapped_column(
        ForeignKey("evaluation_runs.id", ondelete="CASCADE"), index=True
    )
    evaluation_case_id: Mapped[UUID] = mapped_column(ForeignKey("evaluation_cases.id"), index=True)
    passed: Mapped[bool] = mapped_column(Boolean)
    metrics: Mapped[dict[str, object]] = mapped_column(JSON)


class DataSourceSyncRunRecord(IdentityMixin, TimestampMixin, Base):
    __tablename__ = "data_source_sync_runs"

    source_name: Mapped[str] = mapped_column(String(120), index=True)
    status: Mapped[str] = mapped_column(String(32), index=True)
    source_url: Mapped[str] = mapped_column(String(1000))
    license_name: Mapped[str | None] = mapped_column(String(200))
    records_seen: Mapped[int] = mapped_column(Integer, default=0)
    provenance: Mapped[dict[str, object]] = mapped_column(JSON)
