import math
import os
import time
from datetime import datetime
from threading import Thread, active_count

from rich.progress import Progress
from tqdm.auto import tqdm

from finbright_futures.api.constant.interval import Interval
from finbright_futures.api.model.candle import Candle

class DataProvider:
    def __init__(self, api, candles_dir):
        self.__api = api
        self.candles_dir= candles_dir

    @staticmethod
    def __check_candles_correctness(candles: list[Candle], interval: Interval):
        for index in range(len(candles) - 1):
            if candles[index].timestamp + interval != candles[index + 1].timestamp:
                print(index, index + 1, candles[index].datetime, candles[index + 1].datetime)
                raise Exception("Data has redundant or missing values.")

    @staticmethod
    def __create_directory(path: str) -> bool:
        tokens = path.split('/')[:-1]
        parents = ['/'.join(tokens[:index + 1]) for index in range(1, len(tokens))]
        for parent_dir in parents:
            if not os.path.exists(parent_dir):
                os.mkdir(parent_dir)

    def __get_local_candles_file_path(self, symbol: str, interval: Interval) -> str:
        return os.path.join(self.candles_dir, symbol, Interval.get_str(interval))

    def __write_local_candles(self, candles: list, symbol: str, interval: Interval):
        path = self.__get_local_candles_file_path(symbol, interval)
        self.__create_directory(path)
        lines = ["timestamp,open,high,low,close,volume,trades\n"]
        lines.extend([','.join([str(item) for item in candle.get_array()]) + '\n' for candle in candles])
        file = open(path, 'w')
        file.writelines(lines)

    def __read_local_candles(self, symbol: str, interval: Interval):
        path = self.__get_local_candles_file_path(symbol, interval)
        if os.path.exists(path):
            file = open(path, 'r')
            lines = file.readlines()
            if 1 < len(lines):
                return [Candle.create_instance_with_array(row.replace('\n', '').split(',')) for row in lines[1:]]

        return []

    def __get_candles(self, symbol: str, interval: Interval, start_timestamp: int, end_timestamp, progress, show_tqdm):
        candles = []
        requested_candles = 0
        candles_count = (end_timestamp - start_timestamp) / interval
        requests_count = math.ceil(candles_count / self.__api.maximum_requestable_candles)

        bar = list(range(requests_count))
        if progress:
            task = progress.add_task("[green]{}".format(symbol), total=len(bar)) if progress else None
        elif show_tqdm:
            bar = tqdm(bar)

        for index in bar:
            request_limit = self.__api.maximum_requestable_candles
            if candles_count - requested_candles < self.__api.maximum_requestable_candles:
                request_limit = int(candles_count - requested_candles)
            request_start_timestamp = start_timestamp + requested_candles * interval
            request_end_timestamp = request_start_timestamp + request_limit * interval
            request_new_candles = self.__api.get_historical_candles(symbol, interval, request_start_timestamp,
                                                                    request_end_timestamp, request_limit)

            if 0 < len(request_new_candles) and request_end_timestamp == request_new_candles[-1].timestamp:
                request_new_candles = request_new_candles[:-1]

            candles.extend(request_new_candles)
            requested_candles += request_limit

            if progress:
                progress.update(task, advance=1)

            if show_tqdm:
                status = "requested candles: {}, downloaded candles: {}".format(requested_candles, len(candles))
                bar.set_postfix_str(status)
                bar.refresh()

        return candles

    def download_historical_candles(self, symbol: str, interval: Interval, limit: int = None, progress=None,
                                    show_tqdm=False, update_time: int = 24 * 60 * 60) -> list:
        candles = self.__read_local_candles(symbol, interval)

        timestamp = math.floor(datetime.now().timestamp() / interval) * interval
        if 0 < len(candles) and update_time < datetime.now().timestamp() - candles[-1].timestamp:
            start_timestamp = candles[-1].timestamp + interval
            new_candles = self.__get_candles(symbol, interval, start_timestamp, timestamp, progress, show_tqdm)
            candles.extend(new_candles)
            self.__check_candles_correctness(candles, interval)
            self.__write_local_candles(candles, symbol, interval)

        if limit is not None:
            # local candles count are zero
            if 0 == len(candles):
                start_timestamp = timestamp - limit * interval
                new_candles = self.__get_candles(symbol, interval, start_timestamp, timestamp, progress, show_tqdm)
                candles = new_candles + candles
                self.__check_candles_correctness(candles, interval)
                self.__write_local_candles(candles, symbol, interval)

            # limit is greater than local candles count
            elif len(candles) < limit:
                new_limit = limit - len(candles)
                end_timestamp = candles[0].timestamp
                start_timestamp = end_timestamp - new_limit * interval
                new_candles = self.__get_candles(symbol, interval, start_timestamp, end_timestamp, progress, show_tqdm)
                candles = new_candles + candles
                self.__check_candles_correctness(candles, interval)
                self.__write_local_candles(candles, symbol, interval)

        return candles[-limit:]

    def download_symbols_historical_candles(self, symbols: list[str], interval: Interval, limit: int, max_threads: int):
        with Progress() as progress:
            symbol_index = 0
            while symbol_index < len(symbols):
                while active_count() < max_threads + 2 and symbol_index < len(symbols):
                    symbol = symbols[symbol_index]
                    symbol_index += 1
                    thread = Thread(target=self.download_historical_candles, args=(symbol, interval, limit, progress))
                    thread.start()

                time.sleep(1)

    def download_all_symbols_historical_candles(self, interval: Interval, limit: int):
        for symbol in tqdm(self.__api.get_symbols()):
            self.download_historical_candles(symbol, interval, limit, show_tqdm=False)
