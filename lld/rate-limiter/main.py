import logging
import random
import threading
import time
from rate_limiter_service import RateLimitService
# from rate_limiter_strategies.sliding_window import SlidingWindowStrategy
from rate_limiter_strategies.token_bucket import TokenBucketStrategy
from client_tier import clientTiers, TierConfig

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(threadName)s] %(message)s",
    datefmt="%H:%M:%S",
)

service = RateLimitService(TokenBucketStrategy(), clientTiers, TierConfig)

def processRequest(clientId: int):
    return service.allowRequests(clientId)

def simulateTraffic(
    callsPerMin: int = 1000,
    minClientId: int = 1,
    maxClientId: int = 15,
    durationSeconds: int = 60,
    threadCount: int = 4,
):
    totalCalls = int((callsPerMin / 60) * durationSeconds)
    interval = (60.0 / callsPerMin) * threadCount
    allowedCount = 0
    blockedCount = 0
    countLock = threading.Lock()

    def worker(nCalls: int):
        nonlocal allowedCount, blockedCount
        for _ in range(nCalls):
            loopStart = time.perf_counter()
            clientId = random.randint(minClientId, maxClientId)
            allowed = processRequest(clientId)
            with countLock:
                if allowed:
                    allowedCount += 1
                else:
                    blockedCount += 1
            elapsed = time.perf_counter() - loopStart
            time.sleep(max(0.0, interval - elapsed))

    base, rem = divmod(totalCalls, threadCount)
    threads = [
        threading.Thread(
            target=worker,
            args=(base + (1 if i < rem else 0),),
            name=f"w{i + 1}",
        )
        for i in range(threadCount)
    ]

    print(
        f"Starting {totalCalls} requests over {durationSeconds}s "
        f"({callsPerMin} calls/min, {threadCount} threads)..."
    )
    startTime = time.perf_counter()
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()

    totalElapsed = time.perf_counter() - startTime
    summary = {
        "totalRequests": totalCalls,
        "allowed": allowedCount,
        "blocked": blockedCount,
        "elapsedSeconds": round(totalElapsed, 2)
    }
    print(f"Done in {summary['elapsedSeconds']}s | Allowed: {allowedCount} | Blocked: {blockedCount}")
    return summary

if __name__ == '__main__':
    simulateTraffic(callsPerMin=1000, minClientId=1, maxClientId=5, durationSeconds=60, threadCount=4)


# ┌───────────────────────────────┐
# │ RateLimitService              │
# │ - strategy: RateLimitStrategy │  (injected via constructor)
# │ - clientTiers: Map<clientId, Tier>
# │ - tierConfig: TierConfig      │
# │ + allowRequest(clientId): bool│
# └───────────────┬───────────────┘
#         uses    │         has
#                 ▼          ┌────────────────────────────┐
# ┌──────────────────────────┐   │ TierConfig                 │
# │ «interface»              │   │ - limits: Map<Tier, Limit> │
# │ RateLimitStrategy        │   │ + getLimit(tier): Limit    │
# │ + allow(clientId, limit) │   └────────────────────────────┘
# └──────────────────────────┘     enum Tier { FREE, PRO, MAX }
#      ▲                ▲          Limit { maxRequests, windowMs }
#      │ implements     │ implements
# ┌──────────────────────────┐  ┌──────────────────────────┐
# │ TokenBucketStrategy      │  │ SlidingWindowStrategy    │
# │ - buckets: ConcurrentMap │  │ - windows: ConcurrentMap │
# │   <clientId, BucketState>│  │   <clientId, WindowState>│
# └────────────┬─────────────┘  └────────────┬─────────────┘
#              │ has                         │ has
# ┌──────────────────────────┐  ┌──────────────────────────┐
# │ BucketState              │  │ WindowState              │
# │ - tokens: double         │  │ - timestamps: Deque<long>│
# │ - lastRefillMs: long     │  └──────────────────────────┘
# └──────────────────────────┘