import logging
import threading
import time
from .interface import RateLimitStrategy
from client_tier import Limit

logger = logging.getLogger(__name__)

class BucketState:
    _tokens: float
    _lastUsedTimestampMs: int

    def __init__(self, maxTokensLimit: float, currentTimestampMs: int) -> None:
        self._tokens = maxTokensLimit
        self._lastUsedTimestampMs = currentTimestampMs

    def fillBucket(self, currentTimestampMs: int, fillRatePerMs: float, maxTokensLimit: float) -> float:
        elapsedTime = max(0, currentTimestampMs - self._lastUsedTimestampMs)
        newTokens = fillRatePerMs * elapsedTime
        self._tokens = min(maxTokensLimit, self._tokens + newTokens)
        self._lastUsedTimestampMs = currentTimestampMs
        return self._tokens

    def useBucket(self):
        if self._tokens < 1:
            return False
        self._tokens = max(self._tokens - 1, 0)
        return True

class TokenBucketStrategy(RateLimitStrategy):
    # Map<clientId, BucketState>
    buckets: dict[int, BucketState]

    def __init__(self):
        self.buckets = {}
        self._lock = threading.Lock()

    def allow(self, clientId: int, clientLimit: Limit):
        with self._lock:
            currentTimestampMs = time.time_ns() // 1_000_000
            bucketState = self.buckets.get(clientId)
            isNew = bucketState is None
            if not bucketState:
                bucketState = BucketState(clientLimit.limit, currentTimestampMs)
                self.buckets[clientId] = bucketState
            fillRatePerMs = clientLimit.limit / clientLimit.windowMs
            bucketState.fillBucket(currentTimestampMs, fillRatePerMs, clientLimit.limit)
            allowed = bucketState.useBucket()
            prefix = "new bucket " if isNew else ""
            logger.info(
                "client=%s %stokens=%.1f/%s %s",
                clientId,
                prefix,
                bucketState._tokens,
                clientLimit.limit,
                "ALLOW" if allowed else "DENY",
            )
            return allowed
            

            