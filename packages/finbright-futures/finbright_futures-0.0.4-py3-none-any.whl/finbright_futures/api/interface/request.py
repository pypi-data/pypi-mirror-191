import json
from abc import ABC, abstractmethod
from urllib import parse

import requests


class IRequest(ABC):
    def __init__(self, base_url: str, ignore_exceptions: bool):
        self.__base_url = base_url
        self.__ignore_exceptions = ignore_exceptions

    @abstractmethod
    def _check_response(self, response):
        pass

    @abstractmethod
    def _before_request(self, method: str, endpoint: str, params):
        pass

    def _after_request(self, response):
        self._check_response(response)
        return json.loads(response.text)

    def _request(self, method: str, endpoint: str, params: dict, sign: bool):
        try:
            if params is None:
                params = {}
            (headers, params, body) = self._before_request(method, endpoint, params) if sign else ({}, params, '')
            url = parse.urljoin(self.__base_url, endpoint)
            response = requests.request(method=method, url=url, headers=headers, params=params, data=body)
            return self._after_request(response)
        except Exception as e:
            if self.__ignore_exceptions:
                print(e)
            else:
                raise e

    def _get(self, endpoint: str, params: dict = None):
        return self._request(method='GET', endpoint=endpoint, params=params, sign=False)

    def _get_with_signature(self, endpoint: str, params: dict = None):
        return self._request(method='GET', endpoint=endpoint, params=params, sign=True)

    def _post_with_signature(self, endpoint: str, params: dict = None):
        return self._request(method='POST', endpoint=endpoint, params=params, sign=True)

    def _delete_with_signature(self, endpoint: str, params: dict = None):
        return self._request(method='DELETE', endpoint=endpoint, params=params, sign=True)
