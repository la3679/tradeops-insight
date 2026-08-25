"""Required-document, memo, and malformed payload scenarios."""

from dataclasses import replace
from decimal import Decimal

import pytest
from test_models import make_trade

from tradeops_domain.errors import DomainValidationError
from tradeops_domain.exceptions import ExceptionType, Severity
from tradeops_domain.reconciliation.content import (
    MemoConflict,
    PayloadIssue,
    detect_content_exceptions,
)


def _conflict(*, field: str = "price") -> MemoConflict:
    return MemoConflict(
        field=field,
        observed="101.250000",
        expected="99.125000",
        confidence=Decimal("0.97"),
        extractor_version="patterns-v1",
    )


def test_complete_consistent_content_has_no_exception() -> None:
    assert detect_content_exceptions(make_trade()) == ()


def test_missing_confirmation_creates_review_finding() -> None:
    detected = detect_content_exceptions(
        replace(make_trade(), confirmation_received=False),
    )

    assert detected[0].exception_type is ExceptionType.DOCUMENT_OR_MEMO_ISSUE
    assert ("confirmation_received", "false") in detected[0].evidence[0].facts


def test_material_memo_conflict_is_high_severity() -> None:
    detected = detect_content_exceptions(make_trade(), memo_conflicts=(_conflict(),))

    assert detected[0].severity is Severity.HIGH
    assert ("conflict_0_extractor", "patterns-v1") in detected[0].evidence[0].facts


def test_nonmaterial_memo_conflict_is_medium_severity() -> None:
    detected = detect_content_exceptions(
        make_trade(),
        memo_conflicts=(_conflict(field="sales_note"),),
    )

    assert detected[0].severity is Severity.MEDIUM


def test_recoverable_payload_issue_suggests_correction() -> None:
    detected = detect_content_exceptions(
        make_trade(),
        payload_issues=(
            PayloadIssue(
                field="currency", reason="must be three uppercase letters", recoverable=True
            ),
        ),
    )

    assert detected[0].exception_type is ExceptionType.UNSUPPORTED_OR_MALFORMED_PAYLOAD
    assert "Correct and re-import" in detected[0].suggested_actions[0]


def test_unrecoverable_payload_issue_suggests_rejection() -> None:
    detected = detect_content_exceptions(
        make_trade(),
        payload_issues=(
            PayloadIssue(field="product_type", reason="not in allowlist", recoverable=False),
        ),
    )

    assert "Reject the payload" in detected[0].suggested_actions[0]


def test_document_and_payload_findings_are_both_preserved() -> None:
    detected = detect_content_exceptions(
        replace(make_trade(), confirmation_received=False),
        payload_issues=(PayloadIssue(field="memo", reason="invalid encoding", recoverable=True),),
    )

    assert len(detected) == 2


@pytest.mark.parametrize("confidence", [Decimal("-0.1"), Decimal("1.1"), Decimal("NaN")])
def test_memo_confidence_is_bounded(confidence: Decimal) -> None:
    with pytest.raises(DomainValidationError, match="confidence"):
        replace(_conflict(), confidence=confidence)


def test_payload_issue_requires_bounded_reason() -> None:
    with pytest.raises(DomainValidationError, match="reason"):
        PayloadIssue(field="memo", reason="", recoverable=True)
