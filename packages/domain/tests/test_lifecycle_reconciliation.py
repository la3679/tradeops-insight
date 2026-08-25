"""Settlement calendar and duplicate-detection scenarios."""

from dataclasses import replace
from datetime import date

import pytest
from test_models import make_trade

from tradeops_domain.errors import DomainValidationError
from tradeops_domain.exceptions import ExceptionType, Severity
from tradeops_domain.reconciliation.lifecycle import (
    SettlementPolicy,
    calculate_settlement_date,
    detect_lifecycle_exceptions,
    trade_fingerprint,
)


def test_t_plus_two_skips_weekend() -> None:
    friday = date(2026, 8, 21)

    assert calculate_settlement_date(friday) == date(2026, 8, 25)


def test_t_plus_two_skips_configured_holiday() -> None:
    policy = SettlementPolicy(holidays=frozenset({date(2026, 8, 25)}))

    assert calculate_settlement_date(date(2026, 8, 24), policy) == date(2026, 8, 27)


def test_matching_lifecycle_has_no_exception() -> None:
    detected = detect_lifecycle_exceptions(
        make_trade(),
        seen_event_ids=frozenset(),
        seen_trade_fingerprints=frozenset(),
    )

    assert detected == ()


def test_settlement_mismatch_includes_expected_date() -> None:
    trade = replace(make_trade(), settlement_date=date(2026, 8, 27))
    detected = detect_lifecycle_exceptions(
        trade,
        seen_event_ids=frozenset(),
        seen_trade_fingerprints=frozenset(),
    )

    assert detected[0].exception_type is ExceptionType.SETTLEMENT_DATE_MISMATCH
    assert ("expected_settlement_date", "2026-08-26") in detected[0].evidence[0].facts


def test_duplicate_event_is_medium_severity() -> None:
    trade = make_trade()
    detected = detect_lifecycle_exceptions(
        trade,
        seen_event_ids={trade.event_id},
        seen_trade_fingerprints=frozenset(),
    )

    assert detected[0].exception_type is ExceptionType.DUPLICATE_TRADE_OR_EVENT
    assert detected[0].severity is Severity.MEDIUM


def test_duplicate_economic_trade_is_high_severity() -> None:
    trade = make_trade()
    detected = detect_lifecycle_exceptions(
        trade,
        seen_event_ids=frozenset(),
        seen_trade_fingerprints={trade_fingerprint(trade)},
    )

    assert detected[0].severity is Severity.HIGH
    assert ("duplicate_trade", "true") in detected[0].evidence[0].facts


def test_both_lifecycle_findings_are_preserved() -> None:
    trade = replace(make_trade(), settlement_date=date(2026, 8, 27))
    detected = detect_lifecycle_exceptions(
        trade,
        seen_event_ids={trade.event_id},
        seen_trade_fingerprints={trade_fingerprint(trade)},
    )

    assert [finding.exception_type for finding in detected] == [
        ExceptionType.SETTLEMENT_DATE_MISMATCH,
        ExceptionType.DUPLICATE_TRADE_OR_EVENT,
    ]


@pytest.mark.parametrize("lag", [-1, 11])
def test_settlement_policy_rejects_unbounded_lag(lag: int) -> None:
    with pytest.raises(DomainValidationError, match="lag_business_days"):
        SettlementPolicy(lag_business_days=lag)
