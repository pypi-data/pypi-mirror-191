from abc import ABC, abstractmethod

from finbright_futures.api.constant.interval import Interval


class IExchange(ABC):
    def __init__(self, name: str, maximum_requestable_candles: int):
        self.name = name
        self.maximum_requestable_candles = maximum_requestable_candles
        self._package_symbols_info_dictionary = None
        self._exchange_symbols_info_dictionary = None
        self._set_symbols_info_dictionary()

    @abstractmethod
    def get_symbols_info(self):
        raise NotImplemented()

    def _set_symbols_info_dictionary(self):
        symbols_info = self.get_symbols_info()
        self._package_symbols_info_dictionary = {item.symbol: item for item in symbols_info}
        self._exchange_symbols_info_dictionary = {item.exchange_symbol: item for item in symbols_info}

    def _get_exchange_symbol(self, package_symbol: str) -> str:
        return self._package_symbols_info_dictionary[package_symbol].exchange_symbol

    def _get_package_symbol(self, exchange_symbol: str) -> str:
        return self._exchange_symbols_info_dictionary[exchange_symbol].symbol

    @abstractmethod
    def _get_exchange_interval(self, package_interval: Interval) -> str:
        raise NotImplemented()

    @abstractmethod
    def _get_package_interval(self, exchange_interval: str) -> int:
        raise NotImplemented()

    @abstractmethod
    def _get_exchange_timestamp(self, package_timestamp: int) -> int:
        raise NotImplemented()

    def _round_price(self, symbol: str, price: float) -> float:
        return round(price, self._package_symbols_info_dictionary[symbol].price_precision)

    def _round_quantity(self, symbol: str, quantity: float) -> float:
        return round(quantity, self._package_symbols_info_dictionary[symbol].quantity_precision)

    def _round_lot(self, symbol: str, lot: int) -> float:
        return int(round(lot, self._package_symbols_info_dictionary[symbol].lot_precision))

    def _get_quantity(self, symbol: str, lot: int) -> float:
        return lot / 10 ** self._package_symbols_info_dictionary[symbol].quantity_precision

    def _get_lot(self, symbol: str, quantity: float) -> int:
        return quantity * 10 ** self._package_symbols_info_dictionary[symbol].quantity_precision

    @abstractmethod
    def _get_exchange_account_type(self, package_account_type: str) -> str:
        raise NotImplemented()

    @abstractmethod
    def _get_package_account_type(self, exchange_account_type: str) -> str:
        raise NotImplemented()
