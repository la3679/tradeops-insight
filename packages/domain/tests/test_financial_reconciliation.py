"""Fixed-precision financial reconciliation scenarios."""

from dataclasses import replace
from decimal import Decimal

import pytest
from test_models import make_trade

from tradeops_domain.errors import DomainValidationError
from tradeops_domain.exceptions import ExceptionType, Severity
from tradeops_domain.reconciliation.financial import (
    ExpectedFinancials,
    FinancialTolerance,
    detect_financial_exceptions,
)


def _expected() -> ExpectedFinancials:
    trade = make_trade()
    return ExpectedFinancials(
        quantity=trade.quantity,
        notional=trade.notional,
        price=trade.price,
        source_version="confirmation-v1",
    )


def test_exact_values_have_no_exception() -> None:
    assert detect_financial_exceptions(make_trade(), _expected()) == ()


def test_values_inside_tolerance_have_no_exception() -> None:
    trade = replace(
        make_trade(),
        notional=Decimal("1000000.01"),
        price=Decimal("99.175000"),
    )

    assert detect_financial_exceptions(trade, _expected()) == ()


def test_quantity_and_notional_variances_share_one_finding() -> None:
    trade = replace(
        make_trade(),
        quantity=Decimal("1000000.0001"),
        notional=Decimal("1000000.02"),
    )

    detected = detect_financial_exceptions(trade, _expected())

    assert len(detected) == 1
    assert detected[0].exception_type is ExceptionType.QUANTITY_OR_NOTIONAL_MISMATCH
    assert ("notional_difference", "0.02") in detected[0].evidence[0].facts


def test_small_price_breach_is_medium_severity() -> None:
    trade = replace(make_trade(), price=Decimal("99.175001"))

    detected = detect_financial_exceptions(trade, _expected())

    assert detected[0].exception_type is ExceptionType.PRICE_TOLERANCE_BREACH
    assert detected[0].severity is Severity.MEDIUM


def test_large_price_breach_is_high_severity() -> None:
    trade = replace(make_trade(), price=Decimal("100.000000"))

    detected = detect_financial_exceptions(trade, _expected())

    assert detected[0].severity is Severity.HIGH


@pytest.mark.parametrize("value", [Decimal("-0.01"), Decimal("NaN")])
def test_tolerance_rejects_negative_or_nonfinite_values(value: Decimal) -> None:
    with pytest.raises(DomainValidationError, match="price"):
        FinancialTolerance(price=value)


def test_expected_values_require_source_version() -> None:
    with pytest.raises(DomainValidationError, match="source_version"):
        replace(_expected(), source_version="")
