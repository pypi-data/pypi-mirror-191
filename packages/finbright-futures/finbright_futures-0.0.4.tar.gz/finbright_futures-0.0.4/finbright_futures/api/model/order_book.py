from datetime import datetime

from finbright_futures.api.model.order_book_row import OrderBookRow


class OrderBook:
    def __init__(self):
        self.timestamp = None
        self.datetime = None
        self.bids = None
        self.asks = None

    @staticmethod
    def create_instance_for_binance(data):
        instance = OrderBook()

        instance.timestamp = int(data['E'])
        instance.datetime = datetime.fromtimestamp(instance.timestamp / 1000)
        instance.bids = [OrderBookRow.create_instance_for_binance(item) for item in data['bids']]
        instance.asks = [OrderBookRow.create_instance_for_binance(item) for item in data['asks']]

        return instance
