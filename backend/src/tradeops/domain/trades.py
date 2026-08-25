"""Immutable synthetic trade facts."""

import re
from dataclasses import dataclass
from datetime import date, datetime, timedelta
from decimal import Decimal
from uuid import UUID

_TRADE_ID_PATTERN = re.compile(r"TRD-DEMO-\d{6}")
_INSTRUMENT_ID_PATTERN = re.compile(r"INST-DEMO-\d{6}")
_CURRENCY_PATTERN = re.compile(r"[A-Z]{3}")


class TradeValidationError(ValueError):
    """Raised when a synthetic trade violates a domain invariant."""


@dataclass(frozen=True, slots=True)
class SyntheticTrade:
    """A versioned synthetic trade snapshot used as input to deterministic rules."""

    id: UUID
    synthetic_trade_id: str
    synthetic_instrument_id: str
    trade_date: date
    settlement_date: date
    currency: str
    notional: Decimal
    observed_at: datetime
    version: int = 1

    def __post_init__(self) -> None:
        if not _TRADE_ID_PATTERN.fullmatch(self.synthetic_trade_id):
            raise TradeValidationError("synthetic_trade_id must match TRD-DEMO-000000")
        if not _INSTRUMENT_ID_PATTERN.fullmatch(self.synthetic_instrument_id):
            raise TradeValidationError("synthetic_instrument_id must match INST-DEMO-000000")
        if not _CURRENCY_PATTERN.fullmatch(self.currency):
            raise TradeValidationError("currency must be a three-letter uppercase code")
        if not isinstance(self.notional, Decimal) or self.notional <= Decimal("0"):
            raise TradeValidationError("notional must be a positive Decimal")
        if self.observed_at.tzinfo is None or self.observed_at.utcoffset() != timedelta(0):
            raise TradeValidationError("observed_at must be timezone-aware UTC")
        if self.version < 1:
            raise TradeValidationError("version must be at least 1")
