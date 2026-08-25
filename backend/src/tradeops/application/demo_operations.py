"""Deterministic local operations service used by the API and offline demo."""

from dataclasses import dataclass, replace
from datetime import UTC, datetime
from typing import cast
from uuid import UUID, uuid5

from langchain_core.runnables import RunnableConfig
from langgraph.graph.state import CompiledStateGraph
from langgraph.types import Command

from tradeops.domain.reconciliation import ReconciliationPolicy, evaluate_reconciliation
from tradeops.domain.synthetic import generate_synthetic_dataset
from tradeops.orchestration.graph import Decision, WorkflowState, build_workflow

_NAMESPACE = UUID("12aecfaf-a72c-5481-8e4b-eb52299817ab")


class DemoNotFoundError(LookupError):
    """Requested synthetic demo entity does not exist."""


class DemoConflictError(RuntimeError):
    """Requested change conflicts with current demo state."""


@dataclass(frozen=True, slots=True)
class QueueItem:
    id: UUID
    synthetic_trade_id: str
    exception_type: str
    severity: str
    status: str
    review_route: str
    explanation: str
    evidence: tuple[str, ...]
    suggested_actions: tuple[str, ...]
    created_at: datetime
    version: int = 1


@dataclass(frozen=True, slots=True)
class WorkflowView:
    id: UUID
    exception_id: UUID
    status: str
    steps: tuple[str, ...]
    proposal: str | None
    provider: str | None
    model: str | None
    resolution_applied: bool
    version: str = "workflow-v1"


@dataclass(frozen=True, slots=True)
class AuditView:
    id: UUID
    event_type: str
    actor: str
    subject_id: UUID
    occurred_at: datetime
    summary: str


@dataclass(slots=True)
class _WorkflowSession:
    graph: CompiledStateGraph[WorkflowState, None, WorkflowState, WorkflowState]
    config: RunnableConfig
    view: WorkflowView


class DemoOperationsService:
    """In-process replayable facade; every record is visibly synthetic."""

    def __init__(self, *, dataset_size: int = 120) -> None:
        dataset = generate_synthetic_dataset(size=dataset_size)
        policy = ReconciliationPolicy()
        items: list[QueueItem] = []
        for trade in dataset.trades:
            for finding in evaluate_reconciliation(trade, policy):
                items.append(
                    QueueItem(
                        id=finding.id,
                        synthetic_trade_id=trade.synthetic_trade_id,
                        exception_type=finding.exception_type.value,
                        severity=finding.severity.value,
                        status=(
                            "escalated" if finding.review_route.value == "escalate" else "open"
                        ),
                        review_route=finding.review_route.value,
                        explanation=finding.explanation,
                        evidence=finding.evidence,
                        suggested_actions=finding.suggested_actions,
                        created_at=datetime(2026, 1, 15, tzinfo=UTC),
                    )
                )
        self._items = {item.id: item for item in items}
        self._workflows: dict[UUID, _WorkflowSession] = {}
        self._workflow_keys: dict[str, UUID] = {}
        self._approval_keys: dict[str, WorkflowView] = {}
        self._audit: list[AuditView] = []

    def list_exceptions(
        self,
        *,
        status: str | None = None,
        severity: str | None = None,
        search: str | None = None,
    ) -> tuple[QueueItem, ...]:
        values = self._items.values()
        normalized_search = search.casefold().strip() if search else None
        selected = (
            item
            for item in values
            if (status is None or item.status == status)
            and (severity is None or item.severity == severity)
            and (
                normalized_search is None
                or normalized_search in item.synthetic_trade_id.casefold()
                or normalized_search in item.exception_type.casefold()
            )
        )
        return tuple(
            sorted(selected, key=lambda item: (-item.created_at.timestamp(), str(item.id)))
        )

    def get_exception(self, exception_id: UUID) -> QueueItem:
        try:
            return self._items[exception_id]
        except KeyError as error:
            raise DemoNotFoundError("synthetic exception was not found") from error

    def start_workflow(
        self, exception_id: UUID, *, idempotency_key: str, actor: str
    ) -> WorkflowView:
        existing = self._workflow_keys.get(idempotency_key)
        if existing is not None:
            return self._workflows[existing].view
        item = self.get_exception(exception_id)
        workflow_id = uuid5(_NAMESPACE, f"workflow:{exception_id}:{idempotency_key}")
        graph = build_workflow()
        config = RunnableConfig(configurable={"thread_id": str(workflow_id)})
        initial: WorkflowState = {
            "workflow_id": str(workflow_id),
            "exception_id": str(exception_id),
            "exception_type": item.exception_type,
            "evidence": item.evidence,
            "requested_action": "propose_demo_field_correction",
            "payload_valid": True,
            "evidence_malicious": False,
            "deterministic_valid": True,
            "steps": [],
            "workflow_version": "workflow-v1",
            "prompt_version": "prompt-v1",
        }
        result = cast(WorkflowState, graph.invoke(initial, config))
        view = WorkflowView(
            id=workflow_id,
            exception_id=exception_id,
            status=result.get("status", "review_required"),
            steps=tuple(result["steps"]),
            proposal=result.get("proposal"),
            provider=result.get("provider"),
            model=result.get("model"),
            resolution_applied=False,
        )
        self._workflows[workflow_id] = _WorkflowSession(graph, config, view)
        self._workflow_keys[idempotency_key] = workflow_id
        self._record("workflow.started.v1", actor, exception_id, "Workflow paused for review")
        return view

    def get_workflow(self, workflow_id: UUID) -> WorkflowView:
        try:
            return self._workflows[workflow_id].view
        except KeyError as error:
            raise DemoNotFoundError("synthetic workflow was not found") from error

    def resume_workflow(
        self,
        workflow_id: UUID,
        *,
        decision: Decision,
        expected_exception_version: int,
        idempotency_key: str,
        actor: str,
        edit: str | None = None,
    ) -> WorkflowView:
        replay = self._approval_keys.get(idempotency_key)
        if replay is not None:
            return replay
        session = self._workflows.get(workflow_id)
        if session is None:
            raise DemoNotFoundError("synthetic workflow was not found")
        item = self.get_exception(session.view.exception_id)
        if item.version != expected_exception_version:
            raise DemoConflictError("exception version is stale")
        resume: dict[str, object] = {"decision": decision}
        if edit is not None:
            resume["edit"] = edit
        result = cast(
            WorkflowState,
            session.graph.invoke(Command[object](resume=resume), session.config),
        )
        updated = replace(
            session.view,
            status=result["status"],
            steps=tuple(result["steps"]),
            resolution_applied=result.get("resolution_applied", False),
        )
        session.view = updated
        self._approval_keys[idempotency_key] = updated
        self._items[item.id] = replace(item, status=updated.status, version=item.version + 1)
        self._record(
            "workflow.resumed.v1",
            actor,
            item.id,
            f"Reviewer decision recorded: {decision}",
        )
        if updated.resolution_applied:
            self._record(
                "resolution.applied.v1",
                actor,
                item.id,
                "Approved synthetic demo-state resolution applied",
            )
        return updated

    def audit_events(self) -> tuple[AuditView, ...]:
        return tuple(reversed(self._audit))

    def _record(self, event_type: str, actor: str, subject_id: UUID, summary: str) -> None:
        ordinal = len(self._audit)
        self._audit.append(
            AuditView(
                id=uuid5(_NAMESPACE, f"audit:{ordinal}:{event_type}:{subject_id}"),
                event_type=event_type,
                actor=actor,
                subject_id=subject_id,
                occurred_at=datetime(2026, 1, 15, tzinfo=UTC),
                summary=summary,
            )
        )
