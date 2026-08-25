"""Settlement-date mismatch detection with explicit business-day policy."""

from dataclasses import dataclass
from datetime import date, timedelta
from uuid import UUID, uuid5

from tradeops.domain.exceptions import (
    ExceptionFinding,
    ExceptionSeverity,
    ExceptionType,
    ReviewRoute,
)
from tradeops.domain.trades import SyntheticTrade

_FINDING_NAMESPACE = UUID("12fa4460-64b9-5dd0-9c27-a4c6029e4f21")


@dataclass(frozen=True, slots=True)
class SettlementDatePolicy:
    """Versioned convention supplied to the settlement-date rule."""

    version: str = "settlement-date-v1"
    business_day_lag: int = 2
    escalation_threshold_calendar_days: int = 2
    holidays: frozenset[date] = frozenset()

    def __post_init__(self) -> None:
        if not self.version.strip():
            raise ValueError("policy version must not be blank")
        if self.business_day_lag < 0:
            raise ValueError("business_day_lag must not be negative")
        if self.escalation_threshold_calendar_days < 0:
            raise ValueError("escalation threshold must not be negative")

    def is_business_day(self, candidate: date) -> bool:
        return candidate.weekday() < 5 and candidate not in self.holidays

    def expected_settlement_date(self, trade_date: date) -> date:
        candidate = trade_date
        remaining = self.business_day_lag
        while remaining:
            candidate += timedelta(days=1)
            if self.is_business_day(candidate):
                remaining -= 1
        return candidate


def evaluate_settlement_date(
    trade: SyntheticTrade,
    policy: SettlementDatePolicy,
) -> ExceptionFinding | None:
    """Return a typed mismatch finding, or ``None`` when the dates agree."""

    expected = policy.expected_settlement_date(trade.trade_date)
    observed = trade.settlement_date
    if observed == expected:
        return None

    difference = abs((observed - expected).days)
    must_escalate = (
        observed < trade.trade_date or difference > policy.escalation_threshold_calendar_days
    )
    severity = ExceptionSeverity.HIGH if must_escalate else ExceptionSeverity.MEDIUM
    route = ReviewRoute.ESCALATE if must_escalate else ReviewRoute.REVIEW_CORRECTION
    explanation = (
        f"Synthetic trade {trade.synthetic_trade_id} has settlement date "
        f"{observed.isoformat()}; policy {policy.version} expects {expected.isoformat()} "
        f"using T+{policy.business_day_lag} business days."
    )
    actions = (
        ("Escalate for manual review; do not alter the synthetic trade.",)
        if must_escalate
        else (
            "Review the proposed settlement date against the synthetic trade evidence.",
            "Approve or reject any correction through the reviewed workflow.",
        )
    )
    finding_key = (
        f"{trade.id}:{trade.version}:{ExceptionType.SETTLEMENT_DATE_MISMATCH}:"
        f"{policy.version}:{expected.isoformat()}:{observed.isoformat()}"
    )
    return ExceptionFinding(
        id=uuid5(_FINDING_NAMESPACE, finding_key),
        exception_type=ExceptionType.SETTLEMENT_DATE_MISMATCH,
        trade_id=trade.id,
        rule_version=policy.version,
        severity=severity,
        review_route=route,
        expected_date=expected,
        observed_date=observed,
        explanation=explanation,
        suggested_actions=actions,
    )
