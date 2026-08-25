"""PostgreSQL checkpoint composition for normal local workflow execution."""

from collections.abc import Iterator
from contextlib import contextmanager

from langgraph.checkpoint.postgres import PostgresSaver
from langgraph.graph.state import CompiledStateGraph

from tradeops.config import Settings
from tradeops.orchestration.graph import WorkflowState, build_workflow


def checkpoint_connection_string(settings: Settings) -> str:
    """Translate the SQLAlchemy URL to the psycopg URL expected by LangGraph."""

    value = settings.database_url.get_secret_value()
    prefix = "postgresql+psycopg://"
    if not value.startswith(prefix):
        raise ValueError("PostgreSQL checkpoints require a postgresql+psycopg database URL")
    return f"postgresql://{value.removeprefix(prefix)}"


@contextmanager
def postgres_workflow(
    settings: Settings,
) -> Iterator[CompiledStateGraph[WorkflowState, None, WorkflowState, WorkflowState]]:
    """Set up and yield a graph backed by durable PostgreSQL checkpoints."""

    with PostgresSaver.from_conn_string(checkpoint_connection_string(settings)) as saver:
        saver.setup()
        yield build_workflow(checkpointer=saver)
