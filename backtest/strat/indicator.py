# Imports
import pandas as pd
import pandas_ta as ta


class indicator:
    def __init__(self, indicator_type:ta, settings:dict):
        self.indicator_type = indicator_type
        self.settings = settings