# Imports
import pandas as pd
from datetime import datetime, timezone
from dateutil.relativedelta import relativedelta
from enum import Enum

# Local Imports
from lib.api.binance.local import filename
from lib.cli.printer import line

from lib.tools.asset import Asset
from lib.tools.exchange import Exchange
from lib.tools.blockchain import Blockchain
from lib.tools.symbol import Symbol
from lib.tools.interval import _Interval as Interval

class DatabaseType(Enum):
    kline = 'klines'
    signals = 'signals'
    portfolio = 'portfolio'
    info = 'info'

class _Database:
    def __init__(self, database_type:DatabaseType, symbol:Symbol, interval:Interval, starttime:int, endtime:int, exchange:Exchange, verbose:bool=False):
        self.database_type = database_type
        self.symbol = symbol
        self.interval = interval
        self.exchange = exchange    
        self.verbose = verbose

    def __str__(self) -> str:
        return self.database_type.name

    def verify(self):
        # First go to the database file
        filepath = f"db/{self.database_type.name}/{self.symbol}/{self.interval}/"
        filename = f"{self.exchange.exchange_type.name}-{self.symbol.symbol}-{0}-{1}.csv"
        print(filepath)
        print(filename)

        
    
class Database:
    """
    Database class that we will use to create kline, trading signal and other dataframes.
    """

    # Initialises
    def __init__(self, verbose:bool=False):
        self.verbose = verbose
        self.db_mapping = {
            DatabaseType.kline: self._kline_df,
            DatabaseType.signals: self._signals_df,
            DatabaseType.portfolio: self._portfolio_df,
            DatabaseType.info: self._info_df,
        }

    def df(self, db_type:DatabaseType, *args, **kwargs):
        func = self.db_mapping.get(db_type)
        if func:
            return func(*args, **kwargs)
        else:
            raise ValueError(f"Invalid DatabaseType: {db_type}")

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
    
    
    # TODO - to make this the default kline df going forward
    def _kline_df(self, symbol:Symbol, interval:Interval, starttime:int, endtime:int) -> pd.DataFrame:
        # Filepath based on inputs
        filepath = f"db/klines/{symbol.symbol.lower()}/{interval}/"

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

    # Create a signals dataframe
    def _signals_df(self, *args, **kwargs) -> pd.DataFrame:
        # Your implementation here
        pass

    # Create a portfolio dataframe
    def _portfolio_df(self, *args, **kwargs) -> pd.DataFrame:
        # Your implementation here
        pass

    # Create an info dataframe
    def _info_df(self, *args, **kwargs) -> pd.DataFrame:
        # Your implementation here
        pass