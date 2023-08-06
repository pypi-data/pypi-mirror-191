class OrderSide:
    SELL = 'SELL'
    BUY = 'BUY'

    @staticmethod
    def get_reverse(side):
        return OrderSide.SELL if OrderSide.BUY == side else OrderSide.BUY
