"""Read-only platform, provenance, evaluation, and admin demo contracts."""

from dataclasses import asdict
from datetime import UTC, datetime
from hashlib import sha256
from typing import Annotated, Literal
from uuid import UUID, uuid5

from fastapi import APIRouter, Depends, Header, HTTPException, Query, Request, status
from pydantic import BaseModel, ConfigDict, Field

from tradeops import __version__
from tradeops.api.security import Principal, Role, current_principal, require_roles
from tradeops.application.demo_operations import DemoOperationsService
from tradeops.evaluation import build_golden_dataset, run_mock_baseline

router = APIRouter(tags=["platform"])
_NAMESPACE = UUID("b6f0d71f-a895-5f9b-a0d4-1f06b684cbf1")


class DashboardSummary(BaseModel):
    model_config = ConfigDict(frozen=True)
    exception_total: int
    open_total: int
    escalated_total: int
    review_required_total: int
    data_classification: Literal["synthetic"] = "synthetic"


class TradeSummary(BaseModel):
    model_config = ConfigDict(frozen=True)
    synthetic_trade_id: str
    product_type: str
    currency: str
    notional: str
    price: str
    trade_date: str
    settlement_date: str


class TradeList(BaseModel):
    model_config = ConfigDict(frozen=True)
    items: tuple[TradeSummary, ...]
    total: int
    next_cursor: int | None


class ImportResponse(BaseModel):
    model_config = ConfigDict(frozen=True)
    import_id: UUID
    status: Literal["accepted", "duplicate"]
    dataset_version: str
    record_count: int


class KnowledgeDocument(BaseModel):
    model_config = ConfigDict(frozen=True)
    id: str
    title: str
    source_type: str
    record_count: int
    ingestion_status: Literal["ready"] = "ready"
    provenance: str


class SourceStatus(BaseModel):
    model_config = ConfigDict(frozen=True)
    name: str
    mode: Literal["fixture_only"] = "fixture_only"
    status: Literal["hash_verified"] = "hash_verified"
    allowlisted_host: str


class SyncResponse(BaseModel):
    model_config = ConfigDict(frozen=True)
    source: str
    status: Literal["fixture_verified"] = "fixture_verified"
    idempotency_key_sha256: str


class EvaluationCaseResponse(BaseModel):
    model_config = ConfigDict(frozen=True)
    id: str
    case_type: str
    exception_type: str
    expected_status: str


class EvaluationRunResponse(BaseModel):
    model_config = ConfigDict(frozen=True)
    id: UUID
    dataset_version: str
    prompt_version: str
    provider: str
    model: str
    total: int
    passed: int
    failed: int
    temperature: int = 0
    estimated_cost_usd: int = 0
    completed_at: datetime = Field(default=datetime(2026, 1, 15, tzinfo=UTC))


class VersionResponse(BaseModel):
    model_config = ConfigDict(frozen=True)
    version: str
    api_version: Literal["v1"] = "v1"
    data_mode: Literal["synthetic_and_public_fixtures"] = "synthetic_and_public_fixtures"


def _service(request: Request) -> DemoOperationsService:
    service: DemoOperationsService = request.app.state.operations
    return service


@router.get("/dashboard/summary", response_model=DashboardSummary)
def dashboard_summary(
    request: Request, principal: Annotated[Principal, Depends(current_principal)]
) -> DashboardSummary:
    del principal
    items = _service(request).list_exceptions()
    return DashboardSummary(
        exception_total=len(items),
        open_total=sum(item.status == "open" for item in items),
        escalated_total=sum(item.status == "escalated" for item in items),
        review_required_total=sum(item.review_route == "review" for item in items),
    )


@router.get("/trades", response_model=TradeList)
def list_trades(
    request: Request,
    principal: Annotated[Principal, Depends(current_principal)],
    cursor: Annotated[int, Query(ge=0)] = 0,
    limit: Annotated[int, Query(ge=1, le=100)] = 25,
) -> TradeList:
    del principal
    trades = _service(request).trades()
    page = trades[cursor : cursor + limit]
    next_cursor = cursor + limit if cursor + limit < len(trades) else None
    return TradeList(
        items=tuple(
            TradeSummary(
                synthetic_trade_id=trade.synthetic_trade_id,
                product_type=trade.product_type,
                currency=trade.currency,
                notional=str(trade.notional),
                price=str(trade.price),
                trade_date=trade.trade_date.isoformat(),
                settlement_date=trade.settlement_date.isoformat(),
            )
            for trade in page
        ),
        total=len(trades),
        next_cursor=next_cursor,
    )


