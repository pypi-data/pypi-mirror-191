import math
from datetime import datetime


class SymbolInfo:
    def __init__(self):
        self.on_board_timestamp = None
        self.on_board_datetime = None
        self.base_asset = None
        self.quote_asset = None
        self.symbol = None
        self.exchange_symbol = None
        self.price_precision = None
        self.minimum_price = None
        self.maximum_price = None
        self.quantity_precision = None
        self.minimum_quantity = None
        self.maximum_quantity = None
        self.lot_precision = None
        self.maximum_order_count = None
        self.maximum_algo_order_count = None

    @staticmethod
    def create_instance_for_binance(data):
        instance = SymbolInfo()

        instance.on_board_timestamp = int(data['onboardDate'])
        instance.on_board_datetime = datetime.fromtimestamp(instance.on_board_timestamp / 1000)
        instance.base_asset = data['baseAsset']
        instance.quote_asset = data['quoteAsset']
        instance.symbol = instance.base_asset + '-' + instance.quote_asset
        instance.exchange_symbol = data['symbol']
        instance.price_precision = int(math.log10(float(data['filters'][0]['tickSize'])) * -1)
        instance.minimum_price = float(data['filters'][0]['minPrice'])
        instance.maximum_price = float(data['filters'][0]['maxPrice'])
        instance.quantity_precision = int(math.log10(float(data['filters'][1]['stepSize'])) * -1)
        instance.minimum_quantity = float(data['filters'][1]['minQty'])
        instance.maximum_quantity = float(data['filters'][1]['maxQty'])
        instance.maximum_order_count = int(data['filters'][3]['limit'])
        instance.maximum_algo_order_count = int(data['filters'][4]['limit'])

        return instance
