"""Versioned synthetic operations, workflow, approval, and audit endpoints."""

from datetime import datetime
from typing import Annotated, Literal, cast
from uuid import UUID

from fastapi import (
    APIRouter,
    Depends,
    Header,
    Query,
    Request,
    WebSocket,
    WebSocketDisconnect,
    status,
)
from pydantic import BaseModel, ConfigDict, Field

from tradeops.api.security import Principal, Role, current_principal, require_roles
from tradeops.application.demo_operations import (
    AuditView,
    DemoOperationsService,
    QueueItem,
    WorkflowView,
)
from tradeops.orchestration.graph import Decision

router = APIRouter(tags=["operations"])


class UserResponse(BaseModel):
    model_config = ConfigDict(frozen=True)
    subject: str
    display_name: str
    role: Role
    mode: Literal["synthetic_demo"] = "synthetic_demo"


class ExceptionResponse(BaseModel):
    model_config = ConfigDict(frozen=True)
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
    version: int


class ExceptionListResponse(BaseModel):
    model_config = ConfigDict(frozen=True)
    items: tuple[ExceptionResponse, ...]
    total: int
    data_classification: Literal["synthetic"] = "synthetic"


class WorkflowResponse(BaseModel):
    model_config = ConfigDict(frozen=True)
    id: UUID
    exception_id: UUID
    status: str
    steps: tuple[str, ...]
    proposal: str | None
    provider: str | None
    model: str | None
    resolution_applied: bool
    version: str


class ApprovalRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")
    decision: Decision
    expected_exception_version: int = Field(ge=1)
    edit: str | None = Field(default=None, max_length=500)


class AuditResponse(BaseModel):
    model_config = ConfigDict(frozen=True)
    id: UUID
    event_type: str
    actor: str
    subject_id: UUID
    occurred_at: datetime
    summary: str


def _service(request: Request) -> DemoOperationsService:
    return cast(DemoOperationsService, request.app.state.operations)


def _exception(item: QueueItem) -> ExceptionResponse:
    return ExceptionResponse(**{field: getattr(item, field) for field in item.__dataclass_fields__})


def _workflow(view: WorkflowView) -> WorkflowResponse:
    return WorkflowResponse(**{field: getattr(view, field) for field in view.__dataclass_fields__})


def _audit(view: AuditView) -> AuditResponse:
    return AuditResponse(**{field: getattr(view, field) for field in view.__dataclass_fields__})


@router.get("/session/me", response_model=UserResponse)
def me(principal: Annotated[Principal, Depends(current_principal)]) -> UserResponse:
    return UserResponse(
        subject=principal.subject, display_name=principal.display_name, role=principal.role
    )


@router.get("/exceptions", response_model=ExceptionListResponse)
def list_exceptions(
    request: Request,
    principal: Annotated[Principal, Depends(current_principal)],
    queue_status: Annotated[str | None, Query(alias="status")] = None,
    severity: str | None = None,
    search: str | None = None,
) -> ExceptionListResponse:
    del principal
    items = _service(request).list_exceptions(status=queue_status, severity=severity, search=search)
    responses = tuple(_exception(item) for item in items)
    return ExceptionListResponse(items=responses, total=len(responses))


@router.get("/exceptions/{exception_id}", response_model=ExceptionResponse)
def get_exception(
    exception_id: UUID,
    request: Request,
    principal: Annotated[Principal, Depends(current_principal)],
) -> ExceptionResponse:
    del principal
    return _exception(_service(request).get_exception(exception_id))


@router.post(
    "/exceptions/{exception_id}/workflows",
    response_model=WorkflowResponse,
    status_code=status.HTTP_202_ACCEPTED,
)
def start_workflow(
    exception_id: UUID,
    request: Request,
    principal: Annotated[
        Principal, Depends(require_roles(Role.ANALYST, Role.REVIEWER, Role.ADMINISTRATOR))
    ],
    idempotency_key: Annotated[str, Header(alias="Idempotency-Key", min_length=8, max_length=160)],
) -> WorkflowResponse:
    return _workflow(
        _service(request).start_workflow(
            exception_id, idempotency_key=idempotency_key, actor=principal.subject
        )
    )


@router.get("/workflows/{workflow_id}", response_model=WorkflowResponse)
def get_workflow(
    workflow_id: UUID,
    request: Request,
    principal: Annotated[Principal, Depends(current_principal)],
) -> WorkflowResponse:
    del principal
    return _workflow(_service(request).get_workflow(workflow_id))


@router.post("/workflows/{workflow_id}/approvals", response_model=WorkflowResponse)
def approve_workflow(
    workflow_id: UUID,
    body: ApprovalRequest,
    request: Request,
    principal: Annotated[Principal, Depends(require_roles(Role.REVIEWER, Role.ADMINISTRATOR))],
    idempotency_key: Annotated[str, Header(alias="Idempotency-Key", min_length=8, max_length=160)],
) -> WorkflowResponse:
    return _workflow(
        _service(request).resume_workflow(
            workflow_id,
            decision=body.decision,
            expected_exception_version=body.expected_exception_version,
            idempotency_key=idempotency_key,
            actor=principal.subject,
            edit=body.edit,
        )
    )


@router.get("/audit-events", response_model=tuple[AuditResponse, ...])
def audit_events(
    request: Request,
    principal: Annotated[Principal, Depends(require_roles(Role.AUDITOR, Role.ADMINISTRATOR))],
) -> tuple[AuditResponse, ...]:
    del principal
    return tuple(_audit(item) for item in _service(request).audit_events())


@router.get("/events", response_model=tuple[AuditResponse, ...])
def poll_events(
    request: Request,
    principal: Annotated[Principal, Depends(current_principal)],
) -> tuple[AuditResponse, ...]:
    """Polling fallback for clients that cannot maintain a WebSocket."""

    del principal
    return tuple(_audit(item) for item in _service(request).audit_events())


@router.websocket("/events/ws")
async def websocket_events(websocket: WebSocket) -> None:
    """Send a safe current event snapshot; clients reconnect for later updates."""

    settings = websocket.app.state.settings
    requested_role = websocket.query_params.get("role", Role.ANALYST)
    if settings.environment == "production" or requested_role not in set(Role):
        await websocket.close(code=4401)
        return
    await websocket.accept()
    service = cast(DemoOperationsService, websocket.app.state.operations)
    try:
        await websocket.send_json(
            {
                "type": "queue.snapshot.v1",
                "events": [
                    {
                        "id": str(item.id),
                        "event_type": item.event_type,
                        "subject_id": str(item.subject_id),
                        "occurred_at": item.occurred_at.isoformat(),
                        "summary": item.summary,
                    }
                    for item in service.audit_events()
                ],
            }
        )
        await websocket.close(code=1000)
    except WebSocketDisconnect:
        return
