# LOCAL IMPORTS
from backtest.strat.strat import strategy
from lib.cli.listener import *
from lib.cli.printer import *

class Creator:
    """
    This is the creator class. We'll use this class to create strategies.
    """
    def __init__(self, _strategy:strategy) -> None:
        self.strategy = strategy


    def check_strategy(self):
        """
        First we check that we have the conditions to open and subsequenlty close positions.
        """
        pass