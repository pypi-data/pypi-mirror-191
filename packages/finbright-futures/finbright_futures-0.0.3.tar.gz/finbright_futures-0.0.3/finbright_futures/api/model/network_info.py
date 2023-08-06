class NetworkInfo:
    def __init__(self):
        self.asset = None
        self.asset_name = None
        self.network = None
        self.network_name = None
        self.can_deposit = None
        self.can_withdraw = None
        self.min_withdraw = None
        self.max_withdraw = None
        self.min_withdraw_fee = None
        self.max_withdraw_fee = None
        self.need_memo = None
        self.main_network = None
        self.tips = None

    @staticmethod
    def create_instance_for_binance(data, asset_name):
        instance = NetworkInfo()

        instance.asset = data['coin']
        instance.asset_name = asset_name
        instance.network = data['network']
        instance.network_name = data['name']
        instance.can_deposit = data['depositEnable']
        instance.can_withdraw = data['withdrawEnable']
        instance.min_withdraw = float(data['withdrawMin'])
        instance.max_withdraw = float(data['withdrawMax'])
        instance.min_withdraw_fee = float(data['withdrawFee'])
        instance.need_memo = data['sameAddress']
        instance.main_network = data['isDefault']
        instance.tips = data['specialTips']

        return instance
