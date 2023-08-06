class OrderBookRow:
    def __init__(self):
        self.price = None
        self.quantity = None
        self.orders_count = None
        self.liquidated_orders_count = None

    @staticmethod
    def create_instance_for_binance(data):
        instance = OrderBookRow()

        instance.price = float(data[0])
        instance.quantity = float(data[1])

        return instance
