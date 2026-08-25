"""Legal-entity reconciliation scenarios."""

from dataclasses import replace
from datetime import UTC, datetime

from test_models import make_trade

from tradeops_domain.exceptions import ExceptionType, Severity
from tradeops_domain.models import CounterpartyReference, EntityStatus
from tradeops_domain.reconciliation.entity import detect_entity_exceptions


def _lei(prefix: str = "DEMOLEI00000000001") -> str:
    expanded = "".join(str(int(character, 36)) for character in f"{prefix}00")
    check_digits = 98 - (int(expanded) % 97)
    return f"{prefix}{check_digits:02d}"


def _reference(*, status: EntityStatus = EntityStatus.ACTIVE) -> CounterpartyReference:
    return CounterpartyReference(
        lei=_lei(),
        legal_name="Northstar Demo Capital LLC",
        aliases=("Northstar Demo Capital",),
        status=status,
        retrieved_at=datetime(2026, 8, 24, tzinfo=UTC),
        source_version="fixture-1",
    )


def test_matching_active_entity_has_no_exception() -> None:
    reference = _reference()
    trade = replace(make_trade(), counterparty_lei=reference.lei)

    assert detect_entity_exceptions(trade, {reference.lei: reference}) == ()


def test_missing_lei_is_high_risk_review_exception() -> None:
    detected = detect_entity_exceptions(replace(make_trade(), counterparty_lei=None), {})

    assert detected[0].exception_type is ExceptionType.MISSING_OR_INVALID_LEI
    assert detected[0].severity is Severity.HIGH
    assert detected[0].requires_review is True


def test_bad_check_digits_are_invalid() -> None:
    detected = detect_entity_exceptions(
        replace(make_trade(), counterparty_lei="DEMOLEI0000000000100"),
        {},
    )

    assert detected[0].evidence[0].code == "COUNTERPARTY_LEI_INVALID"


def test_valid_unknown_lei_escalates() -> None:
    detected = detect_entity_exceptions(replace(make_trade(), counterparty_lei=_lei()), {})

    assert detected[0].exception_type is ExceptionType.UNKNOWN_OR_INACTIVE_ENTITY
    assert detected[0].evidence[0].code == "COUNTERPARTY_UNKNOWN"


def test_inactive_entity_is_critical() -> None:
    reference = _reference(status=EntityStatus.INACTIVE)
    trade = replace(make_trade(), counterparty_lei=reference.lei)

    detected = detect_entity_exceptions(trade, {reference.lei: reference})

    assert detected[0].severity is Severity.CRITICAL
    assert detected[0].evidence[0].code == "COUNTERPARTY_INACTIVE"


def test_legal_name_mismatch_is_explainable() -> None:
    reference = _reference()
    trade = replace(
        make_trade(),
        counterparty_lei=reference.lei,
        counterparty_name="Different Demo Entity",
    )

    detected = detect_entity_exceptions(trade, {reference.lei: reference})

    assert detected[0].exception_type is ExceptionType.LEGAL_NAME_MISMATCH
    assert detected[0].evidence[0].facts[-1] == (
        "reference_name",
        "Northstar Demo Capital LLC",
    )
