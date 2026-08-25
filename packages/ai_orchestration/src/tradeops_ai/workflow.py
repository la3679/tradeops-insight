"""Explicit typed LangGraph skeleton for governed exception investigation."""

from decimal import Decimal
from itertools import pairwise
from operator import add
from typing import Annotated, Any, Literal, cast

from langgraph.graph import END, START, StateGraph
from typing_extensions import TypedDict

from tradeops_ai.provider import AdvisoryProvider, AdvisoryRequest, AdvisoryResponse

Disposition = Literal["allow_demo", "require_review", "deny"]
WorkflowStatus = Literal[
    "running",
    "awaiting_review",
    "completed",
    "escalated",
]


class WorkflowState(TypedDict):
    """Versioned fields shared by small explicit graph nodes."""

    workflow_id: str
    graph_version: str
    prompt_version: str
    request: AdvisoryRequest
    disposition: Disposition
    advisory: AdvisoryResponse | None
    citations_valid: bool
    status: WorkflowStatus
    error_code: str | None
    visited_nodes: Annotated[list[str], add]


def initial_state(
    *,
    workflow_id: str,
    request: AdvisoryRequest,
    disposition: Disposition = "require_review",
) -> WorkflowState:
    """Create a complete replayable state without reading a clock or global client."""

    return WorkflowState(
        workflow_id=workflow_id,
        graph_version="exception-graph-v1",
        prompt_version="advisory-v1",
        request=request,
        disposition=disposition,
        advisory=None,
        citations_valid=False,
        status="running",
        error_code=None,
        visited_nodes=[],
    )


def _visited(name: str) -> dict[str, Any]:
    return {"visited_nodes": [name]}


def build_workflow(provider: AdvisoryProvider) -> Any:
    """Compile the graph with an injected provider and no hidden mutable clients."""

    async def intake_validation(_: WorkflowState) -> dict[str, Any]:
        return _visited("intake_validation")

    async def deterministic_reconciliation(_: WorkflowState) -> dict[str, Any]:
        return _visited("deterministic_reconciliation")

    async def memo_nlp_analysis(_: WorkflowState) -> dict[str, Any]:
        return _visited("memo_nlp_analysis")

    async def triage_classifier(_: WorkflowState) -> dict[str, Any]:
        return _visited("triage_classifier")

    async def reference_enrichment(_: WorkflowState) -> dict[str, Any]:
        return _visited("reference_enrichment")

    async def evidence_retrieval(_: WorkflowState) -> dict[str, Any]:
        return _visited("evidence_retrieval")

    async def resolution_planner(state: WorkflowState) -> dict[str, Any]:
        advisory = await provider.generate(state["request"])
        return {"advisory": advisory, "visited_nodes": ["resolution_planner"]}

    async def policy_and_risk_validator(state: WorkflowState) -> dict[str, Any]:
        advisory = state["advisory"]
        if advisory is None or advisory.refusal_reason is not None:
            return {
                "disposition": "deny",
                "error_code": "ADVISORY_REFUSED",
                "visited_nodes": ["policy_and_risk_validator"],
            }
        return _visited("policy_and_risk_validator")

    async def confidence_and_citation_gate(state: WorkflowState) -> dict[str, Any]:
        advisory = state["advisory"]
        evidence_ids = {item.chunk_id for item in state["request"].evidence}
        valid = (
            advisory is not None
            and advisory.refusal_reason is None
            and advisory.confidence >= Decimal("0.70")
            and bool(advisory.citations)
            and all(citation.chunk_id in evidence_ids for citation in advisory.citations)
        )
        result: dict[str, Any] = {
            "citations_valid": valid,
            "visited_nodes": ["confidence_and_citation_gate"],
        }
        if not valid:
            result.update(disposition="deny", error_code="EVIDENCE_GATE_FAILED")
        return result

    async def human_review_interrupt(_: WorkflowState) -> dict[str, Any]:
        return {
            "status": "awaiting_review",
            "visited_nodes": ["human_review_interrupt"],
        }

    async def safe_resolution_executor(_: WorkflowState) -> dict[str, Any]:
        return {"status": "running", "visited_nodes": ["safe_resolution_executor"]}

    async def audit_and_finalize(_: WorkflowState) -> dict[str, Any]:
        return {"status": "completed", "visited_nodes": ["audit_and_finalize"]}

    async def failure_and_escalation(_: WorkflowState) -> dict[str, Any]:
        return {"status": "escalated", "visited_nodes": ["failure_and_escalation"]}

    def route_after_gate(state: WorkflowState) -> str:
        if state["disposition"] == "deny":
            return "failure_and_escalation"
        if state["disposition"] == "require_review":
            return "human_review_interrupt"
        return "safe_resolution_executor"

    graph = StateGraph(WorkflowState)

    def add_node(name: str, node: Any) -> None:
        # LangGraph accepts partial TypedDict updates; its overload currently models full state.
        graph.add_node(name, node)

    add_node("intake_validation", intake_validation)
    add_node("deterministic_reconciliation", deterministic_reconciliation)
    add_node("memo_nlp_analysis", memo_nlp_analysis)
    add_node("triage_classifier", triage_classifier)
    add_node("reference_enrichment", reference_enrichment)
    add_node("evidence_retrieval", evidence_retrieval)
    add_node("resolution_planner", resolution_planner)
    add_node("policy_and_risk_validator", policy_and_risk_validator)
    add_node("confidence_and_citation_gate", confidence_and_citation_gate)
    add_node("human_review_interrupt", human_review_interrupt)
    add_node("safe_resolution_executor", safe_resolution_executor)
    add_node("audit_and_finalize", audit_and_finalize)
    add_node("failure_and_escalation", failure_and_escalation)

    ordered = (
        "intake_validation",
        "deterministic_reconciliation",
        "memo_nlp_analysis",
        "triage_classifier",
        "reference_enrichment",
        "evidence_retrieval",
        "resolution_planner",
        "policy_and_risk_validator",
        "confidence_and_citation_gate",
    )
    graph.add_edge(START, ordered[0])
    for current, following in pairwise(ordered):
        graph.add_edge(current, following)
    graph.add_conditional_edges(
        "confidence_and_citation_gate",
        route_after_gate,
        {
            "failure_and_escalation": "failure_and_escalation",
            "human_review_interrupt": "human_review_interrupt",
            "safe_resolution_executor": "safe_resolution_executor",
        },
    )
    graph.add_edge("safe_resolution_executor", "audit_and_finalize")
    graph.add_edge("audit_and_finalize", END)
    graph.add_edge("human_review_interrupt", END)
    graph.add_edge("failure_and_escalation", END)
    return graph.compile()


def typed_result(result: dict[str, object]) -> WorkflowState:
    """Narrow a LangGraph result at the package boundary."""

    return cast(WorkflowState, result)
