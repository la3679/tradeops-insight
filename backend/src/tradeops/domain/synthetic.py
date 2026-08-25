"""Seeded synthetic dataset generator; no output represents a real trade."""

import random
from dataclasses import dataclass, replace
from datetime import UTC, date, datetime, timedelta
from decimal import Decimal
from uuid import UUID, uuid5

from tradeops.domain.exceptions import ExceptionType
from tradeops.domain.reconciliation import (
    ReconciliationInput,
    ReconciliationPolicy,
    ReferenceSnapshot,
    evaluate_reconciliation,
)

_NAMESPACE = UUID("5d7774f4-4c12-593e-aab8-f25d01ac0ce4")


@dataclass(frozen=True, slots=True)
class SyntheticDataset:
    """Deterministic trade envelopes and their expected exception labels."""

    seed: int
    trades: tuple[ReconciliationInput, ...]
    expected_types: tuple[tuple[ExceptionType, ...], ...]


def _baseline(index: int, rng: random.Random) -> ReconciliationInput:
    trade_date = date(2026, 1, 12) + timedelta(days=index % 2)
    policy = ReconciliationPolicy()
    instrument = f"INST-DEMO-{index % 100 + 1:06d}"
    lei = f"LEI-DEMO-{index % 100 + 1:06d}"
    currency = ("USD", "EUR", "GBP")[index % 3]
    notional = Decimal(100_000 + rng.randrange(900_000)).quantize(Decimal("0.01"))
    price = Decimal(90 + rng.randrange(2000) / 100).quantize(Decimal("0.01"))
    reference = ReferenceSnapshot(
        counterparty_lei=lei,
        counterparty_name=f"Synthetic Counterparty {index % 100 + 1:03d}",
        counterparty_active=True,
        instrument_id=instrument,
        currency=currency,
        notional=notional,
        price=price,
        observed_at=datetime(2026, 1, 14, tzinfo=UTC),
    )
    return ReconciliationInput(
        trade_id=uuid5(_NAMESPACE, f"trade:{index}"),
        synthetic_trade_id=f"TRD-DEMO-{index + 1:06d}",
        event_id=f"EVT-DEMO-{index + 1:06d}",
        instrument_id=instrument,
        counterparty_lei=lei,
        counterparty_name=reference.counterparty_name,
        product_type=("government_bond", "corporate_bond")[index % 2],
        currency=currency,
        notional=notional,
        price=price,
        trade_date=trade_date,
        settlement_date=policy.settlement.expected_settlement_date(trade_date),
        memo=f"Synthetic memo {instrument} {currency}",
        confirmation_present=True,
        reference=reference,
    )


def _inject(item: ReconciliationInput, scenario: int, escalated: bool) -> ReconciliationInput:
    if scenario == 0:
        return replace(item, counterparty_lei="" if escalated else "BAD-LEI")
    if scenario == 1:
        return replace(item, counterparty_name="" if escalated else "Contradictory Synthetic Name")
    if scenario == 2:
        return (
            replace(item, counterparty_lei="LEI-DEMO-999999")
            if escalated
            else replace(item, reference=replace(item.reference, counterparty_active=False))
        )
    if scenario == 3:
        return replace(item, instrument_id="UNKNOWN" if escalated else "INST-DEMO-999999")
    if scenario == 4:
        delta = Decimal("200000") if escalated else Decimal("1")
        return replace(item, notional=item.notional + delta)
    if scenario == 5:
        delta = Decimal("5") if escalated else Decimal("1")
        return replace(item, price=item.price + delta)
    if scenario == 6:
        candidate = "JPY" if escalated else ("EUR" if item.reference.currency != "EUR" else "USD")
        return replace(item, currency=candidate)
    if scenario == 7:
        days = -5 if escalated else 1
        return replace(item, settlement_date=item.settlement_date + timedelta(days=days))
    if scenario == 8:
        return replace(item, duplicate_trade=True, duplicate_event=escalated)
    if scenario == 9:
        return replace(item, confirmation_present=not escalated, memo="Contradictory memo")
    if scenario == 10:
        age = 30 if escalated else 8
        return replace(
            item,
            reference=replace(
                item.reference, observed_at=datetime(2026, 1, 15, tzinfo=UTC) - timedelta(days=age)
            ),
        )
    return replace(item, product_type="unsupported_swap", malformed_payload=escalated)


def generate_synthetic_dataset(*, seed: int = 20260115, size: int = 2_400) -> SyntheticDataset:
    """Generate a stable set with normal trades and paired cases for all scenarios."""

    if size < 24:
        raise ValueError("size must be at least 24 so every scenario has two examples")
    rng = random.Random(seed)
    policy = ReconciliationPolicy()
    trades: list[ReconciliationInput] = []
    labels: list[tuple[ExceptionType, ...]] = []
    exception_count = max(24, min(size, size // 8))
    for index in range(size):
        item = _baseline(index, rng)
        if index < exception_count:
            item = _inject(item, index % 12, escalated=(index // 12) % 2 == 1)
        findings = evaluate_reconciliation(item, policy)
        trades.append(item)
        labels.append(tuple(finding.exception_type for finding in findings))
    return SyntheticDataset(seed=seed, trades=tuple(trades), expected_types=tuple(labels))
