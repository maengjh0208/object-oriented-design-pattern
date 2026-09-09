from abc import ABC, abstractmethod


class DiscountPolicy(ABC):
    @abstractmethod
    def apply(self, price: int) -> int:
        pass


class NoDiscount(DiscountPolicy):
    def apply(self, price: int) -> int:
        return price


class PercentageDiscount(DiscountPolicy):
    def __init__(self, rate: float):
        if not 0 <= rate <= 1:
            raise ValueError("Rate must be between 0 and 1")

        self._rate = rate

    def apply(self, price: int) -> int:
        discount_amount = round(price * self._rate)
        return price - discount_amount


class FixedDiscount(DiscountPolicy):
    def __init__(self, amount: int):
        self._amount = amount

    def apply(self, price: int) -> int:
        return max(price - self._amount, 0)
