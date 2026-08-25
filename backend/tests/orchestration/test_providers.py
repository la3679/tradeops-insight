"""Model provider fallback and circuit-breaker tests."""

import pytest

from tradeops.orchestration.providers import (
    MockModelProvider,
    ProviderUnavailable,
    ResilientModelProvider,
    UnavailableModelProvider,
)


def test_mock_provider_is_deterministic_and_requires_evidence() -> None:
    provider = MockModelProvider()

    classification = provider.classify("currency_mismatch", ("trade=USD",))
    draft = provider.draft_resolution("currency_mismatch", ("trade=USD",))

    assert classification.confidence == 0.92
    assert classification.model == "mock-v1"
    assert draft.action == "propose_demo_field_correction"
    assert provider.classify("currency_mismatch", ()).confidence == 0.0
    with pytest.raises(ProviderUnavailable, match="requires evidence"):
        provider.draft_resolution("currency_mismatch", ())


def test_outage_falls_back_explicitly_and_opens_circuit() -> None:
    provider = ResilientModelProvider(UnavailableModelProvider(), failure_threshold=1)

    classification = provider.classify("currency_mismatch", ("evidence",))
    draft = provider.draft_resolution("currency_mismatch", ("evidence",))

    assert classification.provider == "mock-fallback"
    assert draft.provider == "mock-fallback"
    assert provider.name == "mock-fallback"
    with pytest.raises(ValueError, match="positive"):
        ResilientModelProvider(MockModelProvider(), failure_threshold=0)


def test_unavailable_provider_raises_for_both_capabilities() -> None:
    provider = UnavailableModelProvider()
    with pytest.raises(ProviderUnavailable):
        provider.classify("type", ())
    with pytest.raises(ProviderUnavailable):
        provider.draft_resolution("type", ())
