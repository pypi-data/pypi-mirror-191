from datetime import datetime


class DailyTickerPriceChange:
    def __init__(self):
        self.symbol = None
        self.price_change = None
        self.price_change_percentage = None
        self.weighted_average_price = None
        self.last_price = None
        self.last_quantity = None
        self.open_price = None
        self.high_price = None
        self.low_price = None
        self.volume = None
        self.quote_volume = None
        self.open_timestamp = None
        self.open_datetime = None
        self.close_timestamp = None
        self.close_datetime = None
        self.first_trade_id = None
        self.last_trade_id = None
        self.trades_count = None

    @staticmethod
    def create_instance_for_binance(data, symbol: str):
        instance = DailyTickerPriceChange()

        instance.symbol = symbol
        instance.price_change = float(data['priceChange'])
        instance.price_change_percentage = float(data['priceChangePercent'])
        instance.weighted_average_price = float(data['weightedAvgPrice'])
        instance.last_price = float(data['lastPrice'])
        instance.last_quantity = float(data['lastQty'])
        instance.open_price = float(data['openPrice'])
        instance.high_price = float(data['highPrice'])
        instance.low_price = float(data['lowPrice'])
        instance.volume = float(data['volume'])
        instance.quote_volume = float(data['quoteVolume'])
        instance.open_timestamp = int(data['openTime'])
        instance.close_timestamp = int(data['closeTime'])
        instance.first_trade_id = int(data['firstId'])
        instance.last_trade_id = int(data['lastId'])
        instance.trades_count = int(data['count'])

        instance.open_datetime = datetime.fromtimestamp(instance.open_timestamp / 1000)
        instance.close_datetime = datetime.fromtimestamp(instance.close_timestamp / 1000)

        return instance
