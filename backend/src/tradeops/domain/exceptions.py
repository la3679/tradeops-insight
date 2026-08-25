"""Structured outputs from deterministic exception rules."""

from dataclasses import dataclass
from datetime import date
from enum import StrEnum
from uuid import UUID


class ExceptionType(StrEnum):
    INVALID_COUNTERPARTY_LEI = "invalid_counterparty_lei"
    COUNTERPARTY_NAME_MISMATCH = "counterparty_name_mismatch"
    UNKNOWN_OR_INACTIVE_ENTITY = "unknown_or_inactive_entity"
    INSTRUMENT_ID_MISMATCH = "instrument_id_mismatch"
    NOTIONAL_MISMATCH = "notional_mismatch"
    PRICE_OUTSIDE_TOLERANCE = "price_outside_tolerance"
    CURRENCY_MISMATCH = "currency_mismatch"
    SETTLEMENT_DATE_MISMATCH = "settlement_date_mismatch"
    DUPLICATE_TRADE_OR_EVENT = "duplicate_trade_or_event"
    MISSING_OR_CONTRADICTORY_DOCUMENT = "missing_or_contradictory_document"
    STALE_REFERENCE_DATA = "stale_reference_data"
    UNSUPPORTED_OR_MALFORMED_TRADE = "unsupported_or_malformed_trade"


class ExceptionSeverity(StrEnum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class ReviewRoute(StrEnum):
    REVIEW_CORRECTION = "review_correction"
    ESCALATE = "escalate"


@dataclass(frozen=True, slots=True)
class ExceptionFinding:
    """An explainable, deterministic rule finding; never an automatic state change."""

    id: UUID
    exception_type: ExceptionType
    trade_id: UUID
    rule_version: str
    severity: ExceptionSeverity
    review_route: ReviewRoute
    expected_date: date
    observed_date: date
    explanation: str
    suggested_actions: tuple[str, ...]
