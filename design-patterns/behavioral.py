from abc import ABC, abstractmethod

# Strategy Pattern

# class PricingStrategy(ABC):
#     @abstractmethod
#     def calculate_total_price(self, base_amount: float) -> float:
#         pass
    
# class StandardPricing(PricingStrategy):
#     def calculate_total_price(self, base_amount: float):
#         return base_amount

# class SalePricing(PricingStrategy):
#     def calculate_total_price(self, base_amount: float):
#         return base_amount * 0.5

# class VIPPricing(PricingStrategy):
#     def calculate_total_price(self, base_amount: float):
#         return base_amount * 0.8

# class CalculateService:
#     def __init__(self, pricingStrategy: PricingStrategy):
#         self._strategy = pricingStrategy

#     def set_pricing(self, pricingStrategy: PricingStrategy):
#         self._strategy = pricingStrategy

#     def get_final_price(self, base_amount: float):
#         return self._strategy.calculate_total_price(base_amount)


# calcService = CalculateService(SalePricing())

# print(calcService.get_final_price(500))

# calcService.set_pricing(VIPPricing())

# print(calcService.get_final_price(500))




# Observer Pattern 

# class UserObserver(ABC):
#     @abstractmethod
#     def update(self, username: str):
#         pass

# # 2. Concrete Observers
# class EmailService(UserObserver):
#     def update(self, username: str):
#         print(f"[EmailService] Sending welcome email to {username}")

# class AnalyticsService(UserObserver):
#     def update(self, username: str):
#         print(f"[AnalyticsService] Logging user signup event for {username}")

# # 3. Subject
# class UserService:
#     def __init__(self):
#         self._observers = []

#     def attach(self, observer: UserObserver):
#         self._observers.append(observer)

#     def register_user(self, username: str):
#         print(f"User '{username}' registered successfully.")
#         # Notify all subscribed observers
#         for observer in self._observers:
#             observer.update(username)

# # --- Usage ---
# service = UserService()
# service.attach(EmailService())
# service.attach(AnalyticsService())

# service.register_user("alice_dev")