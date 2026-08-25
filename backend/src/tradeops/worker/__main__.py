"""Worker command."""

from tradeops.worker.app import celery_app


def main() -> None:
    """Start the explicitly configured worker."""

    celery_app.worker_main(["worker", "--loglevel=INFO", "--concurrency=2"])


if __name__ == "__main__":
    main()
