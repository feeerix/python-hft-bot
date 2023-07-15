# IMPORT


# LOCAL IMPORT
from lib.tools.network import Network, NetworkType
from lib.tools.asset import Asset


class Blockchain:
    def __init__(self, name:str, network: Network, native_token:Asset, network_type:NetworkType):
        self.name = name
        self.network = network
        self.network_type = network_type
        self.native_token = native_token
