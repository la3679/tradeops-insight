"""Measure deterministic in-process components without making capacity claims."""

from collections.abc import Callable
from datetime import UTC, datetime
from statistics import mean, median, quantiles
from time import perf_counter
from uuid import uuid4

from langgraph.types import Command

from tradeops.orchestration.graph import WorkflowState, build_workflow
from tradeops.rag.pipeline import FaissKnowledgeIndex, generate_synthetic_policy_documents
from tradeops.worker.delivery import ApplicationEvent, EventDeliveryTracker


def measure(action: Callable[[], object], iterations: int) -> tuple[float, float, float]:
    samples: list[float] = []
    for _ in range(iterations):
        started = perf_counter()
        action()
        samples.append((perf_counter() - started) * 1_000)
    return mean(samples), median(samples), quantiles(samples, n=100)[94]


index = FaissKnowledgeIndex()
index.add(generate_synthetic_policy_documents())
retrieval = measure(lambda: index.search("settlement date analyst review"), 1_000)

tracker = EventDeliveryTracker()
aggregate_id = uuid4()
sequence = 0


def deliver() -> None:
    global sequence
    sequence += 1
    tracker.accept(
        ApplicationEvent(uuid4(), aggregate_id, sequence, "demo.event", datetime.now(UTC))
    )


worker = measure(deliver, 10_000)

graph = build_workflow()


def workflow() -> None:
    thread_id = str(uuid4())
    initial: WorkflowState = {
        "workflow_id": thread_id,
        "exception_id": str(uuid4()),
        "exception_type": "settlement_date_mismatch",
        "evidence": ("Synthetic policy requires reviewed settlement evidence.",),
        "requested_action": "review synthetic state",
        "payload_valid": True,
        "evidence_malicious": False,
        "deterministic_valid": True,
        "steps": [],
        "workflow_version": "workflow-v1",
        "prompt_version": "prompt-v1",
    }
    config = {"configurable": {"thread_id": thread_id}}
    graph.invoke(initial, config)
    graph.invoke(Command(resume={"decision": "approve"}), config)


workflow_result = measure(workflow, 100)

for label, values in (
    ("rag_retrieval", retrieval),
    ("worker_delivery", worker),
    ("mock_workflow", workflow_result),
):
    print(f"{label}: mean_ms={values[0]:.3f} median_ms={values[1]:.3f} p95_ms={values[2]:.3f}")
