from enum import Enum

class FeeType(Enum):
    MAKER = 'maker'
    TAKER = 'taker'
    FUNDING = 'funding'

class PositionType(Enum):
    LONG = 'long'
    SHORT = 'short'
    ARB = 'arbitrage'
    OPTION = 'option'

    @classmethod
    def from_string(cls, position_str: str):
        # Prepend underscore for our internal representation
        if position_str in cls._member_names_:
            return cls[position_str]
        else:
            raise ValueError(f"No position type found for '{position_str}'")

class OptionType(Enum):
    AMERICAN = 'american'
    EUROPEAN = 'european'
    ASIAN = 'asian'
    BARRIER = 'barrier'
    BINARY = 'binary'
    EXOTIC = 'exotic'

class Fee:
    def __init__(self, fee_type:FeeType, amount:float, timestamp_ms:float=0):
        self.fee_type = fee_type
        self.amount = amount
        self.timestamp = timestamp_ms

class Trade:
    def __init__(self, amount:float, entry:float, fee:Fee):
        self.amount = amount
        self.entry = entry
        self.fee = fee.amount

class OptionTrade(Trade):
    def __init__(self, amount: float, entry: float, fee:Fee, strike_price: float, expiry:int, option_type: OptionType):
        super().__init__(amount, entry)
        self.strike_price = strike_price
        self.expiry = expiry
        self.option_type = option_type
        self.fee = fee.amount

class Position:
    def __init__(self, position_type:PositionType, trades:list):
        self.position_type = position_type
        self.trades = trades
    