from datetime import datetime


class Candle:
    def __init__(self):
        self.timestamp = None
        self.datetime = None
        self.open = None
        self.high = None
        self.low = None
        self.close = None
        self.volume = None
        self.trades = None

    def get_array(self):
        return [self.timestamp, self.open, self.high, self.low, self.close, self.volume, self.trades]

    @staticmethod
    def create_instance_with_array(array):
        instance = Candle()

        instance.timestamp = int(array[0])
        instance.datetime = datetime.fromtimestamp(instance.timestamp)
        instance.open = float(array[1])
        instance.high = float(array[2])
        instance.low = float(array[3])
        instance.close = float(array[4])
        instance.volume = float(array[5])
        instance.trades = int(array[6])

        return instance

    @staticmethod
    def create_instance_for_binance(data):
        instance = Candle()

        instance.timestamp = int(data[0] / 1000)  # convert unit of time to second
        instance.datetime = datetime.fromtimestamp(instance.timestamp)
        instance.open = float(data[1])
        instance.high = float(data[2])
        instance.low = float(data[3])
        instance.close = float(data[4])
        instance.volume = float(data[5])
        instance.trades = int(data[8])

        return instance
