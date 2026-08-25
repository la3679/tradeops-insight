"""One deterministic facade over the complete rule set."""

from collections.abc import Mapping, Set
from dataclasses import dataclass, field
from datetime import UTC, datetime

from tradeops_domain.errors import DomainValidationError
from tradeops_domain.exceptions import DetectedException
from tradeops_domain.models import CounterpartyReference, InstrumentReference, SyntheticTrade
from tradeops_domain.reconciliation.content import (
    MemoConflict,
    PayloadIssue,
    detect_content_exceptions,
)
from tradeops_domain.reconciliation.entity import detect_entity_exceptions
from tradeops_domain.reconciliation.financial import (
    ExpectedFinancials,
    FinancialTolerance,
    detect_financial_exceptions,
)
from tradeops_domain.reconciliation.lifecycle import (
    SettlementPolicy,
    detect_lifecycle_exceptions,
)
from tradeops_domain.reconciliation.reference import (
    ReferencePolicy,
    detect_reference_exceptions,
)


@dataclass(frozen=True, slots=True, kw_only=True)
class ReconciliationContext:
    """Versioned comparison data supplied to side-effect-free rules."""

    counterparties_by_lei: Mapping[str, CounterpartyReference]
    instrument: InstrumentReference | None
    expected_financials: ExpectedFinancials | None
    evaluated_at: datetime
    seen_event_ids: Set[str]
    seen_trade_fingerprints: Set[str]
    memo_conflicts: tuple[MemoConflict, ...] = ()
    payload_issues: tuple[PayloadIssue, ...] = ()
    reference_policy: ReferencePolicy = field(default_factory=ReferencePolicy)
    financial_tolerance: FinancialTolerance = field(default_factory=FinancialTolerance)
    settlement_policy: SettlementPolicy = field(default_factory=SettlementPolicy)

    def __post_init__(self) -> None:
        if self.evaluated_at.tzinfo is None or self.evaluated_at.utcoffset() != UTC.utcoffset(
            self.evaluated_at
        ):
            raise DomainValidationError(
                field="evaluated_at",
                reason="must be timezone-aware UTC",
            )


@dataclass(frozen=True, slots=True, kw_only=True)
class ReconciliationReport:
    """Ordered findings for one synthetic trade and evaluation instant."""

    trade_id: str
    event_id: str
    evaluated_at: datetime
    findings: tuple[DetectedException, ...]


def reconcile_trade(
    trade: SyntheticTrade,
    context: ReconciliationContext,
) -> ReconciliationReport:
    """Run every applicable rule in stable documented order."""

    counterparty = context.counterparties_by_lei.get(trade.counterparty_lei or "")
    findings: list[DetectedException] = []
    findings.extend(detect_entity_exceptions(trade, context.counterparties_by_lei))
    findings.extend(
        detect_reference_exceptions(
            trade,
            instrument=context.instrument,
            counterparty=counterparty,
            evaluated_at=context.evaluated_at,
            policy=context.reference_policy,
        )
    )
    if context.expected_financials is not None:
        findings.extend(
            detect_financial_exceptions(
                trade,
                context.expected_financials,
                context.financial_tolerance,
            )
        )
    findings.extend(
        detect_lifecycle_exceptions(
            trade,
            seen_event_ids=context.seen_event_ids,
            seen_trade_fingerprints=context.seen_trade_fingerprints,
            settlement_policy=context.settlement_policy,
        )
    )
    findings.extend(
        detect_content_exceptions(
            trade,
            memo_conflicts=context.memo_conflicts,
            payload_issues=context.payload_issues,
        )
    )
    return ReconciliationReport(
        trade_id=trade.trade_id,
        event_id=trade.event_id,
        evaluated_at=context.evaluated_at,
        findings=tuple(findings),
    )
