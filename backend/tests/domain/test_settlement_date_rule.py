from dataclasses import replace
from datetime import date

import pytest

from tradeops.domain.exceptions import ExceptionSeverity, ExceptionType, ReviewRoute
from tradeops.domain.rules.settlement_date import SettlementDatePolicy, evaluate_settlement_date

from .test_trades import synthetic_trade


def test_t_plus_two_skips_weekend() -> None:
    policy = SettlementDatePolicy()

    assert policy.expected_settlement_date(date(2026, 8, 21)) == date(2026, 8, 25)


def test_explicit_holiday_is_not_a_business_day() -> None:
    policy = SettlementDatePolicy(holidays=frozenset({date(2026, 8, 24)}))

    assert policy.expected_settlement_date(date(2026, 8, 21)) == date(2026, 8, 26)


def test_matching_settlement_date_has_no_finding() -> None:
    assert evaluate_settlement_date(synthetic_trade(), SettlementDatePolicy()) is None


def test_near_mismatch_proposes_reviewed_correction() -> None:
    trade = replace(synthetic_trade(), settlement_date=date(2026, 8, 24))

    finding = evaluate_settlement_date(trade, SettlementDatePolicy())

    assert finding is not None
    assert finding.exception_type is ExceptionType.SETTLEMENT_DATE_MISMATCH
    assert finding.severity is ExceptionSeverity.MEDIUM
    assert finding.review_route is ReviewRoute.REVIEW_CORRECTION
    assert finding.expected_date == date(2026, 8, 25)
    assert finding.observed_date == date(2026, 8, 24)
    assert finding.rule_version == "settlement-date-v1"
    assert "T+2 business days" in finding.explanation
    assert len(finding.suggested_actions) == 2


def test_large_mismatch_escalates_without_proposing_mutation() -> None:
    trade = replace(synthetic_trade(), settlement_date=date(2026, 9, 1))

    finding = evaluate_settlement_date(trade, SettlementDatePolicy())

    assert finding is not None
    assert finding.severity is ExceptionSeverity.HIGH
    assert finding.review_route is ReviewRoute.ESCALATE
    assert finding.suggested_actions == (
        "Escalate for manual review; do not alter the synthetic trade.",
    )


def test_settlement_before_trade_date_always_escalates() -> None:
    trade = replace(synthetic_trade(), settlement_date=date(2026, 8, 20))
    policy = SettlementDatePolicy(escalation_threshold_calendar_days=30)

    finding = evaluate_settlement_date(trade, policy)

    assert finding is not None
    assert finding.severity is ExceptionSeverity.HIGH


def test_finding_id_is_deterministic_and_version_sensitive() -> None:
    trade = replace(synthetic_trade(), settlement_date=date(2026, 8, 24))
    first = evaluate_settlement_date(trade, SettlementDatePolicy())
    repeated = evaluate_settlement_date(trade, SettlementDatePolicy())
    revised = evaluate_settlement_date(replace(trade, version=2), SettlementDatePolicy())

    assert first is not None and repeated is not None and revised is not None
    assert first.id == repeated.id
    assert first.id != revised.id


@pytest.mark.parametrize(
    "policy",
    [
        SettlementDatePolicy(version="settlement-date-v1"),
    ],
)
def test_policy_values_are_explicit(policy: SettlementDatePolicy) -> None:
    assert policy.business_day_lag == 2
    assert policy.escalation_threshold_calendar_days == 2


def test_policy_rejects_invalid_configuration() -> None:
    with pytest.raises(ValueError, match="version"):
        SettlementDatePolicy(version=" ")
    with pytest.raises(ValueError, match="business_day_lag"):
        SettlementDatePolicy(business_day_lag=-1)
    with pytest.raises(ValueError, match="escalation threshold"):
        SettlementDatePolicy(escalation_threshold_calendar_days=-1)
