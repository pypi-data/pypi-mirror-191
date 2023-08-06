from finbright_futures.api.exchange.binance.future import Future
from finbright_futures.data_collector import DataProvider
import os

class BinanceFutures:
    def __init__(self, symbols: list[str], path: str) -> None:
        # pass
        ROOT_DIR = os.path.abspath(path)
        CANDLES_DIR = os.path.join(ROOT_DIR, 'data/candles/')
        self.data_provider = DataProvider(Future('', '', ignore_exceptions=False), CANDLES_DIR)
        self.symbols = symbols


    def get_historical_data(self):
        configs = [{
            "interval": 60,
            "limit": 1440,
            "thread": 1
        },{
            "interval": 3600,
            "limit": 48,
            "thread": 1
        },{
            "interval": 86400,
            "limit": 5,
            "thread": 1
        }]

        for config in configs:
            print("get history for: {}".format(config))
            self.data_provider.download_symbols_historical_candles(symbols=self.symbols, interval=config["interval"], limit=config["limit"],
                                                          max_threads=config["thread"])