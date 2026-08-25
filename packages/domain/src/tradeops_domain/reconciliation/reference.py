"""Instrument, currency, product, and reference-freshness rules."""

import re
from dataclasses import dataclass
from datetime import UTC, datetime, timedelta

from tradeops_domain.errors import DomainValidationError
from tradeops_domain.exceptions import (
    DetectedException,
    Evidence,
    ExceptionType,
    RiskLevel,
    Severity,
)
from tradeops_domain.models import (
    CounterpartyReference,
    InstrumentReference,
    ProductType,
    SyntheticTrade,
)

_ISO_CURRENCY = re.compile(r"^[A-Z]{3}$")


@dataclass(frozen=True, slots=True, kw_only=True)
class ReferencePolicy:
    """Versionable deterministic thresholds for reference reconciliation."""

    maximum_age: timedelta = timedelta(days=7)

    def __post_init__(self) -> None:
        if self.maximum_age <= timedelta(0):
            raise DomainValidationError(field="maximum_age", reason="must be positive")


def _unsupported_product(trade: SyntheticTrade) -> DetectedException:
    return DetectedException(
        exception_type=ExceptionType.UNSUPPORTED_OR_MALFORMED_PAYLOAD,
        severity=Severity.HIGH,
        risk=RiskLevel.HIGH,
        explanation="The product type is outside the initial synthetic fixed-income scope.",
        suggested_actions=(
            "Verify the product mapping in the synthetic import.",
            "Escalate rather than coercing an unsupported product.",
        ),
        evidence=(
            Evidence(
                code="PRODUCT_UNSUPPORTED",
                summary="Product type is not in the configured allowlist.",
                facts=(("trade_id", trade.trade_id), ("product_type", trade.product_type)),
            ),
        ),
        requires_review=True,
    )


def _instrument_mismatch(
    trade: SyntheticTrade,
    reference: InstrumentReference | None,
) -> DetectedException:
    facts = [("trade_id", trade.trade_id), ("instrument_id", trade.instrument_id)]
    if reference is not None:
        facts.extend(
            [
                ("observed_product", trade.product_type),
                ("reference_product", reference.product_type.value),
            ]
        )
    return DetectedException(
        exception_type=ExceptionType.INSTRUMENT_MISMATCH,
        severity=Severity.HIGH,
        risk=RiskLevel.HIGH,
        explanation=(
            "The synthetic instrument is unknown or its product type conflicts with reference data."
        ),
        suggested_actions=(
            "Review the synthetic instrument mapping.",
            "Refresh reference data before proposing a correction.",
        ),
        evidence=(
            Evidence(
                code="INSTRUMENT_REFERENCE_MISMATCH",
                summary="Instrument lookup or product comparison failed.",
                facts=tuple(facts),
            ),
        ),
        requires_review=True,
    )


def _currency_mismatch(
    trade: SyntheticTrade,
    reference: InstrumentReference | None,
) -> DetectedException:
    expected = reference.currency if reference is not None else "three-letter ISO code"
    return DetectedException(
        exception_type=ExceptionType.CURRENCY_MISMATCH,
        severity=Severity.HIGH,
        risk=RiskLevel.HIGH,
        explanation="The trade currency is malformed or differs from the instrument currency.",
        suggested_actions=(
            "Verify the structured trade currency.",
            "Propose a correction only with matching instrument evidence.",
        ),
        evidence=(
            Evidence(
                code="CURRENCY_MISMATCH",
                summary="Observed and expected currencies differ.",
                facts=(
                    ("trade_id", trade.trade_id),
                    ("observed_currency", trade.currency),
                    ("expected_currency", expected),
                ),
            ),
        ),
        requires_review=True,
    )


def _stale_reference(
    trade: SyntheticTrade,
    stale_sources: list[tuple[str, datetime]],
    maximum_age: timedelta,
) -> DetectedException:
    facts: list[tuple[str, str]] = [
        ("trade_id", trade.trade_id),
        ("maximum_age_seconds", str(int(maximum_age.total_seconds()))),
    ]
    facts.extend((name, timestamp.isoformat()) for name, timestamp in stale_sources)
    return DetectedException(
        exception_type=ExceptionType.STALE_REFERENCE_DATA,
        severity=Severity.MEDIUM,
        risk=RiskLevel.MEDIUM,
        explanation=(
            "One or more required reference records exceed the configured freshness window."
        ),
        suggested_actions=(
            "Request an approved reference-data refresh.",
            "Escalate if a current source is unavailable.",
        ),
        evidence=(
            Evidence(
                code="REFERENCE_DATA_STALE",
                summary="Reference retrieval time is older than policy permits.",
                facts=tuple(facts),
            ),
        ),
        requires_review=True,
    )


def detect_reference_exceptions(
    trade: SyntheticTrade,
    *,
    instrument: InstrumentReference | None,
    counterparty: CounterpartyReference | None,
    evaluated_at: datetime,
    policy: ReferencePolicy | None = None,
) -> tuple[DetectedException, ...]:
    """Return deterministic product, instrument, currency, and freshness exceptions."""

    if evaluated_at.tzinfo is None or evaluated_at.utcoffset() != UTC.utcoffset(evaluated_at):
        raise DomainValidationError(field="evaluated_at", reason="must be timezone-aware UTC")

    resolved_policy = policy or ReferencePolicy()
    detected: list[DetectedException] = []

    try:
        product = ProductType(trade.product_type)
    except ValueError:
        product = None
        detected.append(_unsupported_product(trade))

    if instrument is None or (product is not None and instrument.product_type is not product):
        detected.append(_instrument_mismatch(trade, instrument))

    currency_invalid = _ISO_CURRENCY.fullmatch(trade.currency) is None
    if currency_invalid or (instrument is not None and instrument.currency != trade.currency):
        detected.append(_currency_mismatch(trade, instrument))

    cutoff = evaluated_at - resolved_policy.maximum_age
    candidates = (
        ("instrument_retrieved_at", instrument.retrieved_at if instrument else None),
        ("counterparty_retrieved_at", counterparty.retrieved_at if counterparty else None),
    )
    stale_sources = [
        (name, timestamp)
        for name, timestamp in candidates
        if timestamp is not None and timestamp < cutoff
    ]
    if stale_sources:
        detected.append(_stale_reference(trade, stale_sources, resolved_policy.maximum_age))

    return tuple(detected)