@router.post(
    "/imports/synthetic",
    response_model=ImportResponse,
    status_code=status.HTTP_202_ACCEPTED,
)
def import_synthetic(
    request: Request,
    principal: Annotated[Principal, Depends(require_roles(Role.ADMINISTRATOR))],
    idempotency_key: Annotated[str, Header(alias="Idempotency-Key", min_length=8, max_length=160)],
) -> ImportResponse:
    del principal
    is_new = _service(request).register_import(idempotency_key)
    return ImportResponse(
        import_id=uuid5(_NAMESPACE, f"import:{idempotency_key}"),
        status="accepted" if is_new else "duplicate",
        dataset_version="synthetic-v1",
        record_count=len(_service(request).trades()),
    )


@router.get("/knowledge/documents", response_model=tuple[KnowledgeDocument, ...])
def knowledge_documents(
    principal: Annotated[Principal, Depends(current_principal)],
) -> tuple[KnowledgeDocument, ...]:
    del principal
    return (
        KnowledgeDocument(
            id="policy-v1",
            title="Synthetic operations policies",
            source_type="synthetic",
            record_count=30,
            provenance="local authored fixture",
        ),
        KnowledgeDocument(
            id="gleif-fixture",
            title="GLEIF API sample",
            source_type="public_fixture",
            record_count=1,
            provenance="data/provenance/manifest.json",
        ),
        KnowledgeDocument(
            id="sec-fixture",
            title="SEC EDGAR sample",
            source_type="public_fixture",
            record_count=1,
            provenance="data/provenance/manifest.json",
        ),
        KnowledgeDocument(
            id="treasury-fixture",
            title="U.S. Treasury sample",
            source_type="public_fixture",
            record_count=1,
            provenance="data/provenance/manifest.json",
        ),
    )


@router.get("/sources", response_model=tuple[SourceStatus, ...])
def source_statuses(
    principal: Annotated[Principal, Depends(current_principal)],
) -> tuple[SourceStatus, ...]:
    del principal
    return tuple(
        SourceStatus(name=name, allowlisted_host=host)
        for name, host in (
            ("GLEIF", "api.gleif.org"),
            ("SEC EDGAR", "data.sec.gov"),
            ("U.S. Treasury", "api.fiscaldata.treasury.gov"),
        )
    )


@router.post("/sources/{source}/sync", response_model=SyncResponse)
def sync_source(
    source: str,
    principal: Annotated[Principal, Depends(require_roles(Role.ADMINISTRATOR))],
    idempotency_key: Annotated[str, Header(alias="Idempotency-Key", min_length=8, max_length=160)],
) -> SyncResponse:
    del principal
    allowed = {"gleif", "sec", "treasury"}
    if source not in allowed:
        raise HTTPException(status_code=404, detail="Source is not allowlisted.")
    return SyncResponse(
        source=source,
        idempotency_key_sha256=sha256(idempotency_key.encode()).hexdigest(),
    )


@router.get("/evaluations/cases", response_model=tuple[EvaluationCaseResponse, ...])
def evaluation_cases(
    principal: Annotated[Principal, Depends(current_principal)],
) -> tuple[EvaluationCaseResponse, ...]:
    del principal
    return tuple(
        EvaluationCaseResponse(
            **{
                key: value
                for key, value in asdict(case).items()
                if key in {"id", "case_type", "exception_type", "expected_status"}
            }
        )
        for case in build_golden_dataset()
    )


@router.post("/evaluations/runs", response_model=EvaluationRunResponse)
def run_evaluation(
    principal: Annotated[Principal, Depends(require_roles(Role.ADMINISTRATOR))],
    idempotency_key: Annotated[str, Header(alias="Idempotency-Key", min_length=8, max_length=160)],
) -> EvaluationRunResponse:
    del principal
    baseline = run_mock_baseline()
    return EvaluationRunResponse(
        id=uuid5(_NAMESPACE, f"evaluation:{idempotency_key}"),
        **asdict(baseline),
    )


@router.get("/version", response_model=VersionResponse)
def version() -> VersionResponse:
    return VersionResponse(version=__version__)
