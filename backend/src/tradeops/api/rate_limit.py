"""Small-process rate limiter for the local demo and single-instance reference API."""

from collections import defaultdict, deque
from threading import Lock
from time import monotonic


class FixedWindowRateLimiter:
    """Bound requests per client over a rolling minute without external state."""

    def __init__(self, requests_per_minute: int) -> None:
        self._limit = requests_per_minute
        self._requests: dict[str, deque[float]] = defaultdict(deque)
        self._lock = Lock()

    def allow(self, client_key: str) -> bool:
        now = monotonic()
        cutoff = now - 60
        with self._lock:
            window = self._requests[client_key]
            while window and window[0] <= cutoff:
                window.popleft()
            if len(window) >= self._limit:
                return False
            window.append(now)
            return True
