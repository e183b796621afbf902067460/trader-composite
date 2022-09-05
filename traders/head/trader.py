from typing import List

from head.interfaces.trader.interface import ITraderComponent
from head.decorators.singleton import singleton
from head.decorators.yieldmethod import yieldmethod

from traders.cefi.composite.trader import cefiTrader
from traders.defi.composite.trader import defiTrader


@singleton
class HeadTrader(ITraderComponent):

    _traders: List[ITraderComponent] = list()
    _stablecoins: dict = {
        '0x57Ab1ec28D129707052df4dF418D58a2D46d5f51': {'symbol': 'sUSD', 'chain': 'eth'},
        '0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48': {'symbol': 'USDC', 'chain': 'eth'},
        '0x056Fd409E1d7A124BD7017459dFEa2F387b6d5Cd': {'symbol': 'GUSD', 'chain': 'eth'},
        '0xdAC17F958D2ee523a2206206994597C13D831ec7': {'symbol': 'USDT', 'chain': 'eth'},
        '0x6B175474E89094C44Da98b954EedeAC495271d0F': {'symbol': 'DAI', 'chain': 'eth'},
        '0x853d955aCEf822Db058eb8505911ED77F175b99e': {'symbol': 'FRAX', 'chain': 'eth'},
        '0x0000000000085d4780B73119b644AE5ecd22b376': {'symbol': 'TUSD', 'chain': 'eth'},
        '0x4Fabb145d64652a948d72533023f6E7A623C7C53': {'symbol': 'BUSD', 'chain': 'eth'},
        '0x956F47F50A910163D8BF957Cf5846D573E7f87CA': {'symbol': 'FEI', 'chain': 'eth'},
        '0x8E870D67F660D95d5be530380D0eC0bd388289E1': {'symbol': 'USDP', 'chain': 'eth'},
        '0x5f98805A4E8be255a32880FDeC7F6728C6568bA0': {'symbol': 'LUSD', 'chain': 'eth'},
        '0x049d68029688eAbF473097a2fC38ef61633A3C7A': {'symbol': 'fUSDT', 'chain': 'ftm'},
        '0x04068DA6C83AFCFA0e13ba15A6696662335D5B75': {'symbol': 'USDC', 'chain': 'ftm'},
        '0x82f0B8B456c1A451378467398982d4834b6829c1': {'symbol': 'MIM', 'chain': 'ftm'},
        '0x8D11eC38a3EB5E956B052f67Da8Bdc9bef8Abf3E': {'symbol': 'DAI', 'chain': 'ftm'}
    }
    _sames: dict = {
        'fUSDT': 'USDT'
    }

    def addTrader(self, trader) -> None:
        self._traders.append(trader)
        trader.setParent(parent=self)

    @yieldmethod
    def getPrice(self, major: str, vs: str = 'USD', *args, **kwargs) -> float:
        symbol = self._same(asset=major)
        for trader in self._traders:
            yield trader.getPrice(major=symbol, vs=vs, *args, **kwargs)

    def isStablecoin(self, address: str) -> bool:
        return address in self._stablecoins

    def _same(self, asset: str) -> str:
        return self._sames[asset] if asset in self._sames else asset


headTrader = HeadTrader()

headTrader.addTrader(trader=cefiTrader)
headTrader.addTrader(trader=defiTrader)
