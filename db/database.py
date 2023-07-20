# Imports
import pandas as pd
from datetime import datetime, timezone
from dateutil.relativedelta import relativedelta
from enum import Enum
import uuid

# Local Imports
from lib.api.binance.local import filename
from lib.cli.printer import line

from lib.tools.asset import Asset
from lib.tools.exchange import Exchange
from lib.tools.blockchain import Blockchain
from backtest.strat.indicator import Indicator
from backtest.strat.settings.settings import Settings
from lib.tools.symbol import Symbol
from lib.tools.interval import _Interval as Interval

class DatabaseType(Enum):
    KLINES = 'klines'
    SIGNALS = 'signals'
    PORTFOLIO = 'portfolio'
    INFO = 'info'
    LOGIC = 'logic'
    POSITIONS = 'positions'
    INDICATORS = 'indicators'
    ORDERBOOK = 'orderbook'

class DatabaseFactory:
    def create_db(self, db_type:DatabaseType=None):

        if not db_type:
            raise NotImplementedError("create_db not implemented!")



class _Database:
    def __init__(self, database_type:DatabaseType, symbol:Symbol, interval:Interval, starttime:int, endtime:int, exchange:Exchange, verbose:bool=False):
        self.database_type = database_type
        self.symbol = symbol
        self.interval = interval
        self.exchange = exchange    
        self.verbose = verbose

    def __str__(self) -> str:
        return f"{self.database_type.name} // {self.symbol.symbol} - {self.interval.name}"

    def verify(self):
        # First go to the database file
        filepath = f"db/{self.database_type.name}/{self.symbol}/{self.interval}/"
        filename = f"{self.exchange.exchange_type.name}-{self.symbol.assets}-{0}-{1}.csv"
        print(filepath)
        print(filename)

        
    
class Database:
    """
    Database class that we will use to create kline, trading signal and other dataframes.

    It's job is to maintain the data - and if something is being done live making sure it's
    up to date as well as correct. We can eventually move the hash and checking mechanism
    directly within this class
    
    """
    # DB_NAMESPACE = uuid.uuid4()

    # Initialises
    def __init__(self, name:str="", db_type:DatabaseType=None, verbose:bool=False, *args, **kwargs):
        self.db_type = db_type
        self.name = name
        self.verbose = verbose
        self.df = None

        # Create a custom name based on type and uuid
        if not name:
            self.name = f'{db_type.name}-{uuid.uuid3(uuid.NAMESPACE_OID, db_type.name)}'

    def __str__(self) -> str:
        return f"DATABASE >> Name: {self.name} | db_type: {self.db_type.name}"
    
    def df(self, db_type:DatabaseType, *args, **kwargs):
        if self.df and func:
            func = self.db_mapping.get(db_type)
            if func:
                self.df = func(*args, **kwargs)            
                return self.df
            else:
                raise ValueError(f"Invalid DatabaseType: {db_type}")
        else:
            raise ValueError(f"self.df does not exist. ")

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
    def _signals_df(self, symbol:Symbol, interval:Interval, starttime:int, endtime:int, *args, **kwargs) -> pd.DataFrame:
        # Your implementation here
        pass

    # Create a portfolio dataframe
    def _portfolio_df(self, symbol:Symbol, interval:Interval, starttime:int, endtime:int, *args, **kwargs) -> pd.DataFrame:
        # Your implementation here
        pass

    # Create an info dataframe
    def _info_df(self, symbol:Symbol, interval:Interval, starttime:int, endtime:int, *args, **kwargs) -> pd.DataFrame:
        # Your implementation here
        pass

    """
    ADDED THE BELOW FUNCTIONS FROM STRATEGY
    
    Migrating these from strategy means that we can better isolate functions within the
    classes to make sure classes have single abstracted responsibility

    TODO - to make sure that all the functions are working correctly based on the corresponding
    context.
    """
    
    # Add indicator to self.df
    def add_indicator(self, _indicator:Indicator, recording:bool=True):
        if self.verbose:
            print(_indicator.settings.data)

        # If we want to write the settings
        if recording:
            self.indicator_settings_list.append(_indicator.settings.data)

        """
        This adds the indicator columns to the current df Database
        """
        self.df = pd.concat(
            [
                self.df, # Existing DF
                _indicator.ret_indicator(self.df)
            ], # New DF
            axis=1, 
            # ignore_index=True # -> removed index
        )

    # Add entry conditions
    def add_entry(self, _settings:Settings, recording:bool=True):

        """
        I should note that the entries are just adding booleans for specific trading signals
        """
        # Test print
        if self.verbose:
            print(_settings.data)
            
        if recording:
            for pos_type in self.position_condition_settings.keys():

                if pos_type == _settings.data["func_name"]:
                    self.position_condition_settings[pos_type].append(
                        _settings.data
                    )

            self.df[_settings.data['name']] = np.where((
                    (self.df[_settings.data['arguments']['open'][True]].all(axis=1)) &
                    (self.df[_settings.data['arguments']['open'][False]].sum(axis=1) == 0)
            ), 1, 0)
        else:
            self.df[_settings.data['name']] = np.where((
                    (self.df[_settings.data['arguments']['open']['true']].all(axis=1)) &
                    (self.df[_settings.data['arguments']['open']['false']].sum(axis=1) == 0)
            ), 1, 0)

    # Add close conditions
    def add_close(self, _settings:Settings, recording:bool=True):    
        # Test print
        if self.verbose:
            print(_settings.data)
        

        if recording:
            for pos_type in self.position_condition_settings.keys():

                if pos_type == _settings.data["func_name"]:
                    self.position_condition_settings[pos_type].append(
                        _settings.data
                    )
            
            self.df[_settings.data['name']] = np.where((
                    (self.df[_settings.data['arguments']['close'][True]].all(axis=1)) &
                    (self.df[_settings.data['arguments']['close'][False]].sum(axis=1) == 0)
            ), 1, 0)
            
        else:
            self.df[_settings.data['name']] = np.where((
                    (self.df[_settings.data['arguments']['close']['true']].all(axis=1)) &
                    (self.df[_settings.data['arguments']['close']['false']].sum(axis=1) == 0)
            ), 1, 0)
