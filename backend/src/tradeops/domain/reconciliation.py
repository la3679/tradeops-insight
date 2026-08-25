"""Complete deterministic exception catalogue for synthetic trade envelopes."""

import re
from dataclasses import dataclass, field
from datetime import UTC, date, datetime, timedelta
from decimal import Decimal
from uuid import UUID, uuid5

from tradeops.domain.exceptions import ExceptionSeverity, ExceptionType, ReviewRoute
from tradeops.domain.rules.settlement_date import SettlementDatePolicy

_NAMESPACE = UUID("34036df2-cdf9-5e57-97d4-04234004c797")
_LEI_PATTERN = re.compile(r"LEI-DEMO-\d{6}")
SUPPORTED_PRODUCTS = frozenset({"government_bond", "corporate_bond"})


@dataclass(frozen=True, slots=True)
class ReferenceSnapshot:
    """Synthetic/public-derived reference facts used only by deterministic checks."""

    counterparty_lei: str
    counterparty_name: str
    counterparty_active: bool
    instrument_id: str
    currency: str
    notional: Decimal
    price: Decimal
    observed_at: datetime


@dataclass(frozen=True, slots=True)
class ReconciliationInput:
    """Trade payload plus independently observed reference and confirmation facts."""

    trade_id: UUID
    synthetic_trade_id: str
    event_id: str
    instrument_id: str
    counterparty_lei: str
    counterparty_name: str
    product_type: str
    currency: str
    notional: Decimal
    price: Decimal
    trade_date: date
    settlement_date: date
    memo: str
    confirmation_present: bool
    reference: ReferenceSnapshot
    duplicate_trade: bool = False
    duplicate_event: bool = False
    malformed_payload: bool = False


@dataclass(frozen=True, slots=True)
class ReconciliationFinding:
    """Stable finding suitable for persistence, audit, UI explanation, and routing."""

    id: UUID
    exception_type: ExceptionType
    severity: ExceptionSeverity
    review_route: ReviewRoute
    explanation: str
    evidence: tuple[str, ...]
    suggested_actions: tuple[str, ...]
    rule_version: str = "reconciliation-v1"


@dataclass(frozen=True, slots=True)
class ReconciliationPolicy:
    """Versioned tolerances and freshness bounds for the catalogue."""

    price_tolerance: Decimal = Decimal("0.50")
    notional_tolerance: Decimal = Decimal("0.01")
    reference_max_age: timedelta = timedelta(days=7)
    as_of: datetime = datetime(2026, 1, 15, tzinfo=UTC)
    settlement: SettlementDatePolicy = field(default_factory=SettlementDatePolicy)

    def __post_init__(self) -> None:
        if self.price_tolerance < 0 or self.notional_tolerance < 0:
            raise ValueError("numeric tolerances must not be negative")
        if self.reference_max_age < timedelta(0):
            raise ValueError("reference_max_age must not be negative")
        if self.as_of.tzinfo is None or self.as_of.utcoffset() != timedelta(0):
            raise ValueError("as_of must be timezone-aware UTC")


def _finding(
    item: ReconciliationInput,
    exception_type: ExceptionType,
    severity: ExceptionSeverity,
    explanation: str,
    evidence: tuple[str, ...],
    *,
    escalated: bool = False,
) -> ReconciliationFinding:
    route = ReviewRoute.ESCALATE if escalated else ReviewRoute.REVIEW_CORRECTION
    key = f"{item.trade_id}:{item.event_id}:{exception_type}:reconciliation-v1"
    actions = (
        ("Escalate for manual review; preserve the original synthetic facts.",)
        if escalated
        else (
            "Compare the synthetic trade with the cited evidence.",
            "Approve, edit, reject, or request more evidence before any demo-state change.",
        )
    )
    return ReconciliationFinding(
        id=uuid5(_NAMESPACE, key),
        exception_type=exception_type,
        severity=severity,
        review_route=route,
        explanation=explanation,
        evidence=evidence,
        suggested_actions=actions,
    )


