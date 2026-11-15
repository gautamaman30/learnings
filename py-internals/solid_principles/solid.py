from abc import ABC, abstractmethod

class Order:
    items = []
    quantities = []
    prices = []
    status = "open"

    def add_item(self, item, quantity, price):
        self.items.append(item)
        self.quantities.append(quantity)
        self.prices.append(price)

    def total_price(self):
        total = 0
        for i in range(len(self.prices)):
            total += (self.prices[i] * self.quantities[i])
        return total
    
# Added Payment Processor to improve single responsibility principle and handling payments separately   

# Payment processor violated open-close principle (open for extension but closed for modification) so we created an abstract payment processor
# Now if we want to add a new payment method let paypal, we can easily create without modification 

# Paypal processor don't use security code but email. Updating it violated Liskov principle as subclass should not break the behavioural contract of the base class. 

# Added sms verification 2FA. But Credit payment processor did not support that so we had to do interface segregation. 

# Used composition to solve interface segregation

# High level modules (processors) depended on a low level module (SmsAuthorizer) but both should depend on a abraction. (Dependency inversion)

class Authorizer(ABC):
    @abstractmethod
    def is_authorized(self):
        pass

class SMSAuthorizer(Authorizer):
    _authorized = False

    def verify_code(self, code):
        print(f"Verifying sms code: {code}")
        self._authorized = True

    def is_authorized(self):
        return self._authorized

class RobotAuthorizer(Authorizer):
    _authorized = False

    def not_a_robot(self):
        print(f"Verifying are you a robot?")
        self._authorized = True

    def is_authorized(self):
        return self._authorized

class PaymentProcessor(ABC):
    @abstractmethod
    def pay(self, order):
        pass

class CreditPaymentProcessor(PaymentProcessor):
    def __init__(self, security_code):
        self.security_code = security_code

    def pay(self, order):
        print("Processing credit method")
        print(f"Verifying security code: {self.security_code}")
        order.status = "paid"

class DebitPaymentProcessor(PaymentProcessor):

    def __init__(self, security_code, authorizer: Authorizer):
        self.security_code = security_code
        self.authorizer = authorizer

    def pay(self, order):
        if not self.authorizer.is_authorized():
            raise Exception('Sms code not verified')
        print("Processing debit method")
        print(f"Verifying security code: {self.security_code}")
        order.status = "paid"

class PaypalPaymentProcessor(PaymentProcessor):

    def __init__(self, email, authorizer: Authorizer):
        self.email = email
        self.authorizer = authorizer

    def pay(self, order):
        if not self.authorizer.is_authorized():
            raise Exception('Sms code not verified')
        print("Processing paypal method")
        print(f"Verifying email: {self.email}")
        order.status = "paid"

order = Order()
order.add_item("Iphone", 1, 1000)
order.add_item("Shoes", 5, 500)
order.add_item("chocolates", 10, 10)
print('Total price:', order.total_price())

robotAuthorizer = RobotAuthorizer()
robotAuthorizer.not_a_robot()
paymentProcessor = PaypalPaymentProcessor("abc@gmail.com", robotAuthorizer)
paymentProcessor.pay(order)