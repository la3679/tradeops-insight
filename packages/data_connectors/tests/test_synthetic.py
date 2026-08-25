"""Deterministic synthetic dataset generation tests."""

from collections import Counter
from collections.abc import Callable
from dataclasses import replace

import pytest

from tradeops_data.synthetic import GeneratorConfig, generate_dataset
from tradeops_domain.errors import DomainValidationError
from tradeops_domain.exceptions import ExceptionType


def _fast_config(seed: int = 42) -> GeneratorConfig:
    return GeneratorConfig(
        seed=seed,
        counterparty_count=12,
        instrument_count=12,
        trade_count=120,
        exception_count=24,
    )


def test_same_seed_produces_identical_dataset() -> None:
    first = generate_dataset(_fast_config())
    second = generate_dataset(_fast_config())

    assert first == second


def test_different_seed_changes_clean_trade_assignment() -> None:
    first = generate_dataset(_fast_config(seed=1))
    second = generate_dataset(_fast_config(seed=2))

    assert first.trades[-1] != second.trades[-1]


def test_fast_dataset_has_reserved_identifiers_and_counts() -> None:
    dataset = generate_dataset(_fast_config())

    assert len(dataset.counterparties) == 12
    assert len(dataset.instruments) == 12
    assert len(dataset.trades) == 120
    assert len(dataset.scenarios) == 24
    assert dataset.trades[0].trade_id == "TRD-DEMO-000001"
    assert dataset.instruments[-1].instrument_id == "INST-DEMO-000012"


def test_each_exception_family_has_resolvable_and_escalation_scenario() -> None:
    dataset = generate_dataset(_fast_config())
    counts = Counter(
        (scenario.expected_exception, scenario.escalation) for scenario in dataset.scenarios
    )

    assert set(counts) == {
        (family, escalation) for family in ExceptionType for escalation in (False, True)
    }


def test_default_config_matches_portfolio_scale() -> None:
    config = GeneratorConfig()

    assert config.counterparty_count == 100
    assert config.instrument_count == 100
    assert 2_000 <= config.trade_count <= 5_000
    assert 250 <= config.exception_count <= 500


@pytest.mark.parametrize(
    "factory",
    [
        lambda: replace(_fast_config(), counterparty_count=3),
        lambda: replace(_fast_config(), instrument_count=3),
        lambda: replace(_fast_config(), trade_count=23),
        lambda: replace(_fast_config(), exception_count=23),
        lambda: replace(_fast_config(), exception_count=121),
    ],
)
def test_config_rejects_unsafe_counts(factory: Callable[[], GeneratorConfig]) -> None:
    with pytest.raises(DomainValidationError):
        factory()
