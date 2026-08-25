"""Deterministic, seedable synthetic fixed-income dataset generation."""

from dataclasses import dataclass, field, replace
from datetime import UTC, date, datetime, timedelta
from decimal import Decimal
from random import Random
from uuid import UUID

from tradeops_domain.errors import DomainValidationError
from tradeops_domain.exceptions import ExceptionType
from tradeops_domain.models import (
    CounterpartyReference,
    EntityStatus,
    InstrumentReference,
    ProductType,
    Side,
    SyntheticTrade,
)
from tradeops_domain.reconciliation.financial import ExpectedFinancials
from tradeops_domain.reconciliation.lifecycle import calculate_settlement_date


@dataclass(frozen=True, slots=True, kw_only=True)
class GeneratorConfig:
    """Bounded counts for a reproducible portfolio-sized demo."""

    seed: int = 20260824
    counterparty_count: int = 100
    instrument_count: int = 100
    trade_count: int = 3_000
    exception_count: int = 360
    generated_at: datetime = field(default_factory=lambda: datetime(2026, 8, 24, 12, tzinfo=UTC))

    def __post_init__(self) -> None:
        if self.counterparty_count < 4 or self.counterparty_count > 999_999:
            raise DomainValidationError(
                field="counterparty_count",
                reason="must be between 4 and 999999",
            )
        if self.instrument_count < 4 or self.instrument_count > 999_999:
            raise DomainValidationError(
                field="instrument_count",
                reason="must be between 4 and 999999",
            )
        if self.trade_count < 24 or self.trade_count > 999_999:
            raise DomainValidationError(
                field="trade_count",
                reason="must be between 24 and 999999",
            )
        if self.exception_count < 24 or self.exception_count > self.trade_count:
            raise DomainValidationError(
                field="exception_count",
                reason="must be between 24 and trade_count",
            )
        if self.generated_at.tzinfo is None or self.generated_at.utcoffset() != timedelta(0):
            raise DomainValidationError(
                field="generated_at",
                reason="must be timezone-aware UTC",
            )


@dataclass(frozen=True, slots=True, kw_only=True)
class SeededScenario:
    """Expected family and comparison values for one intentionally modified trade."""

    trade_id: str
    expected_exception: ExceptionType
    escalation: bool
    expected_financials: ExpectedFinancials


@dataclass(frozen=True, slots=True, kw_only=True)
class SyntheticDataset:
    """Generated source records plus explicit expected scenario labels."""

    seed: int
    generated_at: datetime
    counterparties: tuple[CounterpartyReference, ...]
    instruments: tuple[InstrumentReference, ...]
    trades: tuple[SyntheticTrade, ...]
    scenarios: tuple[SeededScenario, ...]


def _lei(index: int) -> str:
    prefix = f"DEMO{index:014d}"
    expanded = "".join(str(int(character, 36)) for character in f"{prefix}00")
    check_digits = 98 - (int(expanded) % 97)
    return f"{prefix}{check_digits:02d}"


def _counterparties(config: GeneratorConfig) -> tuple[CounterpartyReference, ...]:
    result: list[CounterpartyReference] = []
    for index in range(1, config.counterparty_count + 1):
        result.append(
            CounterpartyReference(
                lei=_lei(index),
                legal_name=f"Demo Counterparty {index:03d} LLC",
                aliases=(f"Demo Counterparty {index:03d}",),
                status=(
                    EntityStatus.INACTIVE
                    if index == config.counterparty_count
                    else EntityStatus.ACTIVE
                ),
                retrieved_at=(
                    config.generated_at - timedelta(days=30)
                    if index == config.counterparty_count - 1
                    else config.generated_at
                ),
                source_version="synthetic-reference-v1",
            )
        )
    return tuple(result)


def _instruments(config: GeneratorConfig) -> tuple[InstrumentReference, ...]:
    result: list[InstrumentReference] = []
    for index in range(1, config.instrument_count + 1):
        result.append(
            InstrumentReference(
                instrument_id=f"INST-DEMO-{index:06d}",
                product_type=(
                    ProductType.GOVERNMENT_BOND if index % 3 == 0 else ProductType.CORPORATE_BOND
                ),
                currency="USD",
                issuer_lei=None,
                retrieved_at=(
                    config.generated_at - timedelta(days=30)
                    if index == config.instrument_count
                    else config.generated_at
                ),
            )
        )
    return tuple(result)


def _baseline_trade(
    *,
    index: int,
    random: Random,
    config: GeneratorConfig,
    counterparties: tuple[CounterpartyReference, ...],
    instruments: tuple[InstrumentReference, ...],
) -> SyntheticTrade:
    counterparty = random.choice(counterparties[:-2])
    instrument = random.choice(instruments[:-1])
    trade_date = date(2026, 8, 17) + timedelta(days=random.randrange(5))
    quantity = random.choice(
        (Decimal("250000.0000"), Decimal("500000.0000"), Decimal("1000000.0000"))
    )
    price = Decimal(random.randrange(95000000, 105000001)) / Decimal("1000000")
    return SyntheticTrade(
        id=_uuid_for(index),
        trade_id=f"TRD-DEMO-{index:06d}",
        event_id=f"EVT-DEMO-{index:06d}",
        version=1,
        counterparty_lei=counterparty.lei,
        counterparty_name=counterparty.legal_name,
        instrument_id=instrument.instrument_id,
        product_type=instrument.product_type.value,
        side=Side.BUY if random.randrange(2) == 0 else Side.SELL,
        currency=instrument.currency,
        quantity=quantity,
        notional=quantity,
        price=price,
        trade_date=trade_date,
        settlement_date=calculate_settlement_date(trade_date),
        confirmation_received=True,
        memo=f"Synthetic {instrument.product_type.value} event TRD-DEMO-{index:06d}.",
        created_at=config.generated_at + timedelta(seconds=index),
    )


