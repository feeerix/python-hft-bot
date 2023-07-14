from enum import Enum

class ExchangeType(Enum):
    BINANCE = "binance"
    BYBIT = "bybit"
    PHEMEX = "phemex"


class Exchange:
    def __init__(self, exchange:ExchangeType):
        self.ExchangeType = exchange

    def __repr__(self) -> ExchangeType:
        return self.ExchangeType

    def __str__(self) -> str:
        return self.ExchangeType.name
    