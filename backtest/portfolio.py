from typing import List

# LOCAL IMPORTS
from lib.tools.asset import Asset
from backtest.strat.strategy import Strategy

class Portfolio:
    """
    A portfolio is a list of assets that we might hold or even positions that we're holding
    that we're hoping will be more valuable over time. This can include longs, shorts, LPs and
    other potential kinds of assets we have not considered yet.

    We can then apply a strategy, noting to it, the strategy can either aim for a 
    'optimal' portfolio based on specific risk factors of your choosing, or it can
    call the trades that you want to make to maximise the value of the portfolio according
    to your own specifications.

    It is designed to be as open and modular as possible so that as long as you've set up your
    Databases correctly, and the corresponding signals it should be able to try and compute
    the results for a particular strategy.
    """

    def __init__(self, asset_universe:List[Asset]=[], strategy:Strategy=None):
        pass

    