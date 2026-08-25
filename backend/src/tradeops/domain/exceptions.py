"""Structured outputs from deterministic exception rules."""

from dataclasses import dataclass
from datetime import date
from enum import StrEnum
from uuid import UUID


class ExceptionType(StrEnum):
    SETTLEMENT_DATE_MISMATCH = "settlement_date_mismatch"


class ExceptionSeverity(StrEnum):
    MEDIUM = "medium"
    HIGH = "high"


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
