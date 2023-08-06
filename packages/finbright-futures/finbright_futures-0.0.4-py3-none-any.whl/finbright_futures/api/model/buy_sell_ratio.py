from datetime import datetime


class BuySellRatio:
    def __init__(self):
        self.buy_sell_ratio = None
        self.buy_volume = None
        self.sell_volume = None
        self.timestamp = None
        self.datetime = None

    @staticmethod
    def create_instance_for_binance(data):
        instance = BuySellRatio()

        instance.buy_sell_ratio = float(data['buySellRatio'])
        instance.buy_volume = float(data['buyVol'])
        instance.sell_volume = float(data['sellVol'])
        instance.timestamp = float(data['timestamp'])

        instance.datetime = datetime.fromtimestamp(instance.timestamp / 1000)

        return instance
