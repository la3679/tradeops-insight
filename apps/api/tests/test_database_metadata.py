"""Persistence metadata and migration invariants."""

from decimal import Decimal
from typing import cast

from sqlalchemy import CheckConstraint, Numeric, UniqueConstraint

from tradeops_api.infrastructure.database import Base


def test_core_tables_are_registered() -> None:
    assert set(Base.metadata.tables) == {
        "audit_events",
        "counterparties",
        "exception_evidence",
        "exceptions",
        "idempotency_records",
        "instruments",
        "issuers",
        "outbox_messages",
        "roles",
        "trade_events",
        "trade_versions",
        "trades",
        "user_roles",
        "users",
    }


def test_trade_versions_enforce_precision_and_version_invariants() -> None:
    table = Base.metadata.tables["trade_versions"]
    check_names = {
        constraint.name
        for constraint in table.constraints
        if isinstance(constraint, CheckConstraint)
    }

    assert {
        "ck_trade_versions_notional_positive",
        "ck_trade_versions_price_positive",
        "ck_trade_versions_quantity_positive",
        "ck_trade_versions_settlement_not_before_trade",
        "ck_trade_versions_version_positive",
    } <= check_names
    quantity_type = cast(Numeric[Decimal], table.c.quantity.type)
    assert quantity_type.precision == 28
    assert quantity_type.scale == 8


def test_mutable_cases_and_commands_have_concurrency_keys() -> None:
    exceptions = Base.metadata.tables["exceptions"]
    idempotency = Base.metadata.tables["idempotency_records"]
    unique_names = {
        constraint.name
        for constraint in idempotency.constraints
        if isinstance(constraint, UniqueConstraint)
    }

    assert "version" in exceptions.c
    assert "uq_idempotency_scope_key" in unique_names


def test_outbox_carries_versioned_correlation_metadata() -> None:
    outbox = Base.metadata.tables["outbox_messages"]

    assert {
        "event_id",
        "schema_name",
        "schema_version",
        "aggregate_id",
        "correlation_id",
        "available_at",
        "dispatched_at",
        "attempts",
    } <= set(outbox.c.keys())
