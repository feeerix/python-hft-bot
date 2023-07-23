# IMPORT
from enum import Enum

# LOCAL IMPORT
from lib.tools.network import Network
# from lib.tools.exchange import ExchangeType

"""
At this stage, we specifically will want to define all of the assets
that we might trade in our universe.
First we must get all the assets that we might want to trade first.
We start by creating an Enum that's defined by their ticker.
"""
class AssetType(Enum):
    COIN = 'coin'
    TOKEN = 'token'
    STABLE = 'stable'
    NFT = 'nft'

assets = ["ETH", "WETH", "BTC", "WBTC"]

class Asset:
    def __init__(
            self, 
            name:str="",
            ticker:str="", 
            address:str="", 
            asset_type:AssetType=None,
            network:Network=None,
            # exchange: ExchangeType=None
            ):
        self.ticker = ticker
        self.asset = asset_type
        self.name = name
        self.address = address
        self.network = network
        # self.exchange = exchange

    def __repr__(self):
        return f"Asset(name={self.name}, ticker-{self.ticker}, network={self.network})"
    
    def __str__(self):
        return f"{self.ticker}"
    
    """
    We now must create different functions as the assets can behave different depending on the venue it's being traded
    """

