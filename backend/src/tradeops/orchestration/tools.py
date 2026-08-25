"""Narrow typed tools; no model receives unrestricted system capabilities."""

from dataclasses import dataclass, field
from datetime import date
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

from tradeops.domain.rules.settlement_date import SettlementDatePolicy


class ToolAuthorizationError(PermissionError):
    """The caller is not authorized for the requested tool operation."""


class ToolConflictError(RuntimeError):
    """The tool request is stale or duplicates an earlier mutation."""


class SettlementDateInput(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")
    trade_date: date
    business_day_lag: int = Field(ge=0, le=10)
    holidays: frozenset[date] = frozenset()


class SettlementDateOutput(BaseModel):
    model_config = ConfigDict(frozen=True)
    settlement_date: date
    policy_version: str


def calculate_settlement_date(payload: SettlementDateInput) -> SettlementDateOutput:
    """Calculate a date from explicit deterministic policy inputs."""

    policy = SettlementDatePolicy(
        business_day_lag=payload.business_day_lag,
        holidays=payload.holidays,
    )
    return SettlementDateOutput(
        settlement_date=policy.expected_settlement_date(payload.trade_date),
        policy_version=policy.version,
    )


class CompareTradeVersionsInput(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")
    previous: dict[str, str]
    current: dict[str, str]


class FieldDifference(BaseModel):
    model_config = ConfigDict(frozen=True)
    field: str
    previous: str | None
    current: str | None


class CompareTradeVersionsOutput(BaseModel):
    model_config = ConfigDict(frozen=True)
    differences: tuple[FieldDifference, ...]


def compare_trade_versions(payload: CompareTradeVersionsInput) -> CompareTradeVersionsOutput:
    """Compare allowlisted string projections without interpreting financial meaning."""

    keys = sorted(payload.previous.keys() | payload.current.keys())
    differences = tuple(
        FieldDifference(
            field=key,
            previous=payload.previous.get(key),
            current=payload.current.get(key),
        )
        for key in keys
        if payload.previous.get(key) != payload.current.get(key)
    )
    return CompareTradeVersionsOutput(differences=differences)


class ApplyResolutionInput(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")
    role: Literal["analyst", "reviewer", "auditor", "administrator"]
    decision: Literal["approve", "edit", "reject", "request_more_evidence", "escalate"]
    field: str
    value: str
    expected_version: int = Field(ge=1)
    current_version: int = Field(ge=1)
    idempotency_key: str = Field(min_length=8, max_length=160)


class ApplyResolutionOutput(BaseModel):
    model_config = ConfigDict(frozen=True)
    applied: bool
    next_version: int
    field: str
    value: str


@dataclass(slots=True)
class SafeResolutionTool:
    """Apply only approved, current-version updates to synthetic demo fields."""

    _used_keys: set[str] = field(default_factory=set)
    allowed_fields: frozenset[str] = frozenset(
        {"counterparty_name", "instrument_id", "currency", "notional", "price", "settlement_date"}
    )

    def apply(self, payload: ApplyResolutionInput) -> ApplyResolutionOutput:
        if payload.role not in {"reviewer", "administrator"}:
            raise ToolAuthorizationError("reviewer or administrator role is required")
        if payload.decision not in {"approve", "edit"}:
            raise ToolAuthorizationError("an approve or edit decision is required")
        if payload.field not in self.allowed_fields:
            raise ToolAuthorizationError("field is not allowlisted for synthetic demo correction")
        if payload.expected_version != payload.current_version:
            raise ToolConflictError("synthetic trade version is stale")
        if payload.idempotency_key in self._used_keys:
            raise ToolConflictError("resolution idempotency key was already used")
        self._used_keys.add(payload.idempotency_key)
        return ApplyResolutionOutput(
            applied=True,
            next_version=payload.current_version + 1,
            field=payload.field,
            value=payload.value,
        )


TOOL_ALLOWLIST = frozenset(
    {
        "calculate_settlement_date",
        "compare_trade_versions",
        "apply_approved_demo_resolution",
    }
)
