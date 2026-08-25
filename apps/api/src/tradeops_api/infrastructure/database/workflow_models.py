"""Knowledge, workflow, approval, tool, evaluation, and source-sync persistence."""

from datetime import date, datetime
from decimal import Decimal
from typing import Any
from uuid import UUID

from sqlalchemy import (
    JSON,
    Boolean,
    CheckConstraint,
    Date,
    DateTime,
    ForeignKey,
    Index,
    Integer,
    Numeric,
    String,
    Text,
    UniqueConstraint,
)
from sqlalchemy.orm import Mapped, mapped_column

from tradeops_api.infrastructure.database.base import Base, TimestampMixin, UUIDPrimaryKeyMixin


class DocumentModel(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "documents"

    document_id: Mapped[str] = mapped_column(String(100), nullable=False)
    version: Mapped[str] = mapped_column(String(100), nullable=False)
    title: Mapped[str] = mapped_column(String(500), nullable=False)
    document_type: Mapped[str] = mapped_column(String(50), nullable=False)
    jurisdiction: Mapped[str | None] = mapped_column(String(100))
    effective_date: Mapped[date | None] = mapped_column(Date)
    source_id: Mapped[str] = mapped_column(String(64), nullable=False)
    source_locator: Mapped[str] = mapped_column(String(2000), nullable=False)
    content_sha256: Mapped[str] = mapped_column(String(64), nullable=False)
    status: Mapped[str] = mapped_column(String(30), default="registered", nullable=False)

    __table_args__ = (UniqueConstraint("document_id", "version", name="uq_documents_id_version"),)


class DocumentChunkModel(UUIDPrimaryKeyMixin, Base):
    __tablename__ = "document_chunks"

    document_id: Mapped[UUID] = mapped_column(ForeignKey("documents.id", ondelete="CASCADE"))
    chunk_id: Mapped[str] = mapped_column(String(150), unique=True, nullable=False)
    ordinal: Mapped[int] = mapped_column(Integer, nullable=False)
    section: Mapped[str | None] = mapped_column(String(500))
    content: Mapped[str] = mapped_column(Text, nullable=False)
    content_sha256: Mapped[str] = mapped_column(String(64), nullable=False)
    token_count: Mapped[int] = mapped_column(Integer, nullable=False)
    metadata_json: Mapped[dict[str, Any]] = mapped_column(JSON, nullable=False)

    __table_args__ = (
        UniqueConstraint("document_id", "ordinal", name="uq_document_chunks_ordinal"),
        CheckConstraint("ordinal >= 0", name="ordinal_nonnegative"),
        CheckConstraint("token_count > 0", name="token_count_positive"),
    )


class WorkflowRunModel(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "workflow_runs"

    workflow_id: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    exception_id: Mapped[UUID] = mapped_column(ForeignKey("exceptions.id", ondelete="CASCADE"))
    graph_version: Mapped[str] = mapped_column(String(100), nullable=False)
    prompt_version: Mapped[str] = mapped_column(String(100), nullable=False)
    provider: Mapped[str] = mapped_column(String(50), nullable=False)
    model: Mapped[str] = mapped_column(String(200), nullable=False)
    status: Mapped[str] = mapped_column(String(30), nullable=False)
    thread_id: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    state_version: Mapped[int] = mapped_column(Integer, default=1, nullable=False)
    started_by_user_id: Mapped[UUID | None] = mapped_column(ForeignKey("users.id"))
    completed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))

    __table_args__ = (
        CheckConstraint("state_version >= 1", name="state_version_positive"),
        Index("ix_workflow_runs_exception_created", "exception_id", "created_at"),
    )


class WorkflowStepModel(UUIDPrimaryKeyMixin, Base):
    __tablename__ = "workflow_steps"

    workflow_run_id: Mapped[UUID] = mapped_column(
        ForeignKey("workflow_runs.id", ondelete="CASCADE")
    )
    node_name: Mapped[str] = mapped_column(String(100), nullable=False)
    attempt: Mapped[int] = mapped_column(Integer, nullable=False)
    status: Mapped[str] = mapped_column(String(30), nullable=False)
    input_sha256: Mapped[str] = mapped_column(String(64), nullable=False)
    output_metadata: Mapped[dict[str, Any]] = mapped_column(JSON, nullable=False)
    error_code: Mapped[str | None] = mapped_column(String(100))
    started_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    completed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))

    __table_args__ = (
        UniqueConstraint(
            "workflow_run_id", "node_name", "attempt", name="uq_workflow_steps_attempt"
        ),
        CheckConstraint("attempt >= 1", name="attempt_positive"),
    )


class ToolCallModel(UUIDPrimaryKeyMixin, Base):
    __tablename__ = "tool_calls"

    workflow_step_id: Mapped[UUID] = mapped_column(
        ForeignKey("workflow_steps.id", ondelete="CASCADE")
    )
    tool_name: Mapped[str] = mapped_column(String(100), nullable=False)
    authorization_decision_id: Mapped[str] = mapped_column(String(100), nullable=False)
    idempotency_key: Mapped[str | None] = mapped_column(String(200))
    input_sha256: Mapped[str] = mapped_column(String(64), nullable=False)
    output_metadata: Mapped[dict[str, Any]] = mapped_column(JSON, nullable=False)
    status: Mapped[str] = mapped_column(String(30), nullable=False)
    latency_ms: Mapped[int] = mapped_column(Integer, nullable=False)
    error_code: Mapped[str | None] = mapped_column(String(100))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)

    __table_args__ = (CheckConstraint("latency_ms >= 0", name="latency_nonnegative"),)


