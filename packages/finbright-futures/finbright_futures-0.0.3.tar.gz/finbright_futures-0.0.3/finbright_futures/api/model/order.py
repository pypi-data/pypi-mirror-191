from finbright_futures.api.constant.order_type import OrderType


class Order:
    def __init__(self):
        self.id = None
        self.type = None
        self.symbol = None
        self.status = None
        self.side = None
        self.quantity = None
        self.executed_quantity = None
        self.price = None
        self.average_price = None
        self.stop_price = None
        self.call_back_rate = None

    @staticmethod
    def create_instance_for_binance(data, symbol):
        instance = Order()

        instance.id = data['orderId']
        instance.type = data['origType']
        instance.symbol = symbol
        instance.status = data['status']
        instance.side = data['side']
        instance.quantity = float(data['origQty'])
        instance.executed_quantity = float(data['executedQty'])
        instance.price = float(data['price'])
        instance.average_price = float(data['avgPrice'])
        instance.stop_price = float(data['stopPrice'])

        if OrderType.TRAILING_STOP_MARKET == instance.type:
            instance.stop_price = float(data['activationPrice'])
            instance.call_back_rate = float(data['priceRate'])

        return instance
