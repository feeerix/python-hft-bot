# LOCAL IMPORTS
from backtest.strat.strat import strategy
from lib.cli.listener import *
from lib.cli.printer import *

class Creator:
    def __init__(self, empty_strategy:strategy) -> None:
        self.strategy = empty_strategy

    def indicator_loop(self):
        pass

    def entry_loop(self):
        pass

    def close_loop(self):
        pass

    