from enum import Enum

class ExchangeType(Enum):
    BINANCE = "binance"
    BYBIT = "bybit"
    PHEMEX = "phemex"


class Exchange:
    def __init__(self, exchange:ExchangeType):
        self.exchange_type = exchange

    def __repr__(self) -> str:
        return self.exchange_type

    def __str__(self) -> str:
        return self.exchange_type.name
    