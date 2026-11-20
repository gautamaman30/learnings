from enum import Enum
from dataclasses import dataclass

class Tier(Enum):
    FREE = 1
    PRO = 2
    MAX = 3

@dataclass
class Limit:
    limit: int
    windowMs: int

TierConfig: dict[Tier, Limit] = {
    Tier.FREE: Limit(50, 30000),
    Tier.PRO: Limit(100, 30000), 
    Tier.MAX: Limit(200, 30000),
}

ClientTiers = dict[int, Tier]

clientTiers: ClientTiers = {
    1: Tier.FREE,
    2: Tier.PRO,
    3: Tier.MAX,
    # 4: Tier.PRO,
    # 5: Tier.PRO,
    # 6: Tier.MAX,
    # 7: Tier.MAX,
    # 8: Tier.MAX,
    # 9: Tier.MAX,
    # 10: Tier.MAX,
}