def _uuid_for(index: int) -> UUID:
    return UUID(f"00000000-0000-4000-8000-{index:012d}")


def _expected(trade: SyntheticTrade) -> ExpectedFinancials:
    return ExpectedFinancials(
        quantity=trade.quantity,
        notional=trade.notional,
        price=trade.price,
        source_version="synthetic-confirmation-v1",
    )


def _seed_exception(
    trade: SyntheticTrade,
    *,
    family: ExceptionType,
    escalation: bool,
    config: GeneratorConfig,
    counterparties: tuple[CounterpartyReference, ...],
    instruments: tuple[InstrumentReference, ...],
    first_trade: SyntheticTrade,
) -> SyntheticTrade:
    if family is ExceptionType.MISSING_OR_INVALID_LEI:
        return replace(trade, counterparty_lei="invalid-lei" if escalation else None)
    if family is ExceptionType.LEGAL_NAME_MISMATCH:
        return replace(trade, counterparty_name="Different Synthetic Entity")
    if family is ExceptionType.UNKNOWN_OR_INACTIVE_ENTITY:
        return replace(
            trade,
            counterparty_lei=(
                counterparties[-1].lei if escalation else _lei(config.counterparty_count + 10)
            ),
        )
    if family is ExceptionType.INSTRUMENT_MISMATCH:
        return replace(trade, instrument_id="INST-DEMO-999999")
    if family is ExceptionType.QUANTITY_OR_NOTIONAL_MISMATCH:
        return replace(trade, notional=trade.notional + Decimal("1000.00"))
    if family is ExceptionType.PRICE_TOLERANCE_BREACH:
        return replace(
            trade, price=trade.price + (Decimal("2.0") if escalation else Decimal("0.1"))
        )
    if family is ExceptionType.CURRENCY_MISMATCH:
        return replace(trade, currency="US_DOLL" if escalation else "EUR")
    if family is ExceptionType.SETTLEMENT_DATE_MISMATCH:
        return replace(trade, settlement_date=trade.settlement_date + timedelta(days=1))
    if family is ExceptionType.DUPLICATE_TRADE_OR_EVENT:
        if not escalation:
            return replace(trade, event_id=first_trade.event_id)
        return replace(
            first_trade,
            id=trade.id,
            trade_id=trade.trade_id,
            event_id=trade.event_id,
            created_at=trade.created_at,
        )
    if family is ExceptionType.DOCUMENT_OR_MEMO_ISSUE:
        return replace(
            trade,
            confirmation_received=False,
            memo=(
                f"Synthetic memo contradicts price {trade.price + Decimal('1.0')}"
                if escalation
                else None
            ),
        )
    if family is ExceptionType.STALE_REFERENCE_DATA:
        stale_instrument = instruments[-1]
        stale_counterparty = counterparties[-2]
        return replace(
            trade,
            instrument_id=stale_instrument.instrument_id,
            product_type=stale_instrument.product_type.value,
            counterparty_lei=stale_counterparty.lei,
            counterparty_name=stale_counterparty.legal_name,
        )
    return replace(trade, product_type="unsupported_demo_swap")


def generate_dataset(config: GeneratorConfig | None = None) -> SyntheticDataset:
    """Generate the same dataset for the same explicit configuration."""

    resolved = config or GeneratorConfig()
    random = Random(resolved.seed)
    counterparties = _counterparties(resolved)
    instruments = _instruments(resolved)
    trades: list[SyntheticTrade] = []
    scenarios: list[SeededScenario] = []
    families = tuple(ExceptionType)

    for index in range(1, resolved.trade_count + 1):
        baseline = _baseline_trade(
            index=index,
            random=random,
            config=resolved,
            counterparties=counterparties,
            instruments=instruments,
        )
        if index <= resolved.exception_count:
            family = families[(index - 1) % len(families)]
            escalation = ((index - 1) // len(families)) % 2 == 1
            seeded = _seed_exception(
                baseline,
                family=family,
                escalation=escalation,
                config=resolved,
                counterparties=counterparties,
                instruments=instruments,
                first_trade=trades[0] if trades else baseline,
            )
            trades.append(seeded)
            scenarios.append(
                SeededScenario(
                    trade_id=seeded.trade_id,
                    expected_exception=family,
                    escalation=escalation,
                    expected_financials=_expected(baseline),
                )
            )
        else:
            trades.append(baseline)

    return SyntheticDataset(
        seed=resolved.seed,
        generated_at=resolved.generated_at,
        counterparties=counterparties,
        instruments=instruments,
        trades=tuple(trades),
        scenarios=tuple(scenarios),
    )
