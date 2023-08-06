from abc import ABC, abstractmethod

from finbright_futures.api.constant.interval import Interval
from finbright_futures.api.constant.order_side import OrderSide
from finbright_futures.api.constant.time_in_force import TimeInForce
from finbright_futures.api.model.balance import Balance
from finbright_futures.api.model.buy_sell_ratio import BuySellRatio
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


class IFuture(ABC):
    def __init__(self, maximum_requestable_candles):
        self.maximum_requestable_candles = maximum_requestable_candles

    # Server
    @abstractmethod
    def get_server_time(self) -> int:
        pass

    @abstractmethod
    def get_ping(self) -> int:
        pass

    # data
    @abstractmethod
    def get_symbols(self) -> list:
        pass

    @abstractmethod
    def get_symbols_info(self) -> list:
        pass

    @abstractmethod
    def get_symbol_info(self, symbol: str) -> SymbolInfo:
        pass

    @abstractmethod
    def get_daily_ticker_price_change(self, symbol: str) -> DailyTickerPriceChange:
        pass

    @abstractmethod
    def get_order_books_ticker(self) -> list:
        pass

    @abstractmethod
    def get_order_book_ticker(self, symbol: str) -> OrderBookTicker:
        pass

    @abstractmethod
    def get_order_book(self, symbol: str) -> OrderBook:
        pass

    @abstractmethod
    def get_price_ticker(self, symbol: str) -> PriceTicker:
        pass

    @abstractmethod
    def get_candles(self, symbol: str, interval: Interval) -> list:
        pass

    @abstractmethod
    def get_historical_candles(self, symbol: str, interval: Interval, from_timestamp: int = None,
                               to_timestamp: int = None, limit: int = None) -> list:
        pass

    @abstractmethod
    def get_open_interest(self, symbol: str) -> OpenInterest:
        pass

    @abstractmethod
    def get_open_interests(self, symbol: str, interval: Interval) -> [OpenInterestStatistic]:
        pass

    @abstractmethod
    def get_historical_open_interests(self, symbol: str, interval: Interval, from_timestamp: int = None,
                                      to_timestamp: int = None, limit: int = None) -> [OpenInterestStatistic]:
        pass

    @abstractmethod
    def get_top_accounts_long_short_ratios(self, symbol: str, interval: Interval) -> [LongShortRatio]:
        pass

    @abstractmethod
    def get_historical_top_accounts_long_short_ratios(self, symbol: str, interval: Interval, from_timestamp: int = None,
                                                      to_timestamp: int = None, limit: int = None) -> [LongShortRatio]:
        pass

    @abstractmethod
    def get_top_positions_long_short_ratios(self, symbol: str, interval: Interval) -> [LongShortRatio]:
        pass

    @abstractmethod
    def get_historical_top_positions_long_short_ratios(self, symbol: str, interval: Interval,
                                                       from_timestamp: int = None, to_timestamp: int = None,
                                                       limit: int = None) -> [LongShortRatio]:
        pass

    @abstractmethod
    def get_long_short_ratios(self, symbol: str, interval: Interval) -> [LongShortRatio]:
        pass

    @abstractmethod
    def get_historical_long_short_ratios(self, symbol: str, interval: Interval, from_timestamp: int = None,
                                         to_timestamp: int = None, limit: int = None) -> [LongShortRatio]:
        pass

    @abstractmethod
    def get_takers_buy_sell_ratios(self, symbol: str, interval: Interval) -> [BuySellRatio]:
        pass

    @abstractmethod
    def get_historical_takers_buy_sell_ratios(self, symbol: str, interval: Interval, from_timestamp: int = None,
                                              to_timestamp: int = None, limit: int = None) -> [BuySellRatio]:
        pass

    # Account
    @abstractmethod
    def get_balance(self, asset: str = 'USDT') -> Balance:
        pass

    # Trade
    @abstractmethod
    def get_leverage(self, symbol: str) -> int:
        pass

    @abstractmethod
    def set_leverage(self, symbol: str, leverage: int) -> bool:
        pass

    @abstractmethod
    def post_limit_order(self, symbol: str, side: OrderSide, quantity: float, price: float,
                         time_in_force: TimeInForce = None) -> str:
        pass

    @abstractmethod
    def post_market_order(self, symbol: str, side: OrderSide, quantity: float) -> str:
        pass

    @abstractmethod
    def post_stop_market_order(self, symbol: str, side: OrderSide, quantity: float, stop_price: float) -> str:
        pass

    @abstractmethod
    def get_order(self, symbol: str, order_id: str) -> Order:
        pass

    @abstractmethod
    def get_open_orders(self, symbol: str) -> list:
        pass

    @abstractmethod
    def cancel_order(self, symbol: str, order_id: str) -> bool:
        pass

    @abstractmethod
    def cancel_open_orders(self, symbol: str) -> bool:
        pass

    @abstractmethod
    def get_position(self, symbol: str) -> Position:
        pass
