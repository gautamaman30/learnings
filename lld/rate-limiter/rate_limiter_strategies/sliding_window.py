import logging
import threading
import time
from dataclasses import dataclass, field
from .interface import RateLimitStrategy
from collections import deque
from client_tier import Limit

logger = logging.getLogger(__name__)

@dataclass
class WindowState:
    _timestamps: deque[int] = field(default_factory=deque)

    def prune(self, currentTimestampMs: int, windowMs: int) -> None:
        cutoffTimestampMs = currentTimestampMs - windowMs
        while self._timestamps and self._timestamps[0] < cutoffTimestampMs:
            self._timestamps.popleft()

    def record(self, currentTimestampMs: int, windowMs: int) -> int:
        self.prune(currentTimestampMs, windowMs)
        self._timestamps.append(currentTimestampMs)
        return len(self._timestamps)
    
    def getWindowSize(self) -> int:
        return len(self._timestamps)

class SlidingWindowStrategy(RateLimitStrategy):
    # Map<clientId, WindowState>
    windows: dict[int, WindowState]

    def __init__(self):
        self.windows = {}
        self._lock = threading.Lock()

    def allow(self, clientId: int, clientLimit: Limit):
        with self._lock:
            currentTimestampMs = time.time_ns() // 1_000_000
            windowState = self.windows.get(clientId)
            if not windowState:
                windowState = WindowState()
                currentClientLimit = windowState.record(currentTimestampMs, clientLimit.windowMs)
                self.windows[clientId] = windowState
                logger.info(
                    "client=%s new window used=%s/%s ALLOW",
                    clientId, currentClientLimit, clientLimit.limit,
                )
                return True
            else:
                windowState.prune(currentTimestampMs, clientLimit.windowMs)
                if windowState.getWindowSize() < clientLimit.limit:
                    used = self.windows[clientId].record(currentTimestampMs, clientLimit.windowMs)
                    logger.info("client=%s used=%s/%s ALLOW", clientId, used, clientLimit.limit)
                    return True
            used = windowState.getWindowSize()
            logger.info("client=%s used=%s/%s DENY", clientId, used, clientLimit.limit)
            return False

            