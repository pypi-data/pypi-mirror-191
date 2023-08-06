from datetime import datetime

from finbright_futures.api.constant.interval import Interval
from finbright_futures.api.constant.order_side import OrderSide
from finbright_futures.api.constant.time_in_force import TimeInForce
from finbright_futures.api.exchange.binance.binance import Binance
from finbright_futures.api.exchange.binance.request import Request
from finbright_futures.api.interface.future import IFuture
from finbright_futures.api.model.balance import Balance
from finbright_futures.api.model.buy_sell_ratio import BuySellRatio
from finbright_futures.api.model.candle import Candle
from finbright_futures.api.model.daily_ticker_price_change import DailyTickerPriceChange
from finbright_futures.api.model.long_short_ratio import LongShortRatio
from finbright_futures.api.model.open_interest import OpenInterest
from finbright_futures.api.model.open_interest_statistic import OpenInterestStatistic
from finbright_futures.api.model.order import Order
from finbright_futures.api.model.order_book import OrderBook
from finbright_futures.api.model.order_book_ticker import OrderBookTicker
from finbright_futures.api.model.position import Position
from finbright_futures.api.model.price_ticker import PriceTicker
from finbright_futures.api.model.symbol_info import SymbolInfo


class Future(Binance, Request, IFuture):
    def __init__(self, api_key: str, api_secret_key: str, ignore_exceptions: bool = False):
        Request.__init__(self, base_url='https://fapi.binance.com', api_key=api_key,
                         api_secret_key=api_secret_key, ignore_exceptions=ignore_exceptions)
        Binance.__init__(self, name='Binance Future', maximum_requestable_candles=1500)

    def get_server_time(self) -> int:
        endpoint = '/fapi/v1/time'
        response = self._get(endpoint=endpoint)
        server_time = int(response['serverTime'])
        return server_time

    def get_ping(self) -> int:
        local = datetime.now().timestamp() * 1000
        server = self.get_server_time()
        ping = round(server - local)
        return ping

    def get_symbols(self) -> list:
        symbols_info = self.get_symbols_info()
        symbols = [symbol_info.symbol for symbol_info in symbols_info]
        return symbols

    def get_symbols_info(self) -> list:
        endpoint = '/fapi/v1/exchangeInfo'
        response = self._get(endpoint=endpoint)
        symbols_info = [SymbolInfo.create_instance_for_binance(item) for item in response['symbols']
                        if 'PERPETUAL' == item['contractType']]
        return symbols_info

    def get_symbol_info(self, symbol: str) -> SymbolInfo:
        symbols_info = self.get_symbols_info()
        symbol_info = [symbol_info for symbol_info in symbols_info if symbol == symbol_info.symbol][0]
        return symbol_info

    def get_daily_ticker_price_change(self, symbol: str) -> DailyTickerPriceChange:
        endpoint = '/fapi/v1/ticker/24hr'
        params = {'symbol': self._get_exchange_symbol(symbol)}
        response = self._get(endpoint=endpoint, params=params)
        ticker = DailyTickerPriceChange.create_instance_for_binance(response, symbol)
        return ticker

    def get_order_books_ticker(self) -> list:
        endpoint = '/fapi/v1/ticker/bookTicker'
        response = self._get(endpoint=endpoint)
        tickers = [OrderBookTicker.create_instance_for_binance(item, self._get_package_symbol(item['symbol']))
                   for item in response if item['symbol'] in self._exchange_symbols_info_dictionary]
        return tickers

    def get_order_book_ticker(self, symbol: str) -> OrderBookTicker:
        endpoint = '/fapi/v1/ticker/bookTicker'
        params = {'symbol': self._get_exchange_symbol(symbol)}
        response = self._get(endpoint=endpoint, params=params)
        ticker = OrderBookTicker.create_instance_for_binance(response, self._get_package_symbol(response['symbol']))
        return ticker

    def get_order_book(self, symbol: str) -> OrderBook:
        endpoint = '/fapi/v1/depth'
        params = {'symbol': self._get_exchange_symbol(symbol)}
        response = self._get(endpoint=endpoint, params=params)
        order_book = OrderBook.create_instance_for_binance(response)
        return order_book

    def get_price_ticker(self, symbol: str) -> PriceTicker:
        endpoint = '/fapi/v1/ticker/price'
        params = {'symbol': self._get_exchange_symbol(symbol)}
        response = self._get(endpoint=endpoint, params=params)
        price_ticker = PriceTicker.create_instance_for_binance(response, symbol)
        return price_ticker

    def get_candles(self, symbol: str, interval: Interval) -> list:
        endpoint = '/fapi/v1/klines'
        params = {'symbol': self._get_exchange_symbol(symbol), 'interval': self._get_exchange_interval(interval)}
        response = self._get(endpoint=endpoint, params=params)
        candles = [Candle.create_instance_for_binance(item) for item in response]
        return candles

    def get_historical_candles(self, symbol: str, interval: Interval, from_timestamp: int = None,
                               to_timestamp: int = None, limit: int = None) -> list:
        endpoint = '/fapi/v1/klines'
        params = {'symbol': self._get_exchange_symbol(symbol), 'interval': self._get_exchange_interval(interval),
                  'startTime': self._get_exchange_timestamp(from_timestamp),
                  'endTime': self._get_exchange_timestamp(to_timestamp), 'limit': limit}
        response = self._get(endpoint=endpoint, params=params)
        candles = [Candle.create_instance_for_binance(item) for item in response]
        return candles

    def get_open_interest(self, symbol: str) -> OpenInterest:
        endpoint = '/fapi/v1/openInterest'
        params = {'symbol': self._get_exchange_symbol(symbol)}
        response = self._get(endpoint=endpoint, params=params)
        open_interest = OpenInterest.create_instance_for_binance(response, symbol)
        return open_interest

    def get_open_interests(self, symbol: str, interval: Interval) -> [OpenInterestStatistic]:
        endpoint = '/futures/data/openInterestHist'
        params = {'symbol': self._get_exchange_symbol(symbol), 'period': self._get_exchange_interval(interval)}
        response = self._get(endpoint=endpoint, params=params)
        open_interests = [OpenInterestStatistic.create_instance_for_binance(item, symbol) for item in response]
        return open_interests

    def get_historical_open_interests(self, symbol: str, interval: Interval, from_timestamp: int = None,
                                      to_timestamp: int = None, limit: int = None) -> [OpenInterestStatistic]:
        endpoint = '/futures/data/openInterestHist'
        params = {'symbol': self._get_exchange_symbol(symbol), 'period': self._get_exchange_interval(interval),
                  'startTime': self._get_exchange_timestamp(from_timestamp),
                  'endTime': self._get_exchange_timestamp(to_timestamp), 'limit': limit}
        response = self._get(endpoint=endpoint, params=params)
        open_interests = [OpenInterestStatistic.create_instance_for_binance(item, symbol) for item in response]
        return open_interests

    def get_top_accounts_long_short_ratios(self, symbol: str, interval: Interval) -> [LongShortRatio]:
        endpoint = '/futures/data/topLongShortAccountRatio'
        params = {'symbol': self._get_exchange_symbol(symbol), 'period': self._get_exchange_interval(interval)}
        response = self._get(endpoint=endpoint, params=params)
        long_short_ratios = [LongShortRatio.create_instance_for_binance(item, symbol) for item in response]
        return long_short_ratios

    def get_historical_top_accounts_long_short_ratios(self, symbol: str, interval: Interval, from_timestamp: int = None,
                                                      to_timestamp: int = None, limit: int = None) -> [LongShortRatio]:
        endpoint = '/futures/data/topLongShortAccountRatio'
        params = {'symbol': self._get_exchange_symbol(symbol), 'period': self._get_exchange_interval(interval),
                  'startTime': self._get_exchange_timestamp(from_timestamp),
                  'endTime': self._get_exchange_timestamp(to_timestamp), 'limit': limit}
        response = self._get(endpoint=endpoint, params=params)
        long_short_ratios = [LongShortRatio.create_instance_for_binance(item, symbol) for item in response]
        return long_short_ratios

    def get_top_positions_long_short_ratios(self, symbol: str, interval: Interval) -> [LongShortRatio]:
        endpoint = '/futures/data/topLongShortPositionRatio'
        params = {'symbol': self._get_exchange_symbol(symbol), 'period': self._get_exchange_interval(interval)}
        response = self._get(endpoint=endpoint, params=params)
        long_short_ratios = [LongShortRatio.create_instance_for_binance(item, symbol) for item in response]
        return long_short_ratios

    def get_historical_top_positions_long_short_ratios(self, symbol: str, interval: Interval,
                                                       from_timestamp: int = None, to_timestamp: int = None,
                                                       limit: int = None) -> [LongShortRatio]:
        endpoint = '/futures/data/topLongShortPositionRatio'
        params = {'symbol': self._get_exchange_symbol(symbol), 'period': self._get_exchange_interval(interval),
                  'startTime': self._get_exchange_timestamp(from_timestamp),
                  'endTime': self._get_exchange_timestamp(to_timestamp), 'limit': limit}
        response = self._get(endpoint=endpoint, params=params)
        long_short_ratios = [LongShortRatio.create_instance_for_binance(item, symbol) for item in response]
        return long_short_ratios

    def get_long_short_ratios(self, symbol: str, interval: Interval) -> [LongShortRatio]:
        endpoint = '/futures/data/globalLongShortAccountRatio'
        params = {'symbol': self._get_exchange_symbol(symbol), 'period': self._get_exchange_interval(interval)}
        response = self._get(endpoint=endpoint, params=params)
        long_short_ratios = [LongShortRatio.create_instance_for_binance(item, symbol) for item in response]
        return long_short_ratios

    def get_historical_long_short_ratios(self, symbol: str, interval: Interval, from_timestamp: int = None,
                                         to_timestamp: int = None, limit: int = None) -> [LongShortRatio]:
        endpoint = '/futures/data/globalLongShortAccountRatio'
        params = {'symbol': self._get_exchange_symbol(symbol), 'period': self._get_exchange_interval(interval),
                  'startTime': self._get_exchange_timestamp(from_timestamp),
                  'endTime': self._get_exchange_timestamp(to_timestamp), 'limit': limit}
        response = self._get(endpoint=endpoint, params=params)
        long_short_ratios = [LongShortRatio.create_instance_for_binance(item, symbol) for item in response]
        return long_short_ratios

    def get_takers_buy_sell_ratios(self, symbol: str, interval: Interval) -> [BuySellRatio]:
        endpoint = '/futures/data/takerlongshortRatio'
        params = {'symbol': self._get_exchange_symbol(symbol), 'period': self._get_exchange_interval(interval)}
        response = self._get(endpoint=endpoint, params=params)
        long_short_ratios = [BuySellRatio.create_instance_for_binance(item) for item in response]
        return long_short_ratios

    def get_historical_takers_buy_sell_ratios(self, symbol: str, interval: Interval, from_timestamp: int = None,
                                              to_timestamp: int = None, limit: int = None) -> [BuySellRatio]:
        endpoint = '/futures/data/takerlongshortRatio'
        params = {'symbol': self._get_exchange_symbol(symbol), 'period': self._get_exchange_interval(interval),
                  'startTime': self._get_exchange_timestamp(from_timestamp),
                  'endTime': self._get_exchange_timestamp(to_timestamp), 'limit': limit}
        response = self._get(endpoint=endpoint, params=params)
        long_short_ratios = [BuySellRatio.create_instance_for_binance(item) for item in response]
        return long_short_ratios

    def get_balance(self, asset: str = 'USDT') -> Balance:
        endpoint = '/fapi/v2/balance'
        response = self._get_with_signature(endpoint)
        balance = Balance.create_instance_for_binance([item for item in response if asset == item['asset']][0])
        return balance

    def get_leverage(self, symbol: str) -> int:
        position = self.get_position(symbol)
        return position.leverage

    def set_leverage(self, symbol: str, leverage: int) -> bool:
        endpoint = '/fapi/v1/leverage'
        params = {'symbol': self._get_exchange_symbol(symbol), 'leverage': leverage}
        response = self._post_with_signature(endpoint, params)
        return leverage == int(response['leverage'])

    def post_limit_order(self, symbol: str, side: OrderSide, quantity: float, price: float,
                         time_in_force: TimeInForce = TimeInForce.GTX) -> str:
        endpoint = '/fapi/v1/order'
        params = {
            'symbol': self._get_exchange_symbol(symbol),
            'side': side,
            'type': 'LIMIT',
            'quantity': self._round_quantity(symbol, quantity),
            'price': self._round_price(symbol, price),
            'timeInForce': time_in_force
        }
        response = self._post_with_signature(endpoint, params)
        order_id = response['orderId']
        return order_id

    def post_market_order(self, symbol: str, side: OrderSide, quantity: float) -> str:
        endpoint = '/fapi/v1/order'
        params = {
            'symbol': self._get_exchange_symbol(symbol),
            'side': side,
            'type': 'MARKET',
            'quantity': self._round_quantity(symbol, quantity)
        }
        response = self._post_with_signature(endpoint, params)
        order_id = response['orderId']
        return order_id

    def post_stop_market_order(self, symbol: str, side: OrderSide, quantity: float, stop_price: float) -> str:
        endpoint = '/fapi/v1/order'
        params = {
            'symbol': self._get_exchange_symbol(symbol),
            'side': side,
            'type': 'STOP_MARKET',
            'quantity': self._round_quantity(symbol, quantity),
            'stopPrice': self._round_price(symbol, stop_price)
        }
        response = self._post_with_signature(endpoint, params)
        order_id = response['orderId']
        return order_id

    def get_order(self, symbol: str, order_id: str) -> Order:
        endpoint = '/fapi/v1/order'
        params = {'symbol': self._get_exchange_symbol(symbol), 'orderId': order_id}
        response = self._get_with_signature(endpoint, params)
        order = Order.create_instance_for_binance(response, symbol)
        return order

    def get_open_orders(self, symbol: str) -> list:
        endpoint = '/fapi/v1/openOrders'
        params = {'symbol': self._get_exchange_symbol(symbol)}
        response = self._get_with_signature(endpoint, params)
        orders = [Order.create_instance_for_binance(item, symbol) for item in response]
        return orders

    def cancel_order(self, symbol: str, order_id: str) -> bool:
        endpoint = '/fapi/v1/order'
        params = {'symbol': self._get_exchange_symbol(symbol), 'orderId': order_id}
        response = self._delete_with_signature(endpoint, params)
        return order_id == response['orderId']

    def cancel_open_orders(self, symbol: str) -> bool:
        endpoint = '/fapi/v1/allOpenOrders'
        params = {'symbol': self._get_exchange_symbol(symbol)}
        response = self._delete_with_signature(endpoint, params)
        return 200 == int(response['code'])

    def get_position(self, symbol: str) -> Position:
        endpoint = '/fapi/v2/positionRisk'
        params = {'symbol': self._get_exchange_symbol(symbol)}
        response = self._get_with_signature(endpoint, params)
        position = Position.create_instance_for_binance(response[0], symbol)
        return position
