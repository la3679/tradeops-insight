"""Catalogue and deterministic dataset acceptance tests."""

from dataclasses import replace
from datetime import timedelta
from decimal import Decimal

import pytest

from tradeops.domain.exceptions import ExceptionType, ReviewRoute
from tradeops.domain.reconciliation import ReconciliationPolicy, evaluate_reconciliation
from tradeops.domain.synthetic import generate_synthetic_dataset


def test_generator_is_reproducible_and_covers_every_exception_type() -> None:
    first = generate_synthetic_dataset(seed=42, size=96)
    second = generate_synthetic_dataset(seed=42, size=96)

    observed = {exception_type for labels in first.expected_types for exception_type in labels}

    assert first == second
    assert observed == set(ExceptionType)


def test_default_dataset_meets_documented_volume_and_exception_bounds() -> None:
    dataset = generate_synthetic_dataset()

    exception_bearing_trades = sum(bool(labels) for labels in dataset.expected_types)

    assert len(dataset.trades) == 2_400
    assert 250 <= exception_bearing_trades <= 500
    assert len({trade.reference.counterparty_lei for trade in dataset.trades}) >= 100
    assert len({trade.reference.instrument_id for trade in dataset.trades}) >= 100


def test_each_exception_type_has_review_and_escalation_examples() -> None:
    dataset = generate_synthetic_dataset(size=288)
    routes: dict[ExceptionType, set[ReviewRoute]] = {
        exception_type: set() for exception_type in ExceptionType
    }
    for trade in dataset.trades:
        for finding in evaluate_reconciliation(trade, ReconciliationPolicy()):
            routes[finding.exception_type].add(finding.review_route)

    assert all(
        values == {ReviewRoute.REVIEW_CORRECTION, ReviewRoute.ESCALATE}
        for values in routes.values()
    )


def test_policy_rejects_invalid_tolerances_and_time_context() -> None:
    base = ReconciliationPolicy()

    with pytest.raises(ValueError, match="numeric tolerances"):
        replace(base, price_tolerance=Decimal("-1"))
    with pytest.raises(ValueError, match="reference_max_age"):
        replace(base, reference_max_age=timedelta(days=-1))
    with pytest.raises(ValueError, match="timezone-aware UTC"):
        replace(base, as_of=base.as_of.replace(tzinfo=None))


def test_clean_baseline_has_no_findings_and_minimum_size_is_enforced() -> None:
    dataset = generate_synthetic_dataset(size=24)
    clean = replace(dataset.trades[-1], duplicate_trade=False, duplicate_event=False)

    # The final fixture is intentionally injected; reconstruct its supported payload.
    clean = replace(clean, product_type="government_bond", malformed_payload=False)

    assert evaluate_reconciliation(clean, ReconciliationPolicy()) == ()
    with pytest.raises(ValueError, match="at least 24"):
        generate_synthetic_dataset(size=23)
