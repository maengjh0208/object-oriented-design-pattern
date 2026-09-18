from structural.adapter.payment_processor import PaymentProcessor


class PaymentGatewayAdapter(PaymentProcessor):
    def __init__(self, legacy_gateway):
        self._legacy_gateway = legacy_gateway

    def pay(self, amount: float) -> bool:
        cents = round(amount * 100)
        result = self._legacy_gateway.make_payment(cents, "USD")
        return result["success"]
