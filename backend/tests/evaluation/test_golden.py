"""Golden evaluation dataset tests."""

from tradeops.evaluation import build_golden_dataset, run_mock_baseline


def test_golden_dataset_has_required_size_and_categories() -> None:
    cases = build_golden_dataset()

    assert len(cases) == 50
    assert len({case.id for case in cases}) == 50
    assert {case.case_type for case in cases} == {
        "normal",
        "ambiguous",
        "missing_evidence",
        "contradictory_evidence",
        "malicious_document",
        "provider_failure",
        "escalation",
    }


def test_mock_baseline_is_replayable() -> None:
    result = run_mock_baseline()

    assert result.total == 50
    assert result.passed == 50
    assert result.failed == 0
    assert result.provider == "mock"
