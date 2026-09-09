from behavioral.strategy.discount import DiscountPolicy, NoDiscount


# 의존은 Cart -> DiscountPolicy 한 방향이어야 한다.
class Cart:
    def __init__(self, discount: DiscountPolicy | None = None):
        self._items: list[int] = []
        self._discount = discount or NoDiscount()

    def add(self, price: int):
        self._items.append(price)

    def total(self) -> int:
        return self._discount.apply(sum(self._items))

    def set_discount(self, discount: DiscountPolicy):
        self._discount = discount
