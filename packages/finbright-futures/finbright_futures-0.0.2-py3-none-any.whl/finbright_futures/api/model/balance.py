class Balance:
    def __init__(self):
        self.total = None
        self.available = None

    def __add__(self, other):
        instance = Balance()

        instance.total = self.total + other.total
        instance.available = self.available + other.available

        return instance

    @staticmethod
    def create_instance_for_binance(data):
        instance = Balance()

        instance.total = float(data['balance'])
        instance.available = float(data['availableBalance'])

        return instance
