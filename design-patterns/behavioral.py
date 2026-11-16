from abc import ABC, abstractmethod

# Strategy Pattern

class PricingStrategy(ABC):
    @abstractmethod
    def calculate_total_price(self, base_amount: float) -> float:
        pass
    
class StandardPricing(PricingStrategy):
    def calculate_total_price(self, base_amount: float):
        return base_amount

class SalePricing(PricingStrategy):
    def calculate_total_price(self, base_amount: float):
        return base_amount * 0.5

class VIPPricing(PricingStrategy):
    def calculate_total_price(self, base_amount: float):
        return base_amount * 0.8

class CalculateService:
    def __init__(self, pricingStrategy: PricingStrategy):
        self._strategy = pricingStrategy

    def set_pricing(self, pricingStrategy: PricingStrategy):
        self._strategy = pricingStrategy

    def get_final_price(self, base_amount: float):
        return self._strategy.calculate_total_price(base_amount)


calcService = CalculateService(SalePricing())

print(calcService.get_final_price(500))

calcService.set_pricing(VIPPricing())

print(calcService.get_final_price(500))

