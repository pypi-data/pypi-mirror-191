import argparse

from rich.progress import Progress

from api.exchange.binance.future import Future
from data_collector import DataProvider

if '__main__' == __name__:
    parser = argparse.ArgumentParser()
    parser.add_argument('--method', action='store', type=int, required=True)
    parser.add_argument('--symbol', action='store', type=str, required=False)
    parser.add_argument('--interval', action='store', type=int, required=True)
    parser.add_argument('--limit', action='store', type=int, required=True)
    parser.add_argument('--threads', action='store', type=int, required=False)
    args = parser.parse_args()

    # (ATTENTION) for debug purposes set ignore_exceptions to True
    api = Future('', '', ignore_exceptions=False)
    data_provider = DataProvider(api)

    if 0 == args.method:
        with Progress() as progress:
            data_provider.download_historical_candles(symbol=args.symbol, interval=args.interval, limit=args.limit,
                                                      progress=progress)

    if 1 == args.method:
        with open('symbols.csv', 'r') as file:
            symbols = [symbol.replace('\n', '') for symbol in file.readlines()[1:]]
        data_provider.download_symbols_historical_candles(symbols=symbols, interval=args.interval, limit=args.limit,
                                                          max_threads=args.threads)

    if 2 == args.method:
        data_provider.download_all_symbols_historical_candles(interval=args.interval, limit=args.limit)
