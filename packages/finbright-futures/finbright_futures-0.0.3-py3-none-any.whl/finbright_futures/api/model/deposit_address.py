class DepositAddress:
    def __init__(self):
        self.asset = None
        self.network = None
        self.address = None
        self.memo = None

    @staticmethod
    def create_instance_for_binance(data, network):
        instance = DepositAddress()

        instance.asset = data['coin']
        instance.network = network
        instance.address = data['address']
        instance.memo = data['tag']

        return instance
