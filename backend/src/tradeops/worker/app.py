"""Celery application factory with side-effect-free configuration."""

from celery import Celery

from tradeops.config import Settings, get_settings


def create_worker(settings: Settings | None = None) -> Celery:
    """Configure a worker without connecting to its broker."""

    resolved = settings or get_settings()
    worker = Celery(
        "tradeops", broker=resolved.worker_broker_url, backend=resolved.worker_result_backend_url
    )
    worker.conf.update(
        accept_content=["json"],
        enable_utc=True,
        result_serializer="json",
        task_acks_late=True,
        task_reject_on_worker_lost=True,
        task_serializer="json",
        timezone="UTC",
    )
    return worker


celery_app = create_worker()
