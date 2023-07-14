# Imports
import pandas as pd
from datetime import datetime, timezone
from dateutil.relativedelta import relativedelta
from enum import Enum

# Local Imports
from lib.api.binance.local import filename
from lib.cli.printer import line

class DatabaseType(Enum):
    kline = "kline"
    

class _Database:
    def __init__(self, symbol:str, interval:str, starttime:int, endtime:int, exchange:str, verbose:bool=False):
        self.verbose = verbose
        
    
class Database:
    """
    Database class that we will use to create kline, trading signal and other dataframes.
    """

    # Initialises
    def __init__(self, verbose:bool=False):
        self.verbose = verbose


    # Create a kline dataframe
    def kline_df(self, symbol:str, interval:str, starttime:int, endtime:int) -> pd.DataFrame:
        # Filepath based on inputs
        filepath = f"db/klines/{symbol.lower()}/{interval}/"

        # Start and endtime
        dt_start = datetime.fromtimestamp(starttime)
        dt_end = datetime.fromtimestamp(endtime)

        distance = endtime - starttime

        # Verbose print
        if self.verbose:
            print(line)
            print("CREATING DATABASE")
            print(f"start: {datetime.fromtimestamp(starttime,  tz=timezone.utc)}")
            print(f"end: {datetime.fromtimestamp(endtime, tz=timezone.utc)}")
        
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
        first = True
        last = False
        df_number = 1
        while dt_start <= dt_end:
            if self.verbose:
                print(f"{round(((int(dt_start.timestamp()) - starttime) / distance) * 100, 3)}% COMPLETE")
            
            # Get filename
            fn = filename(symbol, interval, f"{dt_start.year}", f"{dt_start.month:02d}")
            
            # add new data to return df
            new_df = pd.read_csv(f'{filepath}{fn}')
            if self.verbose:
                print(f"NEW DF LENGTH #{df_number}: {len(new_df.index)}")
                print(f"MONTH: {dt_start.month}")

            df_number += 1

            ret_data = pd.concat([ret_data, new_df], axis=0, ignore_index=True)
            
            
            # TODO - See if we can speed this up a bit
            if dt_start.month == datetime.fromtimestamp(ret_data.iloc[0]['time']/1000, tz=timezone.utc).month and dt_start.timestamp() > (int(ret_data.iloc[0]['time']/1000)):
                ret_data = ret_data.loc[dt_start.timestamp()*1000 > ret_data['time']]
                first = False

            elif dt_end.month == dt_start.month and dt_start.year == dt_end.year and dt_end.timestamp() < (int(ret_data.iloc[-1]['time']/1000)):
                ret_data = ret_data.loc[ret_data['time'] < dt_end.timestamp()*1000]

            # Go to next month
            dt_start += relativedelta(months=1)

            if self.verbose:
                print(f"TOTAL LENGTH: {len(ret_data.index)}")

        # self.df = ret_data
        ret_data = ret_data.reset_index(drop=True)

        if self.verbose:
            print("COMPLETED CREATION OF DATAFRAME")
            print(f"LENGTH OF DATAFRAME: {len(ret_data.index)}")
            print(line)

        # Return data
        return ret_data
    