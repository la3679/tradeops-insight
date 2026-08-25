"""Create knowledge, workflow, approval, evaluation, and source-sync tables.

Revision ID: 20260824_0002
Revises: 20260824_0001
"""

from collections.abc import Sequence

from alembic import op

revision: str = "20260824_0002"
down_revision: str | None = "20260824_0001"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

TABLES = (
    "documents",
    "document_chunks",
    "workflow_runs",
    "workflow_steps",
    "tool_calls",
    "approvals",
    "resolution_actions",
    "evaluation_cases",
    "evaluation_runs",
    "evaluation_results",
    "data_source_sync_runs",
)


def upgrade() -> None:
    """Create governed workflow and evaluation storage."""

    from tradeops_api.infrastructure.database import Base

    Base.metadata.create_all(
        bind=op.get_bind(), tables=[Base.metadata.tables[name] for name in TABLES]
    )


def downgrade() -> None:
    """Drop governed workflow and evaluation storage."""

    from tradeops_api.infrastructure.database import Base

    Base.metadata.drop_all(
        bind=op.get_bind(),
        tables=[Base.metadata.tables[name] for name in reversed(TABLES)],
    )
