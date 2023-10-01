# Import
from enum import Enum
from dataclasses import dataclass
from typing import List

# Local Import
from lib.tools.asset import Asset

class EntryStyle(Enum):
    CLOSE = "close" # opens position with close of last candle
    MARKET = "market" # YOLO's and just market buys at whatever price it is now
    TWAP = "twap" # enters at twap

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
        if position_str.upper() in cls._member_names_:
            return cls[position_str.upper()]
        else:
            raise ValueError(f"No position type found for '{position_str}'")

class TradeType(Enum):
    LIMIT = 'limit'
    MARKET = 'market'
    STOPLIMIT = 'stoplimit'
    STOPMARKET = 'stopmarket'
    TRAILING = 'trailing'

class OptionType(Enum):
    AMERICAN = 'american'
    EUROPEAN = 'european'
    ASIAN = 'asian'
    BARRIER = 'barrier'
    BINARY = 'binary'
    EXOTIC = 'exotic'

@dataclass
class Fee:
    # def __init__(self, fee_type:FeeType, amount:float, timestamp_ms:float=0):
    fee_type: FeeType
    amount: float
    timestamp: float

@dataclass
class EntryArgs:
    quote: Asset = None # Quote Asset (ETH in ETHUSD)
    base: Asset = None # Base Asset (USD in ETHUSD)
    expected_amount: float = 0.0 # Amount of Quote asset being bought or sold 
    expected_size: float = 0.0 # Total Size which accounts for leverage
    entry_price: EntryStyle = None # EntryStyle - used to calculate requested entry
    # entry_execute_price: float = 0.0 # Executed price
    # init_timestamp: float = 0.0 # Time calulcated
    # execute_timestamp: float = 0.0 # Time initially executed
    # fill_timestamp: float = 0.0 # Time completed filled
    trade_type: TradeType = None # TradeType
    pos_family: PositionType = None # Position Types

    def __post_init__(self):
        """
        The post init to get the cumulative fee based on the fee_pct
        """
        # Add to cumulative Fee
        # self.total_fee += self.size * (self.fee_pct / 100)

        # Set the size based on quote amount in base asset
        # self.size += self.amount * self.entry_price
        """
        Just to note, this would mean that the size for ETHUSDC at 1800 for 1.5 ETH
        would mean that the size is:
        size = 1.5 * 1800 = 2700 (Note this is in USDC terms)
        """

    def __str__(self) -> str:
        return f"{self.quote}{self.base} | {self.trade_type} | {self.pos_family}"


class Trade:
    """
    Trades are going to be the building blocks that make up a Position.
    We will also need to define the defaults and placeholder values that the 
    Trades will have, so that they can have certain properties and be dynamically
    adjusted and closed.
    """

    fee_mapping = {
        TradeType.LIMIT: FeeType.MAKER,
        TradeType.MARKET: FeeType.TAKER,
        TradeType.STOPLIMIT: FeeType.MAKER,
        TradeType.STOPMARKET: FeeType.TAKER
    }

    def __init__(
            self, 
            entry_args: EntryArgs
            # amount:float,
            # entry:float, 
            # trade_type:TradeType, 
            # fee:Fee
        ):
        self.entry_args = entry_args

    @staticmethod
    def create(entry_args:EntryArgs):
        """
        This method returns a Trade class
        """
        
        return Trade(entry_args)
    
    def execute(execute_price:float):
        pass

    def close(self, close_type:FeeType, amount:float, timestampe_ms:float=0):
        pass


"""
TODO - To update haven't implemented Options yet
"""
class OptionTrade(Trade):
    def __init__(self, amount: float, entry: float, fee:Fee, strike_price: float, expiry:int, option_type: OptionType):
        super().__init__(amount, entry)
        self.strike_price = strike_price
        self.expiry = expiry
        self.option_type = option_type
        self.fee = fee.amount

@dataclass
class PositionArgs:
    parent_trade: List[Trade]
    take_profit: List[Trade]
    stop_loss: List[Trade]

class Position:
    """
    A Position is created whenever the conditions have been met to do take on some risk.
    It should be noted that the trades are in lists as we can DCA into a position or 
    we can spread out our take profits or stop losses for example.

    This way we can dynamically call our take profits and stop losses when we want to 
    after the position has been created, for example.
    """

    position_mapping = {
        PositionType.LONG: None,
        PositionType.SHORT: None,
        PositionType.ARB: None,
        PositionType.OPTION: None
    }
    def __init__(self, position_type:PositionType, trades:List[Trade]):
        self.position_type = position_type
        self.trades = trades
    
    @staticmethod
    def create(position_type:PositionType, position_arguments:PositionArgs):
        """
        We should be able to create a list of trades (either to be made or otherwise)
        based on the position arguments, as opposed to manually creating a trade 
        manually, although let's allow that possibility
        """
        print(position_type)
        # Create the base trade
        print(position_arguments)
        

        # Trade.create({
        #     "amount": pos_logic.settings.arguments['size'],
        #     "entry": None,
        #     "trade_type": pos_logic.settings.arguments['trade_type'],
        #     "pos_type": pos_logic.settings.func_name,
        #     "fee_pct": 0.1,
        #     "timestamp": 0
        # })

        print("CREATE POSITION EXIT")
        exit()

"""
TODO
CREATE A POSITION FACTORY

When we have a specific position we want to execute, we will have a parent trade
that is the primary thing that's taking on risk for example. For example, if you have
a trade to 1ETH from 1500 USD, that would be a trade that is "long" ETH.

You might then have a take profit that sells ETH to USD for 2000 USD and a stop loss
that sells ETH to USD at a loss for 1000 USD.

These are considered children of the primary trade, and will have a set of initial properties,
that is as they have not been executed yet, and they are looking for the specific
conditions to be executed.

We should also embed logic blocks in them

"""

class PositionFactory:
    """
    This is a factory to create the positions
    """
    @staticmethod
    def create_position(
        entry_args:EntryArgs # Entry Arguments
    ):
        pass


"""
We create a set of pre-determined logic building blocks that we
can place in testing section.

This means we can check for specific conditions such as:
- If we already have a position (the easiest condition)
- If we already have an amount of risk on (if we're DCAing for example)

"""
class Conditions(Enum):
    pass