from collections.abc import Callable
from dataclasses import replace
from datetime import UTC, date, datetime
from decimal import Decimal
from typing import cast
from uuid import UUID

import pytest

from tradeops.domain.trades import SyntheticTrade, TradeValidationError


def synthetic_trade() -> SyntheticTrade:
    return SyntheticTrade(
        id=UUID("f1164f22-67b7-5e75-8cf2-763008f918bd"),
        synthetic_trade_id="TRD-DEMO-000001",
        synthetic_instrument_id="INST-DEMO-000001",
        trade_date=date(2026, 8, 21),
        settlement_date=date(2026, 8, 25),
        currency="USD",
        notional=Decimal("1000000.00"),
        observed_at=datetime(2026, 8, 21, 15, 30, tzinfo=UTC),
    )


def test_synthetic_trade_accepts_fixed_precision_and_utc_facts() -> None:
    trade = synthetic_trade()

    assert trade.notional == Decimal("1000000.00")
    assert trade.observed_at.tzinfo is UTC
    assert trade.version == 1


@pytest.mark.parametrize(
    "mutate",
    [
        lambda trade: replace(trade, synthetic_trade_id="REAL-123"),
        lambda trade: replace(trade, synthetic_instrument_id="CUSIP-123"),
        lambda trade: replace(trade, currency="usd"),
        lambda trade: replace(trade, notional=Decimal("0")),
        lambda trade: replace(trade, notional=cast(Decimal, 1.0)),
        lambda trade: replace(trade, observed_at=datetime(2026, 8, 21, 15, 30)),
        lambda trade: replace(trade, version=0),
    ],
)
def test_synthetic_trade_rejects_invalid_facts(
    mutate: Callable[[SyntheticTrade], SyntheticTrade],
) -> None:
    with pytest.raises(TradeValidationError):
        mutate(synthetic_trade())
