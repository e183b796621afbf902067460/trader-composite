import requests
from typing import Optional

from head.interfaces.trader.interface import ITraderComponent


class CoingeckoTrader(ITraderComponent):
    _endpoint = "https://api.coingecko.com/api/v3/simple/price?ids={}&vs_currencies={}"

    _markets: dict = {
        'USDT': 'tether',
        'WETH': 'weth',
        'WBNB': 'wbnb',
        'WBTC': 'wrapped-bitcoin',
        'amWETH': 'aave-polygon-weth',
        'amWBTC': 'aave-polygon-wbtc',
        'gDAI': 'geist-dai',
        'gUSDC': 'geist-usdc',
        'gfUSDT': 'geist-fusdt'
    }

    @classmethod
    def getPrice(self, major: str, vs: str, *args, **kwargs) -> Optional[float]:
        vs = 'usd' if vs == 'USD' else vs
        try:
            market = self._markets[major]
            return requests.get(url=self._endpoint.format(market, vs)).json()[market][vs]
        except KeyError:
            return None