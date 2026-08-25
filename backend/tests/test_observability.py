"""Telemetry setup remains inert in tests and labels exported resources."""

from fastapi import FastAPI

from tradeops.config import Settings
from tradeops.observability import configure_observability


def test_observability_skips_exporter_threads_in_test_mode() -> None:
    provider = configure_observability(FastAPI(), Settings(environment="test"))

    assert provider is None
