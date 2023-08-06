from api.constant.account_type import AccountType
from api.interface.wallet import IWallet


def wallet_samples(api: IWallet, asset: str, network: str, address: str, amount: str):
    # get asset networks info
    print('get asset networks info:')
    networks_info = api.get_asset_networks_info(asset)
    print([(network_info.network_name, network_info.network) for network_info in networks_info])

    # get deposit address
    print('\nget deposit address:')
    deposit_address = api.get_asset_deposit_address(asset, network)
    print(deposit_address.asset, deposit_address.network, deposit_address.address, deposit_address.memo)

    # get deposit address
    print('\nget balance:')
    balance = api.get_balance(asset)
    print(balance)

    # post withdraw order
    print('\npost withdraw order:')
    # withdraw_id = api.post_withdraw_order(asset, network, address, amount)
    # print(withdraw_id)

    # post transfer order
    print('\npost transfer order:')
    transfer_id = api.post_transfer_order(asset, amount, from_account=AccountType.WALLET, to_account=AccountType.FUTURE)
    print(transfer_id)
