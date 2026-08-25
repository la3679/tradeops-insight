"""Required-document, memo-contradiction, and malformed-field rules."""

from dataclasses import dataclass
from decimal import Decimal

from tradeops_domain.errors import DomainValidationError
from tradeops_domain.exceptions import (
    DetectedException,
    Evidence,
    ExceptionType,
    RiskLevel,
    Severity,
)
from tradeops_domain.models import SyntheticTrade

_MATERIAL_MEMO_FIELDS = frozenset(
    {
        "counterparty_lei",
        "currency",
        "instrument_id",
        "notional",
        "price",
        "quantity",
        "settlement_date",
        "side",
    }
)


def _bounded(*, field: str, value: str, maximum: int) -> None:
    if not value.strip() or len(value) > maximum:
        raise DomainValidationError(
            field=field,
            reason=f"must contain 1 to {maximum} characters",
        )


@dataclass(frozen=True, slots=True, kw_only=True)
class MemoConflict:
    """One extracted memo value that conflicts with structured trade data."""

    field: str
    observed: str
    expected: str
    confidence: Decimal
    extractor_version: str

    def __post_init__(self) -> None:
        _bounded(field="field", value=self.field, maximum=100)
        _bounded(field="observed", value=self.observed, maximum=500)
        _bounded(field="expected", value=self.expected, maximum=500)
        _bounded(field="extractor_version", value=self.extractor_version, maximum=100)
        if not self.confidence.is_finite() or not Decimal("0") <= self.confidence <= Decimal("1"):
            raise DomainValidationError(
                field="confidence",
                reason="must be a finite decimal between 0 and 1",
            )


@dataclass(frozen=True, slots=True, kw_only=True)
class PayloadIssue:
    """A bounded business-level parsing or support issue from ingestion."""

    field: str
    reason: str
    recoverable: bool

    def __post_init__(self) -> None:
        _bounded(field="field", value=self.field, maximum=100)
        _bounded(field="reason", value=self.reason, maximum=500)


def _document_or_memo_exception(
    trade: SyntheticTrade,
    conflicts: tuple[MemoConflict, ...],
) -> DetectedException:
    material = any(conflict.field in _MATERIAL_MEMO_FIELDS for conflict in conflicts)
    facts: list[tuple[str, str]] = [
        ("trade_id", trade.trade_id),
        ("confirmation_received", str(trade.confirmation_received).lower()),
        ("memo_conflict_count", str(len(conflicts))),
    ]
    for index, conflict in enumerate(conflicts):
        prefix = f"conflict_{index}"
        facts.extend(
            [
                (f"{prefix}_field", conflict.field),
                (f"{prefix}_observed", conflict.observed),
                (f"{prefix}_expected", conflict.expected),
                (f"{prefix}_confidence", format(conflict.confidence, "f")),
                (f"{prefix}_extractor", conflict.extractor_version),
            ]
        )
    return DetectedException(
        exception_type=ExceptionType.DOCUMENT_OR_MEMO_ISSUE,
        severity=Severity.HIGH if material else Severity.MEDIUM,
        risk=RiskLevel.HIGH if material else RiskLevel.MEDIUM,
        explanation=(
            "A required synthetic confirmation is missing or memo facts contradict the trade."
        ),
        suggested_actions=(
            "Review the synthetic confirmation and extracted memo entities.",
            "Request corrected evidence or escalate material contradictions.",
        ),
        evidence=(
            Evidence(
                code="DOCUMENT_OR_MEMO_CONFLICT",
                summary=(
                    "Required-document presence and extracted facts failed deterministic checks."
                ),
                facts=tuple(facts),
            ),
        ),
        requires_review=True,
    )


def _malformed_payload_exception(
    trade: SyntheticTrade,
    issues: tuple[PayloadIssue, ...],
) -> DetectedException:
    facts: list[tuple[str, str]] = [("trade_id", trade.trade_id)]
    for index, issue in enumerate(issues):
        prefix = f"issue_{index}"
        facts.extend(
            [
                (f"{prefix}_field", issue.field),
                (f"{prefix}_reason", issue.reason),
                (f"{prefix}_recoverable", str(issue.recoverable).lower()),
            ]
        )
    recoverable = all(issue.recoverable for issue in issues)
    return DetectedException(
        exception_type=ExceptionType.UNSUPPORTED_OR_MALFORMED_PAYLOAD,
        severity=Severity.HIGH,
        risk=RiskLevel.HIGH,
        explanation="One or more required business fields are malformed or unsupported.",
        suggested_actions=(
            "Correct and re-import the synthetic payload."
            if recoverable
            else "Reject the payload and escalate the unsupported fields.",
        ),
        evidence=(
            Evidence(
                code="PAYLOAD_BUSINESS_VALIDATION_FAILED",
                summary="Normalized import contains bounded field-level issues.",
                facts=tuple(facts),
            ),
        ),
        requires_review=True,
    )


def detect_content_exceptions(
    trade: SyntheticTrade,
    *,
    memo_conflicts: tuple[MemoConflict, ...] = (),
    payload_issues: tuple[PayloadIssue, ...] = (),
) -> tuple[DetectedException, ...]:
    """Detect required-document, memo, and normalized-payload exceptions."""

    detected: list[DetectedException] = []
    if not trade.confirmation_received or memo_conflicts:
        detected.append(_document_or_memo_exception(trade, memo_conflicts))
    if payload_issues:
        detected.append(_malformed_payload_exception(trade, payload_issues))
    return tuple(detected)
