from abc import ABC

from api.constant.account_type import AccountType
from api.constant.interval import Interval
from api.interface.exchange import IExchange


class Binance(IExchange, ABC):
    def __init__(self, name: str, maximum_requestable_candles: int):
        super().__init__(name, maximum_requestable_candles)

    def get_symbols_info(self):
        pass

    def _get_exchange_interval(self, package_interval: Interval) -> str:
        minute = int(package_interval / 60)
        if minute < 60:
            return "{}m".format(minute)

        hour = int(minute / 60)
        if hour < 24:
            return "{}h".format(hour)

        day = int(hour / 24)
        if day < 7:
            return "{}d".format(day)

        week = int(day / 7)
        if week < 4:
            return "{}w".format(week)

        return "1M"

    def _get_package_interval(self, exchange_interval: str) -> int:
        raise NotImplemented()

    def _get_exchange_timestamp(self, package_timestamp: int) -> int:
        return package_timestamp * 1000

    def _get_exchange_account_type(self, package_account_type: str) -> str:
        if AccountType.WALLET == package_account_type or AccountType.SPOT == package_account_type:
            return AccountType.SPOT
        else:
            return package_account_type

    def _get_package_account_type(self, exchange_account_type: str) -> str:
        raise NotImplemented()
