from behavioral.strategy.discount import NoDiscount


def test_no_discount_returns_price_unchanged():
    assert NoDiscount().apply(10000) == 10000
