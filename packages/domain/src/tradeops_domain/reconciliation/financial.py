"""Fixed-precision quantity, notional, and price reconciliation."""

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


def _validate_nonnegative(*, field: str, value: Decimal) -> None:
    if not value.is_finite() or value < 0:
        raise DomainValidationError(field=field, reason="must be a nonnegative finite decimal")


@dataclass(frozen=True, slots=True, kw_only=True)
class ExpectedFinancials:
    """Authoritative comparison values from a second synthetic record version."""

    quantity: Decimal
    notional: Decimal
    price: Decimal
    source_version: str

    def __post_init__(self) -> None:
        for field, value in (
            ("quantity", self.quantity),
            ("notional", self.notional),
            ("price", self.price),
        ):
            if not value.is_finite() or value <= 0:
                raise DomainValidationError(
                    field=field,
                    reason="must be a positive finite decimal",
                )
        if not self.source_version.strip() or len(self.source_version) > 100:
            raise DomainValidationError(
                field="source_version",
                reason="must contain 1 to 100 characters",
            )


@dataclass(frozen=True, slots=True, kw_only=True)
class FinancialTolerance:
    """Versioned absolute tolerances; values remain Decimal throughout."""

    quantity: Decimal = Decimal("0.0000")
    notional: Decimal = Decimal("0.01")
    price: Decimal = Decimal("0.050000")

    def __post_init__(self) -> None:
        _validate_nonnegative(field="quantity", value=self.quantity)
        _validate_nonnegative(field="notional", value=self.notional)
        _validate_nonnegative(field="price", value=self.price)


def _fact(name: str, value: Decimal) -> tuple[str, str]:
    return name, format(value, "f")


def _quantity_or_notional_exception(
    trade: SyntheticTrade,
    expected: ExpectedFinancials,
    tolerance: FinancialTolerance,
) -> DetectedException:
    quantity_difference = abs(trade.quantity - expected.quantity)
    notional_difference = abs(trade.notional - expected.notional)
    return DetectedException(
        exception_type=ExceptionType.QUANTITY_OR_NOTIONAL_MISMATCH,
        severity=Severity.HIGH,
        risk=RiskLevel.HIGH,
        explanation="Quantity or notional differs from the comparison version beyond tolerance.",
        suggested_actions=(
            "Compare the two synthetic trade versions.",
            "Submit an evidence-backed field correction for supervisor review.",
        ),
        evidence=(
            Evidence(
                code="FINANCIAL_AMOUNT_MISMATCH",
                summary="Fixed-precision amount comparison exceeded policy.",
                facts=(
                    ("trade_id", trade.trade_id),
                    ("source_version", expected.source_version),
                    _fact("observed_quantity", trade.quantity),
                    _fact("expected_quantity", expected.quantity),
                    _fact("quantity_difference", quantity_difference),
                    _fact("quantity_tolerance", tolerance.quantity),
                    _fact("observed_notional", trade.notional),
                    _fact("expected_notional", expected.notional),
                    _fact("notional_difference", notional_difference),
                    _fact("notional_tolerance", tolerance.notional),
                ),
            ),
        ),
        requires_review=True,
    )


def _price_exception(
    trade: SyntheticTrade,
    expected: ExpectedFinancials,
    tolerance: FinancialTolerance,
) -> DetectedException:
    difference = abs(trade.price - expected.price)
    severe = difference > tolerance.price * Decimal("10")
    return DetectedException(
        exception_type=ExceptionType.PRICE_TOLERANCE_BREACH,
        severity=Severity.HIGH if severe else Severity.MEDIUM,
        risk=RiskLevel.HIGH if severe else RiskLevel.MEDIUM,
        explanation="Price differs from the comparison version beyond the configured tolerance.",
        suggested_actions=(
            "Review the versioned price evidence and tolerance.",
            "Escalate a large or unexplained price variance.",
        ),
        evidence=(
            Evidence(
                code="PRICE_TOLERANCE_EXCEEDED",
                summary="Absolute Decimal price variance exceeded policy.",
                facts=(
                    ("trade_id", trade.trade_id),
                    ("source_version", expected.source_version),
                    _fact("observed_price", trade.price),
                    _fact("expected_price", expected.price),
                    _fact("absolute_difference", difference),
                    _fact("tolerance", tolerance.price),
                ),
            ),
        ),
        requires_review=True,
    )


def detect_financial_exceptions(
    trade: SyntheticTrade,
    expected: ExpectedFinancials,
    policy: FinancialTolerance | None = None,
) -> tuple[DetectedException, ...]:
    """Compare financial values using exact Decimal arithmetic."""

    tolerance = policy or FinancialTolerance()
    detected: list[DetectedException] = []
    if (
        abs(trade.quantity - expected.quantity) > tolerance.quantity
        or abs(trade.notional - expected.notional) > tolerance.notional
    ):
        detected.append(_quantity_or_notional_exception(trade, expected, tolerance))
    if abs(trade.price - expected.price) > tolerance.price:
        detected.append(_price_exception(trade, expected, tolerance))
    return tuple(detected)
