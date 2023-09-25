# IMPORTS

# LOCAL IMPORTS
from lib.tools.asset import Asset
from lib.tools.exchange import Exchange
from lib.tools.interval import Interval
from lib.tools.symbol import Symbol

from backtest.strat.strategy import Strategy
from backtest.strat.indicator import Indicator
from backtest.strat.settings.settings import Settings
from backtest.portfolio import Portfolio
from backtest.strat.signal import Signal

class StrategyFactory(Strategy):
    def __init__(self):
        pass