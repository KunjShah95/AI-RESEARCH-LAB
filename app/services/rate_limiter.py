"""Token bucket rate limiter"""

import time
from collections import defaultdict


class TokenBucket:
    def __init__(self, cap, refill):
        self.cap = cap
        self.tokens = cap
        self.refill = refill
        self.last = time.time()

    def consume(self, n=1):
        self._refill()
        if self.tokens >= n:
            self.tokens -= n
            return True
        return False

    def _refill(self):
        new = (time.time() - self.last) * self.refill
        self.tokens = min(self.cap, self.tokens + new)
        self.last = time.time()


_limits = defaultdict(dict)


def check_limit(key_id, limit):
    if key_id not in _limits:
        _limits[key_id] = TokenBucket(limit, limit / 60)
    return _limits[key_id].consume()
