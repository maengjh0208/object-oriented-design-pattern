from structural.adapter.legacy_gateway import LegacyGateway
from structural.adapter.payment_gateway_adapter import PaymentGatewayAdapter


class SpyLegacyGateway:
    def __init__(self):
        self.received_args = None

    def make_payment(self, amount_in_cents, currency):
        self.received_args = (amount_in_cents, currency)
        return {"success": True}


def test_pay_converts_amount_to_cents_before_calling_legacy():
    spy = SpyLegacyGateway()
    adapter = PaymentGatewayAdapter(spy)

    adapter.pay(10.0)

    assert spy.received_args == (1000, "USD")


def test_pay_returns_true_for_valid_amount():
    adapter = PaymentGatewayAdapter(LegacyGateway())
    assert adapter.pay(10.0) is True


def test_pay_returns_false_for_non_positive_amount():
    adapter = PaymentGatewayAdapter(LegacyGateway())
    assert adapter.pay(0) is False
