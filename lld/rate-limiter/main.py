import logging
import random
import time
from rate_limiter_service import RateLimitService
# from rate_limiter_strategies.sliding_window import SlidingWindowStrategy
from rate_limiter_strategies.token_bucket import TokenBucketStrategy
from client_tier import clientTiers, TierConfig

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(message)s",
    datefmt="%H:%M:%S",
)

service = RateLimitService(TokenBucketStrategy(), clientTiers, TierConfig)

def processRequest(clientId: int):
    return service.allowRequests(clientId)

def simulateTraffic(callsPerMin: int = 1000, minClientId: int = 1, maxClientId: int = 15, durationSeconds: int = 60):
    totalCalls = int((callsPerMin / 60) * durationSeconds)
    interval = 60.0 / callsPerMin  # Time between calls in seconds

    allowedCount = 0
    blockedCount = 0

    print(f"Starting {totalCalls} requests over {durationSeconds}s ({callsPerMin} calls/min)...")
    startTime = time.perf_counter()

    for _ in range(totalCalls):
        loopStart = time.perf_counter()

        clientId = random.randint(minClientId, maxClientId)
        if processRequest(clientId):
            allowedCount += 1
        else:
            blockedCount += 1

        # Adjust sleep time to prevent drift
        elapsed = time.perf_counter() - loopStart
        time.sleep(max(0.0, interval - elapsed))

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
    simulateTraffic(callsPerMin=1000, minClientId=1, maxClientId=5, durationSeconds=60)