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
    def __init__(self, symbol:str="", assets:List[Asset]=[], exchange:Exchange=None):
        """
        NOTE:
        Symbols in our sense can only have a pair
        """
        if len(assets) == 2:
            self.symbol = f"{assets[0].name}{assets[1].name}"
        else:
            raise ValueError("Asset List Length incorrect.")
        
        self.symbol = symbol
        self.assets = assets
        self.exchange = exchange

    def __str__(self) -> str:
        return self.symbol
    
