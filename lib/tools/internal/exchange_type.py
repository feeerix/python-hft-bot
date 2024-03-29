# IMPORTS
from enum import Enum

class ExchangeType(Enum):
    BINANCE = "binance"
    BYBIT = "bybit"
    PHEMEX = "phemex"

    def __str__(self): 
        return self.value