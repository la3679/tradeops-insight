"""Complete deterministic reconciliation facade tests."""

from dataclasses import replace
from datetime import UTC, date, datetime
from decimal import Decimal

import pytest
from test_entity_reconciliation import _lei, _reference
from test_financial_reconciliation import _expected
from test_models import make_trade
from test_reference_reconciliation import _instrument

from tradeops_domain.errors import DomainValidationError
from tradeops_domain.exceptions import ExceptionType
from tradeops_domain.models import EntityStatus, ProductType
from tradeops_domain.reconciliation.content import MemoConflict, PayloadIssue
from tradeops_domain.reconciliation.lifecycle import trade_fingerprint
from tradeops_domain.reconciliation.reconciler import ReconciliationContext, reconcile_trade

EVALUATED_AT = datetime(2026, 8, 24, 18, tzinfo=UTC)


def _clean_context() -> ReconciliationContext:
    reference = _reference()
    return ReconciliationContext(
        counterparties_by_lei={reference.lei: reference},
        instrument=_instrument(),
        expected_financials=_expected(),
        evaluated_at=EVALUATED_AT,
        seen_event_ids=frozenset(),
        seen_trade_fingerprints=frozenset(),
    )


def test_clean_trade_has_empty_report() -> None:
    reference = _reference()
    trade = replace(make_trade(), counterparty_lei=reference.lei)

    report = reconcile_trade(trade, _clean_context())

    assert report.trade_id == trade.trade_id
    assert report.findings == ()


def test_golden_scenarios_cover_all_twelve_families() -> None:
    reference = replace(
        _reference(status=EntityStatus.INACTIVE),
        retrieved_at=datetime(2026, 8, 1, tzinfo=UTC),
    )
    compound = replace(
        make_trade(),
        counterparty_lei=reference.lei,
        counterparty_name="Different Demo Name",
        product_type=ProductType.CORPORATE_BOND,
        currency="EUR",
        quantity=Decimal("900000.0000"),
        notional=Decimal("900000.00"),
        price=Decimal("100.000000"),
        settlement_date=date(2026, 8, 27),
        confirmation_received=False,
    )
    context = ReconciliationContext(
        counterparties_by_lei={reference.lei: reference},
        instrument=replace(
            _instrument(retrieved_at=datetime(2026, 8, 1, tzinfo=UTC)),
            product_type=ProductType.GOVERNMENT_BOND,
        ),
        expected_financials=_expected(),
        evaluated_at=EVALUATED_AT,
        seen_event_ids={compound.event_id},
        seen_trade_fingerprints={trade_fingerprint(compound)},
        memo_conflicts=(
            MemoConflict(
                field="price",
                observed="101.0",
                expected="100.0",
                confidence=Decimal("0.99"),
                extractor_version="patterns-v1",
            ),
        ),
        payload_issues=(
            PayloadIssue(field="payload", reason="unexpected business field", recoverable=False),
        ),
    )
    findings = list(reconcile_trade(compound, context).findings)

    invalid_lei = replace(make_trade(), counterparty_lei="bad-lei")
    findings.extend(reconcile_trade(invalid_lei, _clean_context()).findings)

    unknown_lei = replace(make_trade(), counterparty_lei=_lei("DEMOLEI00000000002"))
    findings.extend(reconcile_trade(unknown_lei, _clean_context()).findings)

    assert {finding.exception_type for finding in findings} == set(ExceptionType)


def test_context_requires_utc_time() -> None:
    with pytest.raises(DomainValidationError, match="evaluated_at"):
        replace(_clean_context(), evaluated_at=datetime(2026, 8, 24))  # noqa: DTZ001
