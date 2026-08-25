"""Provider-independent advisory request and structured output contracts."""

import re
from decimal import Decimal
from enum import StrEnum
from typing import Protocol

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

_DIGEST = re.compile(r"^[0-9a-f]{64}$")


class AdvisoryTask(StrEnum):
    """The narrow model-assisted tasks permitted by the workflow."""

    TRIAGE = "triage"
    RESOLUTION_DRAFT = "resolution_draft"


class EvidenceSnippet(BaseModel):
    """Untrusted, versioned evidence candidate supplied to a provider."""

    model_config = ConfigDict(frozen=True)

    chunk_id: str = Field(min_length=1, max_length=150)
    title: str = Field(min_length=1, max_length=500)
    section: str | None = Field(default=None, max_length=500)
    content: str = Field(min_length=1, max_length=4_000)
    source_locator: str = Field(min_length=1, max_length=2_000)
    content_sha256: str

    @field_validator("content_sha256")
    @classmethod
    def validate_digest(cls, value: str) -> str:
        if _DIGEST.fullmatch(value) is None:
            raise ValueError("content_sha256 must be lowercase SHA-256")
        return value


class AdvisoryRequest(BaseModel):
    """Redacted, bounded request independent of any provider SDK."""

    model_config = ConfigDict(frozen=True)

    request_id: str = Field(min_length=1, max_length=128)
    task: AdvisoryTask
    case_summary: str = Field(min_length=1, max_length=4_000)
    deterministic_findings: tuple[str, ...] = Field(min_length=1, max_length=20)
    evidence: tuple[EvidenceSnippet, ...] = Field(default=(), max_length=20)
    allowed_actions: tuple[str, ...] = Field(default=(), max_length=20)
    schema_version: str = Field(default="advisory-v1", min_length=1, max_length=100)

    @field_validator("deterministic_findings", "allowed_actions")
    @classmethod
    def validate_bounded_items(cls, value: tuple[str, ...]) -> tuple[str, ...]:
        if any(not item.strip() or len(item) > 500 for item in value):
            raise ValueError("items must contain 1 to 500 characters")
        return value


class Citation(BaseModel):
    """Citation resolvable to one exact evidence snippet."""

    model_config = ConfigDict(frozen=True)

    chunk_id: str = Field(min_length=1, max_length=150)
    claim: str = Field(min_length=1, max_length=1_000)


class ProviderMetadata(BaseModel):
    """Non-secret provider execution metadata for audit and evaluation."""

    model_config = ConfigDict(frozen=True)

    provider: str = Field(min_length=1, max_length=50)
    model: str = Field(min_length=1, max_length=200)
    request_id: str = Field(min_length=1, max_length=200)
    input_units: int = Field(ge=0)
    output_units: int = Field(ge=0)
    latency_ms: int = Field(ge=0)


class AdvisoryResponse(BaseModel):
    """Schema-validated advisory output; never an authorization decision."""

    model_config = ConfigDict(frozen=True)

    summary: str = Field(min_length=1, max_length=2_000)
    proposed_action: str | None = Field(default=None, max_length=500)
    confidence: Decimal = Field(ge=Decimal("0"), le=Decimal("1"))
    assumptions: tuple[str, ...] = Field(default=(), max_length=20)
    citations: tuple[Citation, ...] = Field(default=(), max_length=20)
    refusal_reason: str | None = Field(default=None, max_length=1_000)
    metadata: ProviderMetadata

    @model_validator(mode="after")
    def validate_action_or_refusal(self) -> "AdvisoryResponse":
        if self.proposed_action is None and self.refusal_reason is None:
            raise ValueError("a response must propose an action or refuse")
        if self.proposed_action is not None and self.refusal_reason is not None:
            raise ValueError("a response cannot propose and refuse simultaneously")
        if self.proposed_action is not None and not self.citations:
            raise ValueError("an action proposal requires at least one citation")
        return self


class AdvisoryProvider(Protocol):
    """Narrow provider port implemented by mock and optional hosted adapters."""

    async def generate(self, request: AdvisoryRequest) -> AdvisoryResponse:
        """Return one schema-validated advisory response."""

        ...
