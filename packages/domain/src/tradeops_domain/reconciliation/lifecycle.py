"""Business-day settlement and duplicate-event rules."""

from collections.abc import Set
from dataclasses import dataclass
from datetime import date, timedelta
from hashlib import sha256

from tradeops_domain.errors import DomainValidationError
from tradeops_domain.exceptions import (
    DetectedException,
    Evidence,
    ExceptionType,
    RiskLevel,
    Severity,
)
from tradeops_domain.models import SyntheticTrade


@dataclass(frozen=True, slots=True, kw_only=True)
class SettlementPolicy:
    """Versionable weekend and holiday calendar for a demo market."""

    lag_business_days: int = 2
    holidays: frozenset[date] = frozenset()
    version: str = "demo-us-v1"

    def __post_init__(self) -> None:
        if self.lag_business_days < 0 or self.lag_business_days > 10:
            raise DomainValidationError(
                field="lag_business_days",
                reason="must be between 0 and 10",
            )
        if not self.version.strip() or len(self.version) > 100:
            raise DomainValidationError(
                field="version",
                reason="must contain 1 to 100 characters",
            )


def _is_business_day(value: date, policy: SettlementPolicy) -> bool:
    return value.weekday() < 5 and value not in policy.holidays


def calculate_settlement_date(
    trade_date: date,
    policy: SettlementPolicy | None = None,
) -> date:
    """Add the configured number of business days without external calendars."""

    resolved = policy or SettlementPolicy()
    candidate = trade_date
    added = 0
    while added < resolved.lag_business_days:
        candidate += timedelta(days=1)
        if _is_business_day(candidate, resolved):
            added += 1
    return candidate


def trade_fingerprint(trade: SyntheticTrade) -> str:
    """Hash canonical economic fields; exclude record/event identifiers."""

    values = (
        trade.counterparty_lei or "",
        trade.counterparty_name.strip().casefold(),
        trade.instrument_id,
        trade.product_type,
        trade.side.value,
        trade.currency,
        format(trade.quantity, "f"),
        format(trade.notional, "f"),
        format(trade.price, "f"),
        trade.trade_date.isoformat(),
        trade.settlement_date.isoformat(),
    )
    return sha256("\x1f".join(values).encode()).hexdigest()


def _settlement_exception(
    trade: SyntheticTrade,
    expected: date,
    policy: SettlementPolicy,
) -> DetectedException:
    return DetectedException(
        exception_type=ExceptionType.SETTLEMENT_DATE_MISMATCH,
        severity=Severity.HIGH,
        risk=RiskLevel.HIGH,
        explanation="Settlement date differs from the configured business-day calculation.",
        suggested_actions=(
            "Review the trade date, calendar version, and holiday inputs.",
            "Propose the calculated synthetic settlement date for review.",
        ),
        evidence=(
            Evidence(
                code="SETTLEMENT_DATE_MISMATCH",
                summary="Observed and calculated settlement dates differ.",
                facts=(
                    ("trade_id", trade.trade_id),
                    ("trade_date", trade.trade_date.isoformat()),
                    ("observed_settlement_date", trade.settlement_date.isoformat()),
                    ("expected_settlement_date", expected.isoformat()),
                    ("calendar_version", policy.version),
                ),
            ),
        ),
        requires_review=True,
    )


def _duplicate_exception(
    trade: SyntheticTrade,
    *,
    duplicate_event: bool,
    duplicate_trade: bool,
) -> DetectedException:
    return DetectedException(
        exception_type=ExceptionType.DUPLICATE_TRADE_OR_EVENT,
        severity=Severity.HIGH if duplicate_trade else Severity.MEDIUM,
        risk=RiskLevel.HIGH if duplicate_trade else RiskLevel.MEDIUM,
        explanation="The event identifier or canonical trade fingerprint was already observed.",
        suggested_actions=(
            "Compare the prior event and trade versions.",
            "Reject the duplicate or escalate conflicting versions.",
        ),
        evidence=(
            Evidence(
                code="DUPLICATE_TRADE_OR_EVENT",
                summary="An idempotency or economic-identity comparison matched prior state.",
                facts=(
                    ("trade_id", trade.trade_id),
                    ("event_id", trade.event_id),
                    ("duplicate_event", str(duplicate_event).lower()),
                    ("duplicate_trade", str(duplicate_trade).lower()),
                    ("trade_fingerprint", trade_fingerprint(trade)),
                ),
            ),
        ),
        requires_review=True,
    )


def detect_lifecycle_exceptions(
    trade: SyntheticTrade,
    *,
    seen_event_ids: Set[str],
    seen_trade_fingerprints: Set[str],
    settlement_policy: SettlementPolicy | None = None,
) -> tuple[DetectedException, ...]:
    """Detect settlement and duplicate lifecycle exceptions."""

    policy = settlement_policy or SettlementPolicy()
    detected: list[DetectedException] = []
    expected_settlement = calculate_settlement_date(trade.trade_date, policy)
    if trade.settlement_date != expected_settlement:
        detected.append(_settlement_exception(trade, expected_settlement, policy))

    duplicate_event = trade.event_id in seen_event_ids
    duplicate_trade = trade_fingerprint(trade) in seen_trade_fingerprints
    if duplicate_event or duplicate_trade:
        detected.append(
            _duplicate_exception(
                trade,
                duplicate_event=duplicate_event,
                duplicate_trade=duplicate_trade,
            )
        )

    return tuple(detected)
