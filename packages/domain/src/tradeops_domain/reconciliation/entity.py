"""Legal-entity reconciliation rules."""

import re
import unicodedata
from collections.abc import Mapping

from tradeops_domain.exceptions import (
    DetectedException,
    Evidence,
    ExceptionType,
    RiskLevel,
    Severity,
)
from tradeops_domain.models import CounterpartyReference, EntityStatus, SyntheticTrade

_LEI = re.compile(r"^[A-Z0-9]{20}$")


def _lei_modulus(lei: str) -> int:
    expanded = "".join(str(int(character, 36)) for character in lei)
    remainder = 0
    for offset in range(0, len(expanded), 9):
        remainder = int(f"{remainder}{expanded[offset : offset + 9]}") % 97
    return remainder


def _is_valid_lei(value: str | None) -> bool:
    return value is not None and _LEI.fullmatch(value) is not None and _lei_modulus(value) == 1


def _normalize_name(value: str) -> str:
    normalized = unicodedata.normalize("NFKC", value).casefold()
    return "".join(character for character in normalized if character.isalnum())


def _lei_exception(trade: SyntheticTrade) -> DetectedException:
    displayed = trade.counterparty_lei or "missing"
    return DetectedException(
        exception_type=ExceptionType.MISSING_OR_INVALID_LEI,
        severity=Severity.HIGH,
        risk=RiskLevel.HIGH,
        explanation="The trade has no valid ISO 17442-shaped counterparty LEI.",
        suggested_actions=(
            "Verify the synthetic counterparty reference record.",
            "Submit a corrected LEI for supervisor review.",
        ),
        evidence=(
            Evidence(
                code="COUNTERPARTY_LEI_INVALID",
                summary="Counterparty LEI is missing or fails format/check-digit validation.",
                facts=(("trade_id", trade.trade_id), ("observed_lei", displayed)),
            ),
        ),
        requires_review=True,
    )


def _unknown_entity_exception(trade: SyntheticTrade) -> DetectedException:
    return DetectedException(
        exception_type=ExceptionType.UNKNOWN_OR_INACTIVE_ENTITY,
        severity=Severity.HIGH,
        risk=RiskLevel.HIGH,
        explanation=(
            "The valid-shaped counterparty LEI is absent from the approved reference snapshot."
        ),
        suggested_actions=(
            "Refresh the approved legal-entity source.",
            "Escalate if the entity remains unknown.",
        ),
        evidence=(
            Evidence(
                code="COUNTERPARTY_UNKNOWN",
                summary="No counterparty reference record matched the supplied LEI.",
                facts=(("trade_id", trade.trade_id), ("lei", trade.counterparty_lei or "")),
            ),
        ),
        requires_review=True,
    )


def _inactive_entity_exception(
    trade: SyntheticTrade,
    reference: CounterpartyReference,
) -> DetectedException:
    return DetectedException(
        exception_type=ExceptionType.UNKNOWN_OR_INACTIVE_ENTITY,
        severity=Severity.CRITICAL,
        risk=RiskLevel.CRITICAL,
        explanation="The counterparty reference is present but marked inactive.",
        suggested_actions=(
            "Stop automated demo resolution.",
            "Escalate to a supervisor with the reference version.",
        ),
        evidence=(
            Evidence(
                code="COUNTERPARTY_INACTIVE",
                summary="Approved reference data reports an inactive legal entity.",
                facts=(
                    ("trade_id", trade.trade_id),
                    ("lei", reference.lei),
                    ("source_version", reference.source_version),
                ),
            ),
        ),
        requires_review=True,
    )


def _name_mismatch_exception(
    trade: SyntheticTrade,
    reference: CounterpartyReference,
) -> DetectedException:
    return DetectedException(
        exception_type=ExceptionType.LEGAL_NAME_MISMATCH,
        severity=Severity.MEDIUM,
        risk=RiskLevel.MEDIUM,
        explanation=(
            "The trade counterparty name does not match the legal name or an approved alias."
        ),
        suggested_actions=(
            "Review the reference legal name and approved aliases.",
            "Propose a synthetic name correction with evidence.",
        ),
        evidence=(
            Evidence(
                code="COUNTERPARTY_NAME_MISMATCH",
                summary="Normalized legal names differ.",
                facts=(
                    ("trade_id", trade.trade_id),
                    ("observed_name", trade.counterparty_name),
                    ("reference_name", reference.legal_name),
                ),
            ),
        ),
        requires_review=True,
    )


def detect_entity_exceptions(
    trade: SyntheticTrade,
    counterparties_by_lei: Mapping[str, CounterpartyReference],
) -> tuple[DetectedException, ...]:
    """Return deterministic legal-entity exceptions for one trade."""

    if not _is_valid_lei(trade.counterparty_lei):
        return (_lei_exception(trade),)

    assert trade.counterparty_lei is not None
    reference = counterparties_by_lei.get(trade.counterparty_lei)
    if reference is None:
        return (_unknown_entity_exception(trade),)

    detected: list[DetectedException] = []
    if reference.status is EntityStatus.INACTIVE:
        detected.append(_inactive_entity_exception(trade, reference))

    accepted_names = (reference.legal_name, *reference.aliases)
    observed = _normalize_name(trade.counterparty_name)
    if all(observed != _normalize_name(candidate) for candidate in accepted_names):
        detected.append(_name_mismatch_exception(trade, reference))

    return tuple(detected)
