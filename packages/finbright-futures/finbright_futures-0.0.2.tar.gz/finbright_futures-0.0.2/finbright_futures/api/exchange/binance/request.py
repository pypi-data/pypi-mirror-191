import hashlib
import hmac
import json
from abc import ABC
from datetime import datetime
from urllib import parse

from api.interface.request import IRequest


class Request(IRequest, ABC):
    def __init__(self, base_url: str, api_key: str, api_secret_key: str, ignore_exceptions: bool,
                 receive_window_milliseconds: int = 10000):
        super().__init__(base_url, ignore_exceptions)
        self.__api_key = api_key
        self.__api_secret_key = api_secret_key
        self.__receive_window_milliseconds = receive_window_milliseconds

    def _check_response(self, response):
        if 400 == response.status_code:
            response_map = json.loads(response.text)
            message = "Binance API Error(Code: {}, Message: {})".format(response_map["code"], response_map["msg"])
            raise Exception(message)
        elif 200 != response.status_code:
            raise Exception(response.text)

    def _before_request(self, method: str, endpoint: str, params):
        headers = {"X-MBX-APIKEY": self.__api_key}

        timestamp = int(datetime.now().timestamp() * 1000 - 1000)
        params["recvWindow"] = self.__receive_window_milliseconds
        params["timestamp"] = timestamp
        str_to_sign = parse.urlencode(params)
        params["signature"] = hmac.new(self.__api_secret_key.encode(), msg=str_to_sign.encode(),
                                       digestmod=hashlib.sha256).hexdigest()

        return headers, params, ''
