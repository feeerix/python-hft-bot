# IMPORTS
from enum import Enum
from typing import List

# LOCAL IMPORTS
from lib.tools.asset import Asset
from lib.tools.exchange import Exchange

"""
Symbol class
"""

class Symbol:
    def __init__(self, symbol:str, assets:List[Asset]=[], exchange:Exchange=None):
        self.symbol = symbol
        self.assets = assets
        self.exchange = exchange

    def __str__(self) -> str:
        return self.symbol