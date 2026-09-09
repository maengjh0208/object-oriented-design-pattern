import pytest

from behavioral.strategy.cart import Cart
from behavioral.strategy.discount import FixedDiscount, NoDiscount, PercentageDiscount


def test_empty_cart_total_is_zero():
    assert Cart().total() == 0


def test_cart_sums_item_prices_with_no_discount():
    cart = Cart(NoDiscount())
    cart.add(3000)
    cart.add(7000)
    assert cart.total() == 10000


def test_percentage_discount_applies_rate():
    cart = Cart(PercentageDiscount(0.1))
    cart.add(10000)
    assert cart.total() == 9000


def test_fixed_discount_subtracts_amount():
    cart = Cart(FixedDiscount(2000))
    cart.add(10000)
    assert cart.total() == 8000


def test_fixed_discount_never_returns_negative():
    cart = Cart(FixedDiscount(5000))
    cart.add(1000)
    assert cart.total() == 0


def test_discount_can_be_swapped_at_runtime():
    cart = Cart()
    cart.add(10000)
    assert cart.total() == 10000

    cart.set_discount(PercentageDiscount(0.2))
    assert cart.total() == 8000


def test_percentage_discount_rejects_rate_out_of_range():
    with pytest.raises(ValueError):
        PercentageDiscount(1.5)

    with pytest.raises(ValueError):
        PercentageDiscount(-0.1)
