"""Worker command."""

from tradeops.worker.app import celery_app


def main() -> None:
    """Start the explicitly configured worker."""

    celery_app.worker_main(["worker", "--loglevel=INFO"])


if __name__ == "__main__":
    main()
