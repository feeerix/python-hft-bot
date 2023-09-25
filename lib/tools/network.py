# IMPORT
from enum import Enum

# LOCAL IMPORT


class NetworkType(Enum):
    EVM = 'evm'
    UTXO = 'utxo'

class Network(Enum):
    BITCOIN = 'bitcoin'
    ETHEREUM = 'ethereum'
    ARBITRUM = 'arbitrum'
    OPTIMISM = 'optimism'
    POLYGON = 'polygon'
    BSC = 'bsc'
    ZKSYNCERA = 'zk sync era'
    GOERLI = 'goerli'
    AVALANCHEC = 'avalanche c-chain'
    GNOSIS = 'gnosis'

