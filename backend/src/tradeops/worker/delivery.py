"""Idempotent, order-aware event delivery policy."""

from dataclasses import dataclass
from datetime import datetime
from uuid import UUID


@dataclass(frozen=True, slots=True)
class ApplicationEvent:
    id: UUID
    aggregate_id: UUID
    sequence: int
    event_type: str
    occurred_at: datetime


@dataclass(frozen=True, slots=True)
class DeliveryResult:
    status: str
    retry_after_seconds: int | None = None


class EventDeliveryTracker:
    """Reject duplicates and defer gaps without losing the event."""

    def __init__(self) -> None:
        self._delivered: set[UUID] = set()
        self._last_sequence: dict[UUID, int] = {}

    def accept(self, event: ApplicationEvent) -> DeliveryResult:
        if event.id in self._delivered:
            return DeliveryResult("duplicate")
        expected = self._last_sequence.get(event.aggregate_id, 0) + 1
        if event.sequence > expected:
            return DeliveryResult("deferred_gap", retry_after_seconds=min(60, 2**expected))
        if event.sequence < expected:
            return DeliveryResult("stale")
        self._delivered.add(event.id)
        self._last_sequence[event.aggregate_id] = event.sequence
        return DeliveryResult("delivered")
