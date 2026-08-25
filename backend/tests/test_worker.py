from tradeops.config import Settings
from tradeops.worker.app import create_worker


def test_worker_uses_safe_serialization_and_delivery_defaults() -> None:
    worker = create_worker(Settings(environment="test"))

    assert worker.conf.accept_content == ["json"]
    assert worker.conf.task_serializer == "json"
    assert worker.conf.result_serializer == "json"
    assert worker.conf.task_acks_late is True
    assert worker.conf.task_reject_on_worker_lost is True
    assert worker.conf.enable_utc is True
