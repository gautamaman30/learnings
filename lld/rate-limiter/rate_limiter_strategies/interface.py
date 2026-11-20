from abc import ABC, abstractmethod
from client_tier import Limit

class RateLimitStrategy(ABC):
    @abstractmethod
    def allow(self, clientId: int, clientLimit: Limit) -> bool:
        pass