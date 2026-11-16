"""Fixed-window rate limiter used by the public API."""

import time


class RateLimiter:
    def __init__(self, limit: int, window_seconds: float) -> None:
        self.limit = limit
        self.window_seconds = window_seconds
        self.counts: dict[str, int] = {}
        self.window_start: dict[str, float] = {}

    def allow(self, client_id: str) -> bool:
        now = time.monotonic()
        start = self.window_start.get(client_id, now)
        if now - start >= self.window_seconds:
            start = now
            self.counts[client_id] = 0
        self.window_start[client_id] = start
        count = self.counts.get(client_id, 0)
        if count >= self.limit:
            return False
        self.counts[client_id] = count + 1
        return True
