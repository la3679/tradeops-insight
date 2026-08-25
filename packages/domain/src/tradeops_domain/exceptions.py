"""Typed, explainable exception results."""

from dataclasses import dataclass
from enum import StrEnum


class ExceptionType(StrEnum):
    """The twelve exception families supported by the initial release."""

    MISSING_OR_INVALID_LEI = "missing_or_invalid_lei"
    LEGAL_NAME_MISMATCH = "legal_name_mismatch"
    UNKNOWN_OR_INACTIVE_ENTITY = "unknown_or_inactive_entity"
    INSTRUMENT_MISMATCH = "instrument_mismatch"
    QUANTITY_OR_NOTIONAL_MISMATCH = "quantity_or_notional_mismatch"
    PRICE_TOLERANCE_BREACH = "price_tolerance_breach"
    CURRENCY_MISMATCH = "currency_mismatch"
    SETTLEMENT_DATE_MISMATCH = "settlement_date_mismatch"
    DUPLICATE_TRADE_OR_EVENT = "duplicate_trade_or_event"
    DOCUMENT_OR_MEMO_ISSUE = "document_or_memo_issue"
    STALE_REFERENCE_DATA = "stale_reference_data"
    UNSUPPORTED_OR_MALFORMED_PAYLOAD = "unsupported_or_malformed_payload"


class Severity(StrEnum):
    """Operational urgency of a detected exception."""

    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class RiskLevel(StrEnum):
    """Deterministic review risk assigned independently of a model."""

    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


@dataclass(frozen=True, slots=True, kw_only=True)
class Evidence:
    """Human-readable evidence produced by a deterministic rule."""

    code: str
    summary: str
    facts: tuple[tuple[str, str], ...]


@dataclass(frozen=True, slots=True, kw_only=True)
class DetectedException:
    """One exception family detected for a synthetic trade."""

    exception_type: ExceptionType
    severity: Severity
    risk: RiskLevel
    explanation: str
    suggested_actions: tuple[str, ...]
    evidence: tuple[Evidence, ...]
    requires_review: bool
