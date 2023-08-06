from datetime import datetime


class PriceTicker:
    def __init__(self):
        self.timestamp = None
        self.datetime = None
        self.symbol = None
        self.last_traded_price = None
        self.last_traded_quantity = None

    @staticmethod
    def create_instance_for_binance(data, symbol):
        instance = PriceTicker()

        instance.timestamp = int(data['time'])
        instance.datetime = datetime.fromtimestamp(instance.timestamp / 1000)
        instance.symbol = symbol
        instance.last_traded_price = float(data['price'])

        return instance
