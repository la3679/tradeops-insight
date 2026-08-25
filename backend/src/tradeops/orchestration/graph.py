"""Explicit typed LangGraph workflow with mandatory human review before mutation."""

import operator
from typing import Annotated, Literal, NotRequired, TypedDict, cast

from langgraph.checkpoint.base import BaseCheckpointSaver
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.graph import END, START, StateGraph
from langgraph.graph.state import CompiledStateGraph
from langgraph.types import interrupt

from tradeops.orchestration.providers import MockModelProvider, ModelProvider

Decision = Literal["approve", "edit", "reject", "request_more_evidence", "escalate"]


class WorkflowState(TypedDict):
    """Versioned workflow state; steps use an append reducer across checkpoints."""

    workflow_id: str
    exception_id: str
    exception_type: str
    evidence: tuple[str, ...]
    requested_action: str
    payload_valid: bool
    evidence_malicious: bool
    deterministic_valid: bool
    steps: Annotated[list[str], operator.add]
    workflow_version: str
    prompt_version: str
    classification: NotRequired[str]
    confidence: NotRequired[float]
    provider: NotRequired[str]
    model: NotRequired[str]
    proposal: NotRequired[str]
    approval: NotRequired[Decision]
    approved_edit: NotRequired[str]
    status: NotRequired[str]
    resolution_applied: NotRequired[bool]
    escalation_reason: NotRequired[str]


def _step(name: str, **updates: object) -> WorkflowState:
    return cast(WorkflowState, {"steps": [name], **updates})


