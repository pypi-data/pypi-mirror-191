from api.constant.interval import Interval
from api.constant.order_side import OrderSide
from api.interface.future import IFuture


def future_samples(api: IFuture, symbol: str, interval: Interval, quantity: float, price: float, stop_price: float,
                   leverage: int = 20):
    # get ping
    print('get ping:')
    ping = api.get_ping()
    print("ping: {}".format(ping))

    # get symbols
    print('\nget all symbols:')
    symbols = api.get_symbols()
    print(symbols)

    # get symbols info
    print('\nget all symbols info:')
    symbols_info = api.get_symbols_info()
    print()

    # get symbol info
    print('\nget symbol info:')
    symbol_info = api.get_symbol_info(symbol)
    print()

    # get daily ticker price change
    print('\nget daily ticker price change:')
    daily_ticker = api.get_daily_ticker_price_change(symbol)
    print()

    # get all order books ticker
    print('\nget all order books ticker:')
    order_books_ticker = api.get_order_books_ticker()
    print()

    # get order book ticker
    print('\nget order book ticker:')
    order_book_ticker = api.get_order_book_ticker(symbol)
    print()

    # get order book
    print('\nget order book:')
    order_book = api.get_order_book(symbol)
    print()

    # get price ticker
    print('\nget price ticker:')
    price_ticker = api.get_price_ticker(symbol)
    print(price_ticker.last_traded_price, price_ticker.last_traded_quantity)

    # get candles
    print('\nget candles:')
    candles = api.get_candles(symbol, interval)
    print(candles[-1].datetime, candles[-1].close)

    # get open interest
    print('\nget open interest:')
    open_interest = api.get_open_interest(symbol)
    print()

    # get open interests
    print('\nget open interests:')
    open_interests = api.get_open_interests(symbol, interval)
    print()

    # get historical open interests
    print('\nget historical open interests:')
    open_interests = api.get_historical_open_interests(symbol, interval)
    print()

    # get historical top accounts long short ratios
    print('\nget top accounts long short ratios:')
    long_short_ratios = api.get_top_accounts_long_short_ratios(symbol, interval)
    print()

    # get historical top accounts long short ratios
    print('\nget historical top accounts long short ratios:')
    long_short_ratios = api.get_top_accounts_long_short_ratios(symbol, interval)
    print()

    # get historical top positions long short ratios
    print('\nget top positions long short ratios:')
    long_short_ratios = api.get_top_positions_long_short_ratios(symbol, interval)
    print()

    # get historical top positions long short ratios
    print('\nget historical top positions long short ratios:')
    long_short_ratios = api.get_historical_top_positions_long_short_ratios(symbol, interval)
    print()

    # get historical long short ratios
    print('\nget long short ratios:')
    long_short_ratios = api.get_long_short_ratios(symbol, interval)
    print()

    # get historical long short ratios
    print('\nget historical long short ratios:')
    long_short_ratios = api.get_historical_long_short_ratios(symbol, interval)
    print()

    # get buy sell ratios
    print('\nget buy sell ratios:')
    buy_sell_ratios = api.get_takers_buy_sell_ratios(symbol, interval)
    print()

    # get historical buy sell ratios
    print('\nget historical buy sell ratios:')
    buy_sell_ratios = api.get_historical_takers_buy_sell_ratios(symbol, interval)
    print()

    # get total balance
    print('\nget total balance:')
    balance = api.get_balance()
    print(balance.total, balance.available)

    # get leverage
    print('\nget leverage:')
    exchange_leverage = api.get_leverage(symbol)
    print(exchange_leverage)

    # set leverage
    print('\nset leverage:')
    is_set = api.set_leverage(symbol, leverage)
    print(is_set)

    # post limit order
    print('\nplace limit order:')
    order_id = api.post_limit_order(symbol=symbol, side=OrderSide.BUY, quantity=quantity, price=price)
    print(order_id)

    # post market order
    print('\nplace market order:')
    order_id = api.post_market_order(symbol=symbol, side=OrderSide.BUY, quantity=quantity)
    print(order_id)

    # post stop market order
    print('\nplace stop market order:')
    order_id = api.post_stop_market_order(symbol=symbol, side=OrderSide.BUY, quantity=quantity, stop_price=stop_price)
    print(order_id)

    # get order
    print('\nget order:')
    order = api.get_order(symbol=symbol, order_id=order_id)
    print(order.id)

    # get all open orders
    print('\nget all open order:')
    orders = api.get_open_orders(symbol=symbol)
    print([order.id for order in orders])

    # cancel order
    print('\ncancel order:')
    is_canceled = api.cancel_order(symbol=symbol, order_id=order_id)
    print(is_canceled)

    # cancel all open orders
    print('\ncancel all open order:')
    is_canceled = api.cancel_open_orders(symbol=symbol)
    print(is_canceled)

    # get position
    print('\nget position:')
    position = api.get_position(symbol=symbol)
    print(position.quantity)
