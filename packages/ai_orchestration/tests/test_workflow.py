"""Explicit graph shape and deterministic routing tests."""

from hashlib import sha256

import pytest

from tradeops_ai.provider import AdvisoryRequest, AdvisoryTask, EvidenceSnippet
from tradeops_ai.providers.mock import MockAdvisoryProvider
from tradeops_ai.workflow import build_workflow, initial_state, typed_result


@pytest.fixture
def anyio_backend() -> str:
    return "asyncio"


def _request(*, with_evidence: bool) -> AdvisoryRequest:
    content = "A synthetic price correction requires confirmation evidence and supervisor review."
    evidence = (
        EvidenceSnippet(
            chunk_id="RUNBOOK-DEMO-001:v1:0000",
            title="Synthetic price runbook",
            content=content,
            source_locator="repo://data/policies/price.md",
            content_sha256=sha256(content.encode()).hexdigest(),
        ),
    )
    return AdvisoryRequest(
        request_id="request-workflow-1",
        task=AdvisoryTask.RESOLUTION_DRAFT,
        case_summary="Synthetic price exceeds tolerance.",
        deterministic_findings=("price_tolerance_breach",),
        evidence=evidence if with_evidence else (),
        allowed_actions=("propose_demo_price_correction",),
    )


def test_graph_exposes_all_required_nodes() -> None:
    graph = build_workflow(MockAdvisoryProvider()).get_graph()

    assert {
        "intake_validation",
        "deterministic_reconciliation",
        "memo_nlp_analysis",
        "triage_classifier",
        "reference_enrichment",
        "evidence_retrieval",
        "resolution_planner",
        "policy_and_risk_validator",
        "confidence_and_citation_gate",
        "human_review_interrupt",
        "safe_resolution_executor",
        "audit_and_finalize",
        "failure_and_escalation",
    } <= set(graph.nodes)


@pytest.mark.anyio
async def test_grounded_material_proposal_stops_for_review() -> None:
    graph = build_workflow(MockAdvisoryProvider())
    result = typed_result(
        await graph.ainvoke(
            initial_state(workflow_id="workflow-1", request=_request(with_evidence=True))
        )
    )

    assert result["status"] == "awaiting_review"
    assert result["citations_valid"] is True
    assert result["visited_nodes"][-1] == "human_review_interrupt"
    assert "safe_resolution_executor" not in result["visited_nodes"]


@pytest.mark.anyio
async def test_refusal_routes_to_failure_and_escalation() -> None:
    graph = build_workflow(MockAdvisoryProvider())
    result = typed_result(
        await graph.ainvoke(
            initial_state(workflow_id="workflow-2", request=_request(with_evidence=False))
        )
    )

    assert result["status"] == "escalated"
    assert result["error_code"] in {"ADVISORY_REFUSED", "EVIDENCE_GATE_FAILED"}
    assert result["visited_nodes"][-1] == "failure_and_escalation"


@pytest.mark.anyio
async def test_explicit_low_risk_policy_can_reach_demo_executor() -> None:
    graph = build_workflow(MockAdvisoryProvider())
    result = typed_result(
        await graph.ainvoke(
            initial_state(
                workflow_id="workflow-3",
                request=_request(with_evidence=True),
                disposition="allow_demo",
            )
        )
    )

    assert result["status"] == "completed"
    assert result["visited_nodes"][-2:] == ["safe_resolution_executor", "audit_and_finalize"]
