"""Core domain invariant tests."""

from collections.abc import Callable
from dataclasses import replace
from datetime import UTC, date, datetime, timedelta
from decimal import Decimal
from uuid import UUID

import pytest

from tradeops_domain.errors import DomainValidationError
from tradeops_domain.models import (
    CounterpartyReference,
    EntityStatus,
    InstrumentReference,
    ProductType,
    Side,
    SyntheticTrade,
)


def make_trade() -> SyntheticTrade:
    return SyntheticTrade(
        id=UUID("00000000-0000-4000-8000-000000000001"),
        trade_id="TRD-DEMO-000001",
        event_id="EVT-DEMO-000001",
        version=1,
        counterparty_lei="DEMOLEI0000000000010",
        counterparty_name="Northstar Demo Capital",
        instrument_id="INST-DEMO-000001",
        product_type=ProductType.CORPORATE_BOND,
        side=Side.BUY,
        currency="USD",
        quantity=Decimal("1000000.0000"),
        notional=Decimal("1000000.00"),
        price=Decimal("99.125000"),
        trade_date=date(2026, 8, 24),
        settlement_date=date(2026, 8, 26),
        confirmation_received=True,
        memo="Demo buy for TRD-DEMO-000001.",
        created_at=datetime(2026, 8, 24, 16, 30, tzinfo=UTC),
    )


def test_valid_trade_preserves_decimal_precision() -> None:
    trade = make_trade()

    assert trade.price == Decimal("99.125000")
    assert trade.quantity == Decimal("1000000.0000")


@pytest.mark.parametrize(
    ("field", "factory"),
    [
        ("trade_id", lambda: replace(make_trade(), trade_id="REAL-123")),
        ("event_id", lambda: replace(make_trade(), event_id="EVENT-1")),
        ("instrument_id", lambda: replace(make_trade(), instrument_id="CUSIP-LIKE")),
        ("version", lambda: replace(make_trade(), version=0)),
        ("quantity", lambda: replace(make_trade(), quantity=Decimal("0"))),
        ("notional", lambda: replace(make_trade(), notional=Decimal("NaN"))),
        ("price", lambda: replace(make_trade(), price=Decimal("-1"))),
    ],
)
def test_trade_rejects_structural_invariant_violations(
    field: str,
    factory: Callable[[], SyntheticTrade],
) -> None:
    with pytest.raises(DomainValidationError) as error:
        factory()

    assert error.value.field == field


def test_trade_allows_bounded_bad_operational_values_for_reconciliation() -> None:
    trade = replace(
        make_trade(),
        counterparty_lei="not-a-lei",
        product_type="unsupported_demo_swap",
        currency="US_DOLL",
    )

    assert trade.counterparty_lei == "not-a-lei"
    assert trade.product_type == "unsupported_demo_swap"


def test_trade_rejects_settlement_before_trade_date() -> None:
    with pytest.raises(DomainValidationError, match="settlement_date"):
        replace(make_trade(), settlement_date=date(2026, 8, 23))


def test_trade_rejects_non_utc_timestamp() -> None:
    non_utc = datetime(2026, 8, 24, 12, tzinfo=UTC) + timedelta(hours=1)

    with pytest.raises(DomainValidationError, match="created_at"):
        replace(make_trade(), created_at=non_utc.replace(tzinfo=None))


def test_reference_records_enforce_identifier_shapes() -> None:
    counterparty = CounterpartyReference(
        lei="DEMOLEI0000000000010",
        legal_name="Northstar Demo Capital",
        status=EntityStatus.ACTIVE,
        retrieved_at=datetime(2026, 8, 24, tzinfo=UTC),
        source_version="fixture-1",
    )
    instrument = InstrumentReference(
        instrument_id="INST-DEMO-000001",
        product_type=ProductType.GOVERNMENT_BOND,
        currency="USD",
        issuer_lei=None,
        retrieved_at=datetime(2026, 8, 24, tzinfo=UTC),
    )

    assert counterparty.status is EntityStatus.ACTIVE
    assert instrument.product_type is ProductType.GOVERNMENT_BOND
