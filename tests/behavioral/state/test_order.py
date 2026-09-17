import pytest

from behavioral.state.order import Order
from behavioral.state.order_status import InvalidTransitionError


def test_starts_pending():
    order = Order()
    assert order.status == "Pending"


def test_pay_transition_to_paid():
    order = Order()
    order.pay()
    assert order.status == "Paid"


def test_ship_transition_to_shipping():
    order = Order()
    order.pay()
    order.ship()
    assert order.status == "Shipping"


def test_deliver_transition_to_delivered():
    order = Order()
    order.pay()
    order.ship()
    order.deliver()
    assert order.status == "Delivered"


def test_cancel_from_pending_transition_to_cancelled():
    order = Order()
    order.cancel()
    assert order.status == "Cancelled"


def test_cancel_from_paid_transition_to_cancelled():
    order = Order()
    order.pay()
    order.cancel()
    assert order.status == "Cancelled"


def test_cannot_cancel_after_shipping():
    order = Order()
    order.pay()
    order.ship()
    with pytest.raises(InvalidTransitionError):
        order.cancel()
