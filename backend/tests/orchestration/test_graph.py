"""Workflow routing, interrupt, resume, and escalation tests."""

from langchain_core.runnables import RunnableConfig
from langgraph.types import Command

from tradeops.orchestration.graph import WorkflowState, build_workflow


def _state(**updates: object) -> WorkflowState:
    state: WorkflowState = {
        "workflow_id": "WF-DEMO-000001",
        "exception_id": "EXC-DEMO-000001",
        "exception_type": "currency_mismatch",
        "evidence": ("trade=EUR", "reference=USD"),
        "requested_action": "propose_demo_field_correction",
        "payload_valid": True,
        "evidence_malicious": False,
        "deterministic_valid": True,
        "steps": [],
        "workflow_version": "workflow-v1",
        "prompt_version": "prompt-v1",
    }
    state.update(updates)  # type: ignore[typeddict-item]
    return state


def test_workflow_interrupts_and_resumes_approved_resolution() -> None:
    graph = build_workflow()
    config = RunnableConfig(configurable={"thread_id": "WF-DEMO-000001"})

    paused = graph.invoke(_state(), config)
    completed = graph.invoke(Command[object](resume={"decision": "approve"}), config)

    assert "__interrupt__" in paused
    assert completed["status"] == "resolved"
    assert completed["resolution_applied"] is True
    assert completed["steps"] == [
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
    ]


def test_edit_and_reject_resume_paths_never_bypass_review() -> None:
    graph = build_workflow()
    edit_config = RunnableConfig(configurable={"thread_id": "edit"})
    graph.invoke(_state(workflow_id="edit"), edit_config)
    edited = graph.invoke(
        Command[object](resume={"decision": "edit", "edit": "currency=USD"}), edit_config
    )

    reject_config = RunnableConfig(configurable={"thread_id": "reject"})
    graph.invoke(_state(workflow_id="reject"), reject_config)
    rejected = graph.invoke(Command[object](resume={"decision": "reject"}), reject_config)

    assert edited["approved_edit"] == "currency=USD"
    assert edited["resolution_applied"] is True
    assert rejected["status"] == "reject"
    assert rejected.get("resolution_applied") is not True


def test_invalid_malicious_and_failed_validation_cases_escalate() -> None:
    graph = build_workflow()
    cases = (
        (_state(payload_valid=False), "invalid_payload"),
        (_state(evidence_malicious=True), "malicious_or_insufficient_evidence"),
        (_state(deterministic_valid=False), "deterministic_validation_failed"),
    )
    for index, (state, reason) in enumerate(cases):
        completed = graph.invoke(
            state, RunnableConfig(configurable={"thread_id": f"failure-{index}"})
        )
        assert completed["status"] == "escalated"
        assert completed["escalation_reason"] == reason
        assert "safe_resolution_executor" not in completed["steps"]
