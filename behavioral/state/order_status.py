class InvalidTransitionError(Exception):
    pass


class OrderStatus:
    def pay(self, order):
        raise InvalidTransitionError(f"{type(self).__name__} 상태에서는 결제할 수 없음")

    def ship(self, order):
        raise InvalidTransitionError(f"{type(self).__name__} 상태에서는 배송을 시작할 수 없음")

    def deliver(self, order):
        raise InvalidTransitionError(f"{type(self).__name__} 상태에서는 배송완료 처리할 수 없음")

    def cancel(self, order):
        raise InvalidTransitionError(f"{type(self).__name__} 상태에서는 취소할 수 없음")


class Pending(OrderStatus):
    def pay(self, order):
        order.status = Paid()

    def cancel(self, order):
        order.status = Cancelled()


class Paid(OrderStatus):
    def ship(self, order):
        order.status = Shipping()

    def cancel(self, order):
        order.status = Cancelled()


class Shipping(OrderStatus):
    def deliver(self, order):
        order.status = Delivered()


class Delivered(OrderStatus):
    pass


class Cancelled(OrderStatus):
    pass
