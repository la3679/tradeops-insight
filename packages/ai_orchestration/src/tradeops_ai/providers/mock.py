"""Deterministic no-key provider used by the demo and CI."""

from decimal import Decimal
from hashlib import sha256

from tradeops_ai.provider import (
    AdvisoryRequest,
    AdvisoryResponse,
    Citation,
    ProviderMetadata,
)


class MockAdvisoryProvider:
    """Draft from structured inputs without interpreting evidence as instructions."""

    async def generate(self, request: AdvisoryRequest) -> AdvisoryResponse:
        digest = sha256(request.model_dump_json().encode()).hexdigest()[:16]
        metadata = ProviderMetadata(
            provider="mock",
            model="deterministic-advisory-v1",
            request_id=f"mock-{digest}",
            input_units=len(request.case_summary.split())
            + sum(len(item.content.split()) for item in request.evidence),
            output_units=0,
            latency_ms=0,
        )
        if not request.evidence:
            return AdvisoryResponse(
                summary="No versioned evidence was available for a grounded recommendation.",
                confidence=Decimal("0"),
                refusal_reason="insufficient_evidence",
                metadata=metadata,
            )
        if not request.allowed_actions:
            return AdvisoryResponse(
                summary="Evidence was available, but policy supplied no allowlisted action.",
                confidence=Decimal("0"),
                refusal_reason="no_allowlisted_action",
                metadata=metadata,
            )

        evidence = request.evidence[0]
        action = request.allowed_actions[0]
        return AdvisoryResponse(
            summary=(
                f"Deterministic mock draft for {request.deterministic_findings[0]}; "
                "the cited evidence must still pass policy and human review."
            ),
            proposed_action=action,
            confidence=Decimal("0.75"),
            assumptions=("The supplied synthetic case and evidence versions are current.",),
            citations=(
                Citation(
                    chunk_id=evidence.chunk_id,
                    claim=(
                        "The first allowlisted action is supported by the supplied "
                        "evidence candidate."
                    ),
                ),
            ),
            metadata=metadata,
        )
