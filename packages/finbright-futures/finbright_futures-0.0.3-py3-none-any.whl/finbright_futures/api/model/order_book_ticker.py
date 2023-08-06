from datetime import datetime


class OrderBookTicker:
    def __init__(self):
        self.timestamp = None
        self.datetime = None
        self.symbol = None
        self.best_ask_price = None
        self.best_ask_quantity = None
        self.best_bid_price = None
        self.best_bid_quantity = None

    @staticmethod
    def create_instance_for_binance(data, symbol):
        instance = OrderBookTicker()

        instance.timestamp = int(data['time'])
        instance.datetime = datetime.fromtimestamp(instance.timestamp / 1000)
        instance.symbol = symbol
        instance.best_ask_price = float(data['askPrice'])
        instance.best_ask_quantity = float(data['askQty'])
        instance.best_bid_price = float(data['bidPrice'])
        instance.best_bid_quantity = float(data['bidQty'])

        return instance
