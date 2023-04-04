# Imports
import pandas as pd
from time import time
from datetime import datetime
from dateutil.relativedelta import relativedelta

# Local Imports
from lib.api.binance.local import filename

class database:
    def __init__(self):
        self.df = None

    def kline_df(self, symbol:str, interval:str, starttime:int, endtime:int) -> pd.DataFrame:
        # Filepath based on inputs
        filepath = f"db/klines/{symbol.lower()}/{interval}/"

        # Start and endtime
        dt_start = datetime.fromtimestamp(starttime)
        dt_end = datetime.fromtimestamp(endtime)
        
        # return file
        ret_data = pd.DataFrame(columns=[
            'time',
            'open',
            'high',
            'low',
            'close',
            'volume',
            'close_time',
            'quote_volume',
            'trade_number',
            'taker_buy_volume',
            'taker_quote_volume',
            'na'
        ])

        
        
        # build loop
        while dt_start < dt_end:
            
            # Get filename
            fn = filename(symbol, interval, f"{dt_start.year}", f"{dt_start.month:02d}")
            
            # add new data to return df
            ret_data = pd.concat([ret_data, pd.read_csv(f'{filepath}{fn}')])

            # Go to next month
            dt_start += relativedelta(months=1)

        self.df = ret_data
        # Return data
        return ret_data
    