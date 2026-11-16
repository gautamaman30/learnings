from abc import ABC, abstractmethod

# Adapter Pattern

# class PaymentProcessor:
#     @abstractmethod
#     def process_payment(self, amount_in_cents: int) -> bool:
#         pass

# class StripeSDK:
#     def process_charge(self, amount_in_dollars: int) -> dict:
#         print('Processed in stripe')
#         return { "status": "success" }
    
# class StripeAdapter(PaymentProcessor):
#     def __init__(self):
#         self.stripe_processor = StripeSDK()

#     def process_payment(self, amount_in_cents: int):
#         response = self.stripe_processor.process_charge(amount_in_cents/100)
#         return response["status"] == "success"

# def checkout_service(payment_processor: PaymentProcessor, amount: int):
#     if payment_processor.process_payment(amount):
#         print('Order confirmed')

# checkout_service(StripeAdapter(), 50)


# Decorator Pattern

class DataService(ABC):
    @abstractmethod
    def fetch_data(self, query: str):
        pass
    
class CachingDecoratorService(DataService):
    def __init__(self, service: DataService):
        self._service = service
        self._cache = {}
    
    def fetch_data(self, query: str):
        if query in self._cache:
            print('Using cached data for query', query)
            return self._cache[query]

        response = self._service.fetch_data(query)
        self._cache[query] = response
        return response

class TaxDataService(DataService):
    def fetch_data(self, query: str):
        print('Fetching data for query', query)
        return "Fetched data"
    
service = CachingDecoratorService(TaxDataService())
print(service.fetch_data('Tax 2026'))
print(service.fetch_data('Tax 2026'))
