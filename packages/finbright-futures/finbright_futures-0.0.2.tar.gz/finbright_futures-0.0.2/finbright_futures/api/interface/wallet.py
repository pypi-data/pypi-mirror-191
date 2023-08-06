from abc import ABC, abstractmethod

from api.constant.account_type import AccountType
from api.model.deposit_address import DepositAddress


class IWallet(ABC):
    @abstractmethod
    def get_asset_networks_info(self, asset: str) -> list:
        pass

    @abstractmethod
    def get_asset_deposit_address(self, asset: str, network: str) -> DepositAddress:
        pass

    @abstractmethod
    def get_balance(self, asset: str) -> float:
        pass

    @abstractmethod
    def post_withdraw_order(self, asset: str, network: str, address: str, amount: float, memo: str = None,
                            fee: float = None) -> str:
        pass

    @abstractmethod
    def post_transfer_order(self, asset: str, amount: str, from_account: AccountType, to_account: AccountType) -> str:
        pass
