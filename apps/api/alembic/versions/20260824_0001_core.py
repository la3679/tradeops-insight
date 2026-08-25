"""Create core identity, reference, trade, exception, audit, and delivery tables.

Revision ID: 20260824_0001
Revises: None
"""

from collections.abc import Sequence

from alembic import op

revision: str = "20260824_0001"
down_revision: str | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Create the initial authoritative data model."""

    # Keep migration definitions bound to the reviewed metadata revision.
    from tradeops_api.infrastructure.database import Base

    bind = op.get_bind()
    tables = [
        Base.metadata.tables[name]
        for name in (
            "users",
            "roles",
            "user_roles",
            "counterparties",
            "issuers",
            "instruments",
            "trades",
            "trade_events",
            "trade_versions",
            "exceptions",
            "exception_evidence",
            "audit_events",
            "outbox_messages",
            "idempotency_records",
        )
    ]
    Base.metadata.create_all(bind=bind, tables=tables)


def downgrade() -> None:
    """Drop initial tables in dependency-safe metadata order."""

    from tradeops_api.infrastructure.database import Base

    bind = op.get_bind()
    tables = [
        Base.metadata.tables[name]
        for name in (
            "idempotency_records",
            "outbox_messages",
            "audit_events",
            "exception_evidence",
            "exceptions",
            "trade_versions",
            "trade_events",
            "trades",
            "instruments",
            "issuers",
            "counterparties",
            "user_roles",
            "roles",
            "users",
        )
    ]
    Base.metadata.drop_all(bind=bind, tables=tables)
