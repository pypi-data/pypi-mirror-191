from abc import ABC, abstractmethod

from api.constant.interval import Interval
from api.constant.order_side import OrderSide
from api.constant.time_in_force import TimeInForce
from api.model.order_book import OrderBook
from api.model.order_book_ticker import OrderBookTicker
from api.model.price_ticker import PriceTicker
from api.model.symbol_info import SymbolInfo


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

    # Account
    @abstractmethod
    def get_balance(self, asset: str = 'USDT') -> float:
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

    # Trade
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
    def get_order(self, symbol: str, order_id: int):
        pass

    @abstractmethod
    def get_open_orders(self, symbol: str) -> list:
        pass

    @abstractmethod
    def cancel_order(self, symbol: str, order_id: int) -> bool:
        pass

    @abstractmethod
    def cancel_open_orders(self, symbol: str) -> bool:
        pass
