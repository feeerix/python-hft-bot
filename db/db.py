# Imports
import pandas as pd
from time import time
from datetime import datetime
from dateutil.relativedelta import relativedelta

# Local Imports
from lib.api.binance.local import filename

class database:
    def __init__(self, verbose:bool=False):
        self.df = None
        self.verbose = verbose

    def kline_df(self, symbol:str, interval:str, starttime:int, endtime:int) -> pd.DataFrame:
        # Filepath based on inputs
        filepath = f"db/klines/{symbol.lower()}/{interval}/"

        # Start and endtime
        dt_start = datetime.fromtimestamp(starttime)
        dt_end = datetime.fromtimestamp(endtime)

        # Verbose print
        if self.verbose:
            print(f"start: {datetime.fromtimestamp(starttime)}")
            print(f"end: {datetime.fromtimestamp(endtime)}")
        
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
            ret_data = pd.concat([ret_data, pd.read_csv(f'{filepath}{fn}')], axis=0, ignore_index=True)
            
            # TODO - See if we can speed this up a bit
            if dt_start.timestamp() > (ret_data.iloc[0]['time']/1000):
                ret_data = ret_data.loc[ret_data['time'] > dt_start.timestamp()]
                first = False

            if dt_end.timestamp() < (ret_data.iloc[-1]['time']/1000):
                ret_data = ret_data.loc[ret_data['time'] < dt_end.timestamp()]

            # Go to next month
            dt_start += relativedelta(months=1)

        self.df = ret_data
        # Return data
        return ret_data
    