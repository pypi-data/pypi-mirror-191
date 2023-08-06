from api.constant.account_type import AccountType
from api.exchange.binance.binance import Binance
from api.exchange.binance.request import Request
from api.interface.wallet import IWallet
from api.model.deposit_address import DepositAddress
from api.model.network_info import NetworkInfo


class Wallet(Binance, Request, IWallet):
    def __init__(self, api_key: str, api_secret_key: str, ignore_exceptions: bool = False):
        Request.__init__(self, base_url='https://api.binance.com', api_key=api_key,
                         api_secret_key=api_secret_key, ignore_exceptions=ignore_exceptions)
        Binance.__init__(self, name='Binance Wallet')

    def get_asset_networks_info(self, asset: str) -> list:
        endpoint = '/sapi/v1/capital/config/getall'
        response = self._get_with_signature(endpoint)
        asset_response = [item for item in response if asset == item['coin']][0]
        networks_info = [NetworkInfo.create_instance_for_binance(item, asset_response['name'])
                         for item in asset_response['networkList']]
        return networks_info

    def get_asset_deposit_address(self, asset: str, network: str) -> DepositAddress:
        endpoint = '/sapi/v1/capital/deposit/address'
        params = {'coin': asset, 'network': network}
        response = self._get_with_signature(endpoint, params)
        deposit_address = DepositAddress.create_instance_for_binance(response, network)
        return deposit_address

    def get_balance(self, asset: str) -> float:
        endpoint = '/api/v3/account'
        response = self._get_with_signature(endpoint)
        balance = float([item['free'] for item in response['balances']][0])
        return balance

    def post_withdraw_order(self, asset: str, network: str, address: str, amount: float, memo: str = None,
                            fee: float = None) -> str:
        endpoint = '/api/v3/account'
        params = {'coin': asset, 'network': network, 'address': address, 'amount': amount}
        if memo:
            params['addressTag'] = memo
        response = self._post_with_signature(endpoint, params)
        withdraw_id = response['id']
        return withdraw_id

    def post_transfer_order(self, asset: str, amount: str, from_account: AccountType, to_account: AccountType) -> str:
        from_account = self._get_exchange_account_type(from_account)
        to_account = self._get_exchange_account_type(to_account)

        if AccountType.SPOT == from_account and AccountType.FUTURE == to_account:
            return self.__post_transfer_order_between_spot_and_future(asset, amount, direction=True)
        if AccountType.FUTURE == from_account and AccountType.SPOT == to_account:
            return self.__post_transfer_order_between_spot_and_future(asset, amount, direction=False)

    def __post_transfer_order_between_spot_and_future(self, asset: str, amount: float, direction: bool):
        endpoint = '/sapi/v1/futures/transfer'
        params = {'asset': asset, 'amount': amount, 'type': '1' if direction else '2'}
        response = self._post_with_signature(endpoint, params)
        transfer_id = response['tranId']
        return transfer_id
