"""Reviewed SQLAlchemy repository for deterministic synthetic demo state."""

from dataclasses import asdict, dataclass
from datetime import UTC, datetime
from uuid import UUID

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from tradeops.adapters.persistence.models import (
    CounterpartyRecord,
    ExceptionEvidenceRecord,
    ExceptionRecord,
    InstrumentRecord,
    TradeRecord,
    TradeVersionRecord,
)
from tradeops.domain.reconciliation import ReconciliationPolicy, evaluate_reconciliation
from tradeops.domain.synthetic import SyntheticDataset


@dataclass(frozen=True, slots=True)
class SeedResult:
    """Counts written by an idempotent seed operation."""

    trades_created: int
    exceptions_created: int
    already_loaded: bool


@dataclass(frozen=True, slots=True)
class ExceptionSummary:
    """Queue projection detached from persistence implementation details."""

    id: UUID
    synthetic_trade_id: str
    exception_type: str
    severity: str
    status: str
    explanation: str
    version: int
    created_at: datetime


class TradeOpsRepository:
    """Narrow repository; commits remain an application composition concern."""

    def __init__(self, session: Session) -> None:
        self._session = session

    def seed(self, dataset: SyntheticDataset) -> SeedResult:
        """Load a generated dataset once using its stable first trade identifier."""

        first_trade_id = dataset.trades[0].synthetic_trade_id
        exists = self._session.scalar(
            select(func.count())
            .select_from(TradeRecord)
            .where(TradeRecord.synthetic_trade_id == first_trade_id)
        )
        if exists:
            return SeedResult(0, 0, True)

        counterparties: dict[str, CounterpartyRecord] = {}
        instruments: dict[str, InstrumentRecord] = {}
        exceptions_created = 0
        policy = ReconciliationPolicy()
        for item in dataset.trades:
            reference = item.reference
            counterparty = counterparties.get(reference.counterparty_lei)
            if counterparty is None:
                counterparty = CounterpartyRecord(
                    synthetic_lei=reference.counterparty_lei,
                    legal_name=reference.counterparty_name,
                    status="active" if reference.counterparty_active else "inactive",
                    reference_as_of=reference.observed_at,
                )
                counterparties[reference.counterparty_lei] = counterparty
                self._session.add(counterparty)
            instrument = instruments.get(reference.instrument_id)
            if instrument is None:
                instrument = InstrumentRecord(
                    synthetic_instrument_id=reference.instrument_id,
                    issuer_id=None,
                    product_type=item.product_type,
                    currency=reference.currency,
                    is_active=True,
                    reference_as_of=reference.observed_at,
                )
                instruments[reference.instrument_id] = instrument
                self._session.add(instrument)

            trade = TradeRecord(
                id=item.trade_id,
                synthetic_trade_id=item.synthetic_trade_id,
                current_version=1,
            )
            self._session.add(trade)
            self._session.flush()
            self._session.add(
                TradeVersionRecord(
                    trade_id=trade.id,
                    version=1,
                    instrument_id=instrument.id,
                    counterparty_id=counterparty.id,
                    side="buy",
                    currency=item.currency,
                    notional=item.notional,
                    price=item.price,
                    trade_date=item.trade_date,
                    settlement_date=item.settlement_date,
                    memo=item.memo,
                    observed_at=datetime(2026, 1, 15, tzinfo=UTC),
                )
            )
            for finding in evaluate_reconciliation(item, policy):
                exception = ExceptionRecord(
                    id=finding.id,
                    trade_id=trade.id,
                    exception_type=finding.exception_type.value,
                    severity=finding.severity.value,
                    status="escalated" if finding.review_route.value == "escalate" else "open",
                    explanation=finding.explanation,
                    rule_version=finding.rule_version,
                    finding_key=str(finding.id),
                    version=1,
                )
                self._session.add(exception)
                self._session.flush()
                self._session.add(
                    ExceptionEvidenceRecord(
                        exception_id=exception.id,
                        source_type="deterministic_rule",
                        source_reference=finding.rule_version,
                        content={
                            "facts": list(finding.evidence),
                            "suggested_actions": list(finding.suggested_actions),
                            "review_route": finding.review_route.value,
                        },
                    )
                )
                exceptions_created += 1
        return SeedResult(len(dataset.trades), exceptions_created, False)

    def list_exceptions(self, *, status: str | None = None) -> tuple[ExceptionSummary, ...]:
        """Return a stable queue ordering with an optional exact status filter."""

        statement = (
            select(ExceptionRecord, TradeRecord.synthetic_trade_id)
            .join(TradeRecord, TradeRecord.id == ExceptionRecord.trade_id)
            .order_by(ExceptionRecord.created_at.desc(), ExceptionRecord.id)
        )
        if status is not None:
            statement = statement.where(ExceptionRecord.status == status)
        rows = self._session.execute(statement).all()
        return tuple(
            ExceptionSummary(
                id=record.id,
                synthetic_trade_id=synthetic_trade_id,
                exception_type=record.exception_type,
                severity=record.severity,
                status=record.status,
                explanation=record.explanation,
                version=record.version,
                created_at=record.created_at,
            )
            for record, synthetic_trade_id in rows
        )

    def evidence(self, exception_id: UUID) -> tuple[dict[str, object], ...]:
        """Return detached evidence payloads for a single finding."""

        records = self._session.scalars(
            select(ExceptionEvidenceRecord)
            .where(ExceptionEvidenceRecord.exception_id == exception_id)
            .order_by(ExceptionEvidenceRecord.created_at, ExceptionEvidenceRecord.id)
        )
        return tuple(
            {
                "source_type": record.source_type,
                "source_reference": record.source_reference,
                "content": record.content,
            }
            for record in records
        )

    @staticmethod
    def serialize_seed_result(result: SeedResult) -> dict[str, object]:
        """Expose a JSON-compatible projection without leaking ORM state."""

        return asdict(result)
