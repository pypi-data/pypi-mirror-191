from api.constant.interval import Interval
from api.exchange.binance.future import Future
from api.exchange.binance.wallet import Wallet
from api.sample.future import future_samples
from api.sample.wallet import wallet_samples

api_key = ''
api_secret_key = ''

# futures samples
future_api = Future(api_key, api_secret_key)
future_samples(future_api, 'BTC-USDT', Interval.MIN5, quantity=0.00101, price=10000, stop_price=50000)

# wallet samples
wallet_api = Wallet(api_key, api_secret_key)
wallet_samples(wallet_api, "TRX", 'TRC20', '', 100)
