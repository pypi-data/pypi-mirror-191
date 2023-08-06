from datetime import datetime


class OpenInterest:
    def __init__(self):
        self.symbol = None
        self.open_interest = None
        self.timestamp = None
        self.datetime = None

    @staticmethod
    def create_instance_for_binance(data, symbol: str):
        instance = OpenInterest()

        instance.symbol = symbol
        instance.open_interest = float(data['openInterest'])
        instance.timestamp = int(data['time'])

        instance.datetime = datetime.fromtimestamp(instance.timestamp / 1000)

        return instance