def build_workflow(
    *,
    provider: ModelProvider | None = None,
    checkpointer: BaseCheckpointSaver[str] | None = None,
) -> CompiledStateGraph[WorkflowState, None, WorkflowState, WorkflowState]:
    """Compile the reviewed thirteen-node graph with replayable defaults."""

    model = provider or MockModelProvider()

    def intake_validation(state: WorkflowState) -> WorkflowState:
        return _step("intake_validation", status="running")

    def after_intake(state: WorkflowState) -> str:
        return (
            "deterministic_reconciliation" if state["payload_valid"] else "failure_and_escalation"
        )

    def deterministic_reconciliation(state: WorkflowState) -> WorkflowState:
        return _step("deterministic_reconciliation")

    def memo_nlp_analysis(state: WorkflowState) -> WorkflowState:
        return _step("memo_nlp_analysis")

    def triage_classifier(state: WorkflowState) -> WorkflowState:
        result = model.classify(state["exception_type"], state["evidence"])
        return _step(
            "triage_classifier",
            classification=result.label,
            confidence=result.confidence,
            provider=result.provider,
            model=result.model,
        )

    def reference_enrichment(state: WorkflowState) -> WorkflowState:
        return _step("reference_enrichment")

    def evidence_retrieval(state: WorkflowState) -> WorkflowState:
        return _step("evidence_retrieval")

    def after_evidence(state: WorkflowState) -> str:
        if state["evidence_malicious"]:
            return "failure_and_escalation"
        return "resolution_planner" if state["evidence"] else "failure_and_escalation"

    def resolution_planner(state: WorkflowState) -> WorkflowState:
        draft = model.draft_resolution(state["exception_type"], state["evidence"])
        return _step(
            "resolution_planner",
            proposal=draft.summary,
            provider=draft.provider,
            model=draft.model,
        )

    def policy_and_risk_validator(state: WorkflowState) -> WorkflowState:
        return _step("policy_and_risk_validator")

    def confidence_and_citation_gate(state: WorkflowState) -> WorkflowState:
        confidence = state.get("confidence", 0.0)
        passed = state["deterministic_valid"] and confidence >= 0.75 and bool(state["evidence"])
        return _step(
            "confidence_and_citation_gate",
            status="review_required" if passed else "escalation_required",
        )

    def after_gate(state: WorkflowState) -> str:
        return (
            "human_review_interrupt"
            if state["status"] == "review_required"
            else "failure_and_escalation"
        )

    def human_review_interrupt(state: WorkflowState) -> WorkflowState:
        response = interrupt(
            {
                "exception_id": state["exception_id"],
                "proposal": state.get("proposal"),
                "allowed_decisions": [
                    "approve",
                    "edit",
                    "reject",
                    "request_more_evidence",
                    "escalate",
                ],
            }
        )
        if not isinstance(response, dict) or response.get("decision") not in {
            "approve",
            "edit",
            "reject",
            "request_more_evidence",
            "escalate",
        }:
            return _step("human_review_interrupt", approval="escalate")
        decision = cast(Decision, response["decision"])
        edit = response.get("edit")
        updates: dict[str, object] = {"approval": decision}
        if decision == "edit" and isinstance(edit, str):
            updates["approved_edit"] = edit
        return _step("human_review_interrupt", **updates)

    def after_review(state: WorkflowState) -> str:
        return (
            "safe_resolution_executor"
            if state.get("approval") in {"approve", "edit"}
            else "audit_and_finalize"
        )

    def safe_resolution_executor(state: WorkflowState) -> WorkflowState:
        allowed = state["requested_action"] == "propose_demo_field_correction"
        return _step(
            "safe_resolution_executor",
            resolution_applied=allowed,
            status="resolved" if allowed else "escalated",
        )

    def audit_and_finalize(state: WorkflowState) -> WorkflowState:
        status = state.get("status", "closed_without_change")
        if state.get("approval") in {"reject", "request_more_evidence", "escalate"}:
            status = cast(str, state["approval"])
        return _step("audit_and_finalize", status=status)

    def failure_and_escalation(state: WorkflowState) -> WorkflowState:
        reason = "malicious_or_insufficient_evidence"
        if not state["payload_valid"]:
            reason = "invalid_payload"
        elif not state["deterministic_valid"]:
            reason = "deterministic_validation_failed"
        return _step(
            "failure_and_escalation",
            status="escalated",
            resolution_applied=False,
            escalation_reason=reason,
        )

    graph = StateGraph(WorkflowState)
    nodes = {
        "intake_validation": intake_validation,
        "deterministic_reconciliation": deterministic_reconciliation,
        "memo_nlp_analysis": memo_nlp_analysis,
        "triage_classifier": triage_classifier,
        "reference_enrichment": reference_enrichment,
        "evidence_retrieval": evidence_retrieval,
        "resolution_planner": resolution_planner,
        "policy_and_risk_validator": policy_and_risk_validator,
        "confidence_and_citation_gate": confidence_and_citation_gate,
        "human_review_interrupt": human_review_interrupt,
        "safe_resolution_executor": safe_resolution_executor,
        "audit_and_finalize": audit_and_finalize,
        "failure_and_escalation": failure_and_escalation,
    }
    for name, node in nodes.items():
        graph.add_node(name, node)
    graph.add_edge(START, "intake_validation")
    graph.add_conditional_edges("intake_validation", after_intake)
    graph.add_edge("deterministic_reconciliation", "memo_nlp_analysis")
    graph.add_edge("memo_nlp_analysis", "triage_classifier")
    graph.add_edge("triage_classifier", "reference_enrichment")
    graph.add_edge("reference_enrichment", "evidence_retrieval")
    graph.add_conditional_edges("evidence_retrieval", after_evidence)
    graph.add_edge("resolution_planner", "policy_and_risk_validator")
    graph.add_edge("policy_and_risk_validator", "confidence_and_citation_gate")
    graph.add_conditional_edges("confidence_and_citation_gate", after_gate)
    graph.add_conditional_edges("human_review_interrupt", after_review)
    graph.add_edge("safe_resolution_executor", "audit_and_finalize")
    graph.add_edge("failure_and_escalation", "audit_and_finalize")
    graph.add_edge("audit_and_finalize", END)
    return graph.compile(checkpointer=checkpointer or InMemorySaver())
