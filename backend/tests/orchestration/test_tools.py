"""Typed tool schema, authorization, conflict, and deterministic behavior tests."""

from datetime import date

import pytest
from pydantic import ValidationError

from tradeops.orchestration.tools import (
    TOOL_ALLOWLIST,
    ApplyResolutionInput,
    CompareTradeVersionsInput,
    SafeResolutionTool,
    SettlementDateInput,
    ToolAuthorizationError,
    ToolConflictError,
    calculate_settlement_date,
    compare_trade_versions,
)


def test_calculate_settlement_date_and_compare_versions() -> None:
    settlement = calculate_settlement_date(
        SettlementDateInput(
            trade_date=date(2026, 1, 16),
            business_day_lag=2,
            holidays=frozenset({date(2026, 1, 19)}),
        )
    )
    comparison = compare_trade_versions(
        CompareTradeVersionsInput(
            previous={"currency": "USD", "price": "99.00"},
            current={"currency": "EUR", "price": "99.00", "memo": "synthetic"},
        )
    )

    assert settlement.settlement_date == date(2026, 1, 21)
    assert [difference.field for difference in comparison.differences] == ["currency", "memo"]
    assert TOOL_ALLOWLIST == {
        "calculate_settlement_date",
        "compare_trade_versions",
        "apply_approved_demo_resolution",
    }


def _resolution(**updates: object) -> ApplyResolutionInput:
    values: dict[str, object] = {
        "role": "reviewer",
        "decision": "approve",
        "field": "currency",
        "value": "USD",
        "expected_version": 1,
        "current_version": 1,
        "idempotency_key": "resolution-key-1",
    }
    values.update(updates)
    return ApplyResolutionInput.model_validate(values)


def test_resolution_requires_approval_role_allowlist_version_and_unique_key() -> None:
    tool = SafeResolutionTool()

    result = tool.apply(_resolution())

    assert result.applied is True
    assert result.next_version == 2
    with pytest.raises(ToolConflictError, match="already used"):
        tool.apply(_resolution())
    with pytest.raises(ToolAuthorizationError, match="role"):
        tool.apply(_resolution(role="analyst", idempotency_key="resolution-key-2"))
    with pytest.raises(ToolAuthorizationError, match="decision"):
        tool.apply(_resolution(decision="reject", idempotency_key="resolution-key-3"))
    with pytest.raises(ToolAuthorizationError, match="allowlisted"):
        tool.apply(_resolution(field="secret", idempotency_key="resolution-key-4"))
    with pytest.raises(ToolConflictError, match="stale"):
        tool.apply(_resolution(expected_version=2, idempotency_key="resolution-key-5"))


def test_tool_schemas_reject_unknown_fields_and_invalid_bounds() -> None:
    with pytest.raises(ValidationError):
        SettlementDateInput.model_validate(
            {"trade_date": "2026-01-01", "business_day_lag": 11, "unexpected": True}
        )
