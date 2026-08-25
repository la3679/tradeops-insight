"""Low-cardinality Prometheus metrics for one API process."""

from prometheus_client import CollectorRegistry, Counter, Histogram, generate_latest


class ApiMetrics:
    """Own an isolated registry so application factories remain test-safe."""

    def __init__(self) -> None:
        self.registry = CollectorRegistry()
        self.requests = Counter(
            "tradeops_http_requests_total",
            "Completed HTTP requests",
            ("method", "status_class"),
            registry=self.registry,
        )
        self.duration = Histogram(
            "tradeops_http_request_duration_seconds",
            "HTTP request duration without route or domain identifiers",
            ("method",),
            registry=self.registry,
        )

    def observe(self, *, method: str, status_code: int, duration_seconds: float) -> None:
        self.requests.labels(method=method, status_class=f"{status_code // 100}xx").inc()
        self.duration.labels(method=method).observe(duration_seconds)

    def render(self) -> bytes:
        return generate_latest(self.registry)
