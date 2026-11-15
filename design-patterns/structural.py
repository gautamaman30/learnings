from abc import ABC, abstractmethod

class PaymentProcessor:
    @abstractmethod
    def process_payment(self, amount_in_cents: int) -> bool:
        pass

class StripeSDK:
    def process_charge(self, amount_in_dollars: int) -> dict:
        print('Processed in stripe')
        return { "status": "success" }
    
class StripeAdapter(PaymentProcessor):
    def __init__(self):
        self.stripe_processor = StripeSDK()

    def process_payment(self, amount_in_cents: int):
        response = self.stripe_processor.process_charge(amount_in_cents/100)
        return response["status"] == "success"

def checkout_service(payment_processor: PaymentProcessor, amount: int):
    if payment_processor.process_payment(amount):
        print('Order confirmed')

checkout_service(StripeAdapter(), 50)