class ApprovalModel(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "approvals"

    workflow_run_id: Mapped[UUID] = mapped_column(ForeignKey("workflow_runs.id"))
    exception_id: Mapped[UUID] = mapped_column(ForeignKey("exceptions.id"))
    reviewer_user_id: Mapped[UUID] = mapped_column(ForeignKey("users.id"))
    decision: Mapped[str] = mapped_column(String(30), nullable=False)
    reason: Mapped[str] = mapped_column(String(2000), nullable=False)
    proposal_version: Mapped[int] = mapped_column(Integer, nullable=False)
    exception_version: Mapped[int] = mapped_column(Integer, nullable=False)
    evidence_sha256: Mapped[str] = mapped_column(String(64), nullable=False)
    idempotency_key: Mapped[str] = mapped_column(String(200), unique=True, nullable=False)
    used_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)

    __table_args__ = (
        CheckConstraint("proposal_version >= 1", name="proposal_version_positive"),
        CheckConstraint("exception_version >= 1", name="exception_version_positive"),
    )


class ResolutionActionModel(UUIDPrimaryKeyMixin, Base):
    __tablename__ = "resolution_actions"

    exception_id: Mapped[UUID] = mapped_column(ForeignKey("exceptions.id"))
    workflow_run_id: Mapped[UUID] = mapped_column(ForeignKey("workflow_runs.id"))
    approval_id: Mapped[UUID | None] = mapped_column(ForeignKey("approvals.id"))
    action_type: Mapped[str] = mapped_column(String(100), nullable=False)
    target_field: Mapped[str] = mapped_column(String(100), nullable=False)
    before_value: Mapped[dict[str, Any]] = mapped_column(JSON, nullable=False)
    after_value: Mapped[dict[str, Any]] = mapped_column(JSON, nullable=False)
    idempotency_key: Mapped[str] = mapped_column(String(200), unique=True, nullable=False)
    status: Mapped[str] = mapped_column(String(30), nullable=False)
    applied_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)


class EvaluationCaseModel(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "evaluation_cases"

    case_id: Mapped[str] = mapped_column(String(100), nullable=False)
    version: Mapped[str] = mapped_column(String(100), nullable=False)
    category: Mapped[str] = mapped_column(String(100), nullable=False)
    input_payload: Mapped[dict[str, Any]] = mapped_column(JSON, nullable=False)
    expected_payload: Mapped[dict[str, Any]] = mapped_column(JSON, nullable=False)
    tags: Mapped[list[str]] = mapped_column(JSON, nullable=False)

    __table_args__ = (UniqueConstraint("case_id", "version", name="uq_evaluation_cases_version"),)


class EvaluationRunModel(UUIDPrimaryKeyMixin, Base):
    __tablename__ = "evaluation_runs"

    dataset_version: Mapped[str] = mapped_column(String(100), nullable=False)
    graph_version: Mapped[str] = mapped_column(String(100), nullable=False)
    provider: Mapped[str] = mapped_column(String(50), nullable=False)
    model: Mapped[str] = mapped_column(String(200), nullable=False)
    config_sha256: Mapped[str] = mapped_column(String(64), nullable=False)
    status: Mapped[str] = mapped_column(String(30), nullable=False)
    started_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    completed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))


class EvaluationResultModel(UUIDPrimaryKeyMixin, Base):
    __tablename__ = "evaluation_results"

    evaluation_run_id: Mapped[UUID] = mapped_column(
        ForeignKey("evaluation_runs.id", ondelete="CASCADE")
    )
    evaluation_case_id: Mapped[UUID] = mapped_column(ForeignKey("evaluation_cases.id"))
    passed: Mapped[bool] = mapped_column(Boolean, nullable=False)
    score: Mapped[Decimal | None] = mapped_column(Numeric(8, 6))
    metrics: Mapped[dict[str, Any]] = mapped_column(JSON, nullable=False)
    output_metadata: Mapped[dict[str, Any]] = mapped_column(JSON, nullable=False)
    latency_ms: Mapped[int] = mapped_column(Integer, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)

    __table_args__ = (
        UniqueConstraint(
            "evaluation_run_id", "evaluation_case_id", name="uq_evaluation_result_case"
        ),
        CheckConstraint("score IS NULL OR (score >= 0 AND score <= 1)", name="score_bounded"),
        CheckConstraint("latency_ms >= 0", name="latency_nonnegative"),
    )


class DataSourceSyncRunModel(UUIDPrimaryKeyMixin, Base):
    __tablename__ = "data_source_sync_runs"

    source_id: Mapped[str] = mapped_column(String(64), nullable=False)
    requested_by_user_id: Mapped[UUID | None] = mapped_column(ForeignKey("users.id"))
    status: Mapped[str] = mapped_column(String(30), nullable=False)
    cursor: Mapped[str | None] = mapped_column(String(1000))
    fetched_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    changed_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    error_code: Mapped[str | None] = mapped_column(String(100))
    started_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    completed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))

    __table_args__ = (
        CheckConstraint("fetched_count >= 0", name="fetched_nonnegative"),
        CheckConstraint("changed_count >= 0", name="changed_nonnegative"),
    )
