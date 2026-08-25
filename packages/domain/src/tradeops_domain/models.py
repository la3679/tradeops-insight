"""Core immutable domain records and structural invariants."""

import re
from dataclasses import dataclass
from datetime import UTC, date, datetime
from decimal import Decimal
from enum import StrEnum
from uuid import UUID

from tradeops_domain.errors import DomainValidationError

_TRADE_ID = re.compile(r"^TRD-DEMO-[0-9]{6}$")
_INSTRUMENT_ID = re.compile(r"^INST-DEMO-[0-9]{6}$")
_EVENT_ID = re.compile(r"^EVT-DEMO-[0-9]{6}$")
_CURRENCY = re.compile(r"^[A-Z]{3}$")
_LEI_SHAPE = re.compile(r"^[A-Z0-9]{20}$")


class Side(StrEnum):
    """Synthetic trade direction."""

    BUY = "buy"
    SELL = "sell"


class ProductType(StrEnum):
    """Products supported by the initial deterministic demo."""

    GOVERNMENT_BOND = "government_bond"
    CORPORATE_BOND = "corporate_bond"


class EntityStatus(StrEnum):
    """Bounded legal-entity lifecycle status used by reconciliation."""

    ACTIVE = "active"
    INACTIVE = "inactive"


def _require_pattern(*, field: str, value: str, pattern: re.Pattern[str]) -> None:
    if pattern.fullmatch(value) is None:
        raise DomainValidationError(field=field, reason="invalid format")


def _require_bounded_text(
    *, field: str, value: str, maximum: int, allow_empty: bool = False
) -> None:
    if (not allow_empty and not value.strip()) or len(value) > maximum:
        raise DomainValidationError(
            field=field, reason=f"must contain at most {maximum} characters"
        )


def _require_positive_decimal(*, field: str, value: Decimal) -> None:
    if not value.is_finite() or value <= 0:
        raise DomainValidationError(field=field, reason="must be a positive finite decimal")


def _require_utc(*, field: str, value: datetime) -> None:
    if value.tzinfo is None or value.utcoffset() != UTC.utcoffset(value):
        raise DomainValidationError(field=field, reason="must be timezone-aware UTC")


@dataclass(frozen=True, slots=True, kw_only=True)
class CounterpartyReference:
    """Versioned reference record from an approved source or fixture."""

    lei: str
    legal_name: str
    status: EntityStatus
    retrieved_at: datetime
    source_version: str

    def __post_init__(self) -> None:
        _require_pattern(field="lei", value=self.lei, pattern=_LEI_SHAPE)
        _require_bounded_text(field="legal_name", value=self.legal_name, maximum=200)
        _require_utc(field="retrieved_at", value=self.retrieved_at)
        _require_bounded_text(field="source_version", value=self.source_version, maximum=100)


@dataclass(frozen=True, slots=True, kw_only=True)
class InstrumentReference:
    """Synthetic instrument reference used for exact matching."""

    instrument_id: str
    product_type: ProductType
    currency: str
    issuer_lei: str | None
    retrieved_at: datetime

    def __post_init__(self) -> None:
        _require_pattern(field="instrument_id", value=self.instrument_id, pattern=_INSTRUMENT_ID)
        _require_pattern(field="currency", value=self.currency, pattern=_CURRENCY)
        if self.issuer_lei is not None:
            _require_pattern(field="issuer_lei", value=self.issuer_lei, pattern=_LEI_SHAPE)
        _require_utc(field="retrieved_at", value=self.retrieved_at)


@dataclass(frozen=True, slots=True, kw_only=True)
class SyntheticTrade:
    """One normalized synthetic trade event ready for reconciliation."""

    id: UUID
    trade_id: str
    event_id: str
    version: int
    counterparty_lei: str | None
    counterparty_name: str
    instrument_id: str
    product_type: str
    side: Side
    currency: str
    quantity: Decimal
    notional: Decimal
    price: Decimal
    trade_date: date
    settlement_date: date
    confirmation_received: bool
    memo: str | None
    created_at: datetime

    def __post_init__(self) -> None:
        _require_pattern(field="trade_id", value=self.trade_id, pattern=_TRADE_ID)
        _require_pattern(field="event_id", value=self.event_id, pattern=_EVENT_ID)
        _require_pattern(field="instrument_id", value=self.instrument_id, pattern=_INSTRUMENT_ID)
        if self.version < 1:
            raise DomainValidationError(field="version", reason="must be at least 1")
        if self.counterparty_lei is not None:
            _require_bounded_text(
                field="counterparty_lei",
                value=self.counterparty_lei,
                maximum=64,
                allow_empty=True,
            )
        _require_bounded_text(field="counterparty_name", value=self.counterparty_name, maximum=200)
        _require_bounded_text(field="product_type", value=self.product_type, maximum=100)
        _require_bounded_text(field="currency", value=self.currency, maximum=8)
        _require_positive_decimal(field="quantity", value=self.quantity)
        _require_positive_decimal(field="notional", value=self.notional)
        _require_positive_decimal(field="price", value=self.price)
        if self.settlement_date < self.trade_date:
            raise DomainValidationError(
                field="settlement_date",
                reason="must not precede trade_date",
            )
        if self.memo is not None:
            _require_bounded_text(field="memo", value=self.memo, maximum=2_000, allow_empty=True)
        _require_utc(field="created_at", value=self.created_at)
