"""Duplicate, reordered, and missed event behavior."""

from datetime import UTC, datetime
from uuid import UUID, uuid4

from tradeops.worker.delivery import ApplicationEvent, EventDeliveryTracker


def _event(aggregate_id: UUID, sequence: int) -> ApplicationEvent:
    return ApplicationEvent(
        id=uuid4(),
        aggregate_id=aggregate_id,
        sequence=sequence,
        event_type="workflow.step_completed.v1",
        occurred_at=datetime(2026, 1, 15, tzinfo=UTC),
    )


def test_duplicate_delivery_is_idempotent() -> None:
    tracker = EventDeliveryTracker()
    event = _event(uuid4(), 1)

    assert tracker.accept(event).status == "delivered"
    assert tracker.accept(event).status == "duplicate"


def test_gap_defers_then_recovers_in_order() -> None:
    tracker = EventDeliveryTracker()
    aggregate_id = uuid4()
    first = _event(aggregate_id, 1)
    second = _event(aggregate_id, 2)

    deferred = tracker.accept(second)
    assert deferred.status == "deferred_gap"
    assert deferred.retry_after_seconds is not None
    assert tracker.accept(first).status == "delivered"
    assert tracker.accept(second).status == "delivered"


def test_late_distinct_event_is_stale() -> None:
    tracker = EventDeliveryTracker()
    aggregate_id = uuid4()

    assert tracker.accept(_event(aggregate_id, 1)).status == "delivered"
    assert tracker.accept(_event(aggregate_id, 1)).status == "stale"