def evaluate_reconciliation(
    item: ReconciliationInput, policy: ReconciliationPolicy
) -> tuple[ReconciliationFinding, ...]:
    """Evaluate all twelve rule families without network or model calls."""

    findings: list[ReconciliationFinding] = []
    reference = item.reference
    if not _LEI_PATTERN.fullmatch(item.counterparty_lei):
        findings.append(
            _finding(
                item,
                ExceptionType.INVALID_COUNTERPARTY_LEI,
                ExceptionSeverity.HIGH,
                "The counterparty identifier is missing or is not a synthetic LEI.",
                (f"observed={item.counterparty_lei or '<missing>'}", "expected=LEI-DEMO-000000"),
                escalated=not item.counterparty_lei,
            )
        )
    if item.counterparty_name.strip().casefold() != reference.counterparty_name.casefold():
        findings.append(
            _finding(
                item,
                ExceptionType.COUNTERPARTY_NAME_MISMATCH,
                ExceptionSeverity.MEDIUM,
                "The trade counterparty name differs from the reference snapshot.",
                (f"trade={item.counterparty_name}", f"reference={reference.counterparty_name}"),
                escalated=not item.counterparty_name.strip(),
            )
        )
    if item.counterparty_lei != reference.counterparty_lei or not reference.counterparty_active:
        findings.append(
            _finding(
                item,
                ExceptionType.UNKNOWN_OR_INACTIVE_ENTITY,
                ExceptionSeverity.HIGH,
                "The counterparty is unknown or inactive in the reference snapshot.",
                (
                    f"trade_lei={item.counterparty_lei}",
                    f"reference_lei={reference.counterparty_lei}",
                    f"active={reference.counterparty_active}",
                ),
                escalated=item.counterparty_lei != reference.counterparty_lei,
            )
        )
    if item.instrument_id != reference.instrument_id:
        findings.append(
            _finding(
                item,
                ExceptionType.INSTRUMENT_ID_MISMATCH,
                ExceptionSeverity.HIGH,
                "The synthetic instrument identifier differs from the reference snapshot.",
                (f"trade={item.instrument_id}", f"reference={reference.instrument_id}"),
                escalated=not item.instrument_id.startswith("INST-DEMO-"),
            )
        )
    notional_delta = abs(item.notional - reference.notional)
    if notional_delta > policy.notional_tolerance:
        material = notional_delta > max(reference.notional * Decimal("0.10"), Decimal("1"))
        findings.append(
            _finding(
                item,
                ExceptionType.NOTIONAL_MISMATCH,
                ExceptionSeverity.HIGH if material else ExceptionSeverity.MEDIUM,
                "The fixed-precision notional differs beyond the configured tolerance.",
                (f"delta={notional_delta}", f"tolerance={policy.notional_tolerance}"),
                escalated=material,
            )
        )
    price_delta = abs(item.price - reference.price)
    if price_delta > policy.price_tolerance:
        material = price_delta > policy.price_tolerance * Decimal("5")
        findings.append(
            _finding(
                item,
                ExceptionType.PRICE_OUTSIDE_TOLERANCE,
                ExceptionSeverity.HIGH if material else ExceptionSeverity.MEDIUM,
                "The trade price is outside the configured absolute tolerance.",
                (f"delta={price_delta}", f"tolerance={policy.price_tolerance}"),
                escalated=material,
            )
        )
    if item.currency != reference.currency:
        findings.append(
            _finding(
                item,
                ExceptionType.CURRENCY_MISMATCH,
                ExceptionSeverity.HIGH,
                "The trade currency differs from the instrument reference currency.",
                (f"trade={item.currency}", f"reference={reference.currency}"),
                escalated=item.currency not in {"USD", "EUR", "GBP"},
            )
        )
    expected_settlement = policy.settlement.expected_settlement_date(item.trade_date)
    if item.settlement_date != expected_settlement:
        delta = abs((item.settlement_date - expected_settlement).days)
        findings.append(
            _finding(
                item,
                ExceptionType.SETTLEMENT_DATE_MISMATCH,
                ExceptionSeverity.HIGH if delta > 2 else ExceptionSeverity.MEDIUM,
                "The settlement date does not match the versioned business-day convention.",
                (
                    f"observed={item.settlement_date.isoformat()}",
                    f"expected={expected_settlement.isoformat()}",
                ),
                escalated=item.settlement_date < item.trade_date or delta > 2,
            )
        )
    if item.duplicate_trade or item.duplicate_event:
        findings.append(
            _finding(
                item,
                ExceptionType.DUPLICATE_TRADE_OR_EVENT,
                ExceptionSeverity.HIGH,
                "A duplicate synthetic trade or event idempotency key was detected.",
                (
                    f"duplicate_trade={item.duplicate_trade}",
                    f"duplicate_event={item.duplicate_event}",
                ),
                escalated=item.duplicate_trade and item.duplicate_event,
            )
        )
    memo_contradicts = item.currency not in item.memo or item.instrument_id not in item.memo
    if not item.confirmation_present or memo_contradicts:
        findings.append(
            _finding(
                item,
                ExceptionType.MISSING_OR_CONTRADICTORY_DOCUMENT,
                ExceptionSeverity.HIGH
                if not item.confirmation_present
                else ExceptionSeverity.MEDIUM,
                "Required synthetic confirmation evidence is missing or the memo "
                "contradicts structured fields.",
                (
                    f"confirmation_present={item.confirmation_present}",
                    f"memo_contains_currency_and_instrument={not memo_contradicts}",
                ),
                escalated=not item.confirmation_present,
            )
        )
    reference_age = policy.as_of - reference.observed_at
    if reference_age > policy.reference_max_age:
        findings.append(
            _finding(
                item,
                ExceptionType.STALE_REFERENCE_DATA,
                ExceptionSeverity.MEDIUM,
                "The reference snapshot is older than the configured freshness bound.",
                (f"age_days={reference_age.days}", f"max_days={policy.reference_max_age.days}"),
                escalated=reference_age > policy.reference_max_age * 3,
            )
        )
    if item.malformed_payload or item.product_type not in SUPPORTED_PRODUCTS:
        findings.append(
            _finding(
                item,
                ExceptionType.UNSUPPORTED_OR_MALFORMED_TRADE,
                ExceptionSeverity.HIGH,
                "The trade payload is malformed or its product type is unsupported.",
                (f"product_type={item.product_type}", f"malformed={item.malformed_payload}"),
                escalated=item.malformed_payload,
            )
        )
    return tuple(findings)
