import logging
from client_tier import ClientTiers, TierConfig, Tier
from rate_limiter_strategies.interface import RateLimitStrategy

logger = logging.getLogger(__name__)

class RateLimitService:
    def __init__(self, strategy: RateLimitStrategy, clientTiers: ClientTiers, tierConfig: TierConfig) -> None:
        self.strategy = strategy
        self.clientTiers = clientTiers
        self.tierConfig = tierConfig
        self._loggedUnknownClients: set[int] = set()
    
    def allowRequests(self, clientId: int) -> bool:
        clientTier = self.clientTiers.get(clientId)
        if not clientTier:
            clientTier = Tier.FREE
            if clientId not in self._loggedUnknownClients:
                self._loggedUnknownClients.add(clientId)
                logger.info("client=%s unknown, using %s", clientId, clientTier.name)
        tierLimit = TierConfig[clientTier]
        return self.strategy.allow(clientId, tierLimit)