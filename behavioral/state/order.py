from behavioral.state.order_status import OrderStatus, Pending


class Order:
    def __init__(self):
        self._status: OrderStatus = Pending()

    @property
    def status(self):
        return type(self._status).__name__

    @status.setter
    def status(self, state: OrderStatus):
        self._status = state

    def pay(self):
        self._status.pay(self)

    def ship(self):
        self._status.ship(self)

    def deliver(self):
        self._status.deliver(self)

    def cancel(self):
        self._status.cancel(self)
