"""Versioned, deterministic mock evaluation dataset."""

from dataclasses import dataclass
from typing import Literal

CaseType = Literal[
    "normal",
    "ambiguous",
    "missing_evidence",
    "contradictory_evidence",
    "malicious_document",
    "provider_failure",
    "escalation",
]


@dataclass(frozen=True, slots=True)
class GoldenCase:
    id: str
    case_type: CaseType
    exception_type: str
    expected_status: Literal["review_required", "escalated"]
    evidence: tuple[str, ...]
    provider_available: bool = True
    malicious: bool = False


@dataclass(frozen=True, slots=True)
class BaselineResult:
    dataset_version: str
    prompt_version: str
    provider: str
    model: str
    total: int
    passed: int
    failed: int


_CASE_TYPES: tuple[CaseType, ...] = (
    "normal",
    "ambiguous",
    "missing_evidence",
    "contradictory_evidence",
    "malicious_document",
    "provider_failure",
    "escalation",
)


def build_golden_dataset() -> tuple[GoldenCase, ...]:
    """Return exactly 50 independently named synthetic evaluation cases."""

    cases: list[GoldenCase] = []
    for ordinal in range(50):
        case_type = _CASE_TYPES[ordinal % len(_CASE_TYPES)]
        escalates = case_type != "normal"
        cases.append(
            GoldenCase(
                id=f"golden-v1-{ordinal + 1:03d}",
                case_type=case_type,
                exception_type=(
                    "settlement_date_mismatch" if ordinal % 2 == 0 else "counterparty_name_mismatch"
                ),
                expected_status="escalated" if escalates else "review_required",
                evidence=(f"synthetic-policy-{(ordinal % 30) + 1:02d}",),
                provider_available=case_type != "provider_failure",
                malicious=case_type == "malicious_document",
            )
        )
    return tuple(cases)


def run_mock_baseline() -> BaselineResult:
    """Evaluate the deterministic expected routing contract without a model key."""

    cases = build_golden_dataset()
    passed = sum(
        1
        for case in cases
        if ("escalated" if case.case_type != "normal" else "review_required")
        == case.expected_status
    )
    return BaselineResult(
        dataset_version="golden-v1",
        prompt_version="prompt-v1",
        provider="mock",
        model="deterministic-v1",
        total=len(cases),
        passed=passed,
        failed=len(cases) - passed,
    )
