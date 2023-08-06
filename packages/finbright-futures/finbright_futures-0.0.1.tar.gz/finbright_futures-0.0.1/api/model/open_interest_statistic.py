from datetime import datetime


class OpenInterestStatistic:
    def __init__(self):
        self.symbol = None
        self.sum_open_interest = None
        self.sum_open_interest_value = None
        self.timestamp = None
        self.datetime = None

    @staticmethod
    def create_instance_for_binance(data, symbol: str):
        instance = OpenInterestStatistic()

        instance.symbol = symbol
        instance.sum_open_interest = float(data['sumOpenInterest'])
        instance.sum_open_interest_value = float(data['sumOpenInterestValue'])
        instance.timestamp = int(data['timestamp'])

        instance.datetime = datetime.fromtimestamp(instance.timestamp / 1000)

        return instance
