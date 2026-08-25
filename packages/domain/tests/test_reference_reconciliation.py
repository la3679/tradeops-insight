"""Instrument and reference reconciliation scenarios."""

from dataclasses import replace
from datetime import UTC, datetime, timedelta

import pytest
from test_entity_reconciliation import _reference
from test_models import make_trade

from tradeops_domain.errors import DomainValidationError
from tradeops_domain.exceptions import ExceptionType
from tradeops_domain.models import InstrumentReference, ProductType
from tradeops_domain.reconciliation.reference import (
    ReferencePolicy,
    detect_reference_exceptions,
)

EVALUATED_AT = datetime(2026, 8, 24, 18, tzinfo=UTC)


def _instrument(*, retrieved_at: datetime = EVALUATED_AT) -> InstrumentReference:
    return InstrumentReference(
        instrument_id="INST-DEMO-000001",
        product_type=ProductType.CORPORATE_BOND,
        currency="USD",
        issuer_lei=None,
        retrieved_at=retrieved_at,
    )


def test_current_matching_reference_has_no_exception() -> None:
    assert (
        detect_reference_exceptions(
            make_trade(),
            instrument=_instrument(),
            counterparty=_reference(),
            evaluated_at=EVALUATED_AT,
        )
        == ()
    )


def test_unknown_instrument_is_detected() -> None:
    detected = detect_reference_exceptions(
        make_trade(),
        instrument=None,
        counterparty=_reference(),
        evaluated_at=EVALUATED_AT,
    )

    assert detected[0].exception_type is ExceptionType.INSTRUMENT_MISMATCH


def test_instrument_product_mismatch_is_detected() -> None:
    instrument = replace(_instrument(), product_type=ProductType.GOVERNMENT_BOND)
    detected = detect_reference_exceptions(
        make_trade(),
        instrument=instrument,
        counterparty=_reference(),
        evaluated_at=EVALUATED_AT,
    )

    assert detected[0].evidence[0].code == "INSTRUMENT_REFERENCE_MISMATCH"


def test_unsupported_product_and_bad_currency_are_independent() -> None:
    trade = replace(make_trade(), product_type="demo_swap", currency="US_DOLL")
    detected = detect_reference_exceptions(
        trade,
        instrument=_instrument(),
        counterparty=_reference(),
        evaluated_at=EVALUATED_AT,
    )

    assert [finding.exception_type for finding in detected] == [
        ExceptionType.UNSUPPORTED_OR_MALFORMED_PAYLOAD,
        ExceptionType.CURRENCY_MISMATCH,
    ]


def test_reference_currency_mismatch_is_explainable() -> None:
    detected = detect_reference_exceptions(
        replace(make_trade(), currency="EUR"),
        instrument=_instrument(),
        counterparty=_reference(),
        evaluated_at=EVALUATED_AT,
    )

    assert detected[0].evidence[0].facts[-1] == ("expected_currency", "USD")


def test_stale_sources_are_combined_in_one_exception() -> None:
    stale_time = EVALUATED_AT - timedelta(days=8)
    detected = detect_reference_exceptions(
        make_trade(),
        instrument=_instrument(retrieved_at=stale_time),
        counterparty=replace(_reference(), retrieved_at=stale_time),
        evaluated_at=EVALUATED_AT,
    )

    stale = detected[0]
    assert stale.exception_type is ExceptionType.STALE_REFERENCE_DATA
    assert len(stale.evidence[0].facts) == 4


def test_reference_policy_rejects_nonpositive_age() -> None:
    with pytest.raises(DomainValidationError, match="maximum_age"):
        ReferencePolicy(maximum_age=timedelta(0))


def test_reconciliation_requires_utc_evaluation_time() -> None:
    with pytest.raises(DomainValidationError, match="evaluated_at"):
        detect_reference_exceptions(
            make_trade(),
            instrument=_instrument(),
            counterparty=_reference(),
            evaluated_at=datetime(2026, 8, 24),  # noqa: DTZ001 - negative test input
        )
