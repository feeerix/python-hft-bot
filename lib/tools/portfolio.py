# IMPORTS
from typing import Dict

# lOCAL IMPORTS
from lib.tools.asset import Asset

class Portfolio:
    def __init__(self, name:str, assets:Dict[Asset, float]):
        self.name = name
        self.assets = assets

    def add_asset(self, asset: Asset, balance: float):
        self.assets[asset] = balance