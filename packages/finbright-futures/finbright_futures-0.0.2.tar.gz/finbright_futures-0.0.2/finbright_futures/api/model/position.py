from api.constant.position_side import PositionSide


class Position:
    def __init__(self):
        self.symbol = None
        self.side = None
        self.quantity = None
        self.margin_mode = None
        self.entry_price = None
        self.mark_price = None
        self.pnl = None
        self.leverage = None
        self.liquidation_price = None

    @staticmethod
    def create_instance_for_binance(data, symbol):
        instance = Position()

        instance.symbol = symbol
        instance.side = PositionSide.LONG if 0 < float(data['positionAmt']) else PositionSide.SHORT
        instance.quantity = abs(float(data['positionAmt']))
        instance.margin_mode = str.upper(data['marginType'])
        instance.entry_price = float(data['entryPrice'])
        instance.mark_price = float(data['markPrice'])
        instance.pnl = float(data['unRealizedProfit'])
        instance.leverage = float(data['leverage'])
        instance.liquidation_price = float(data['liquidationPrice'])

        return instance
