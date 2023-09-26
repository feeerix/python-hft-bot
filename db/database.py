# Imports
import pandas as pd
import pandas_ta as ta
from datetime import datetime, timezone
from dateutil.relativedelta import relativedelta
from enum import Enum
import uuid
from typing import List, Dict
import numpy as np

# Local Imports
from lib.api.binance.local import filename
from lib.cli.printer import line
# from lib.file.reader import get_json, get_list
# from lib.file.writer import write_json

# from lib.tools.asset import Asset
from lib.tools.exchange import Exchange
from lib.tools.internal.exchange_type import ExchangeType
# from lib.tools.blockchain import Blockchain
from backtest.strat.indicator import Indicator
from backtest.strat.trigger import Trigger
from backtest.strat.settings.settings import Settings
from lib.tools.symbol import Symbol
from lib.tools.interval import Interval
from lib.tools.asset import Asset

class DatabaseType(Enum):
    KLINES = 'klines'
    TRIGGERS = 'triggers'
    SIGNALS = 'signals'
    PORTFOLIO = 'portfolio'
    INFO = 'info'
    LOGIC = 'logic'
    POSITIONS = 'positions'
    INDICATORS = 'indicators'
    ORDERBOOK = 'orderbook'
    RESULTS = 'results'

class DatabaseFactory:
    def create_db(self, db_type:DatabaseType=None):

        if not db_type:
            raise NotImplementedError("create_db not implemented!")

class Database:
    """
    Database class that we will use to create kline, trading signal and other dataframes.
    I know it's not a REAL database lol.

    It's job is to maintain the data - and if something is being done live making sure it's
    up to date as well as correct. We can eventually move the hash and checking mechanism
    directly within this class

    TODO - Somehow the Database uuid's seem to be the same in some circumstances.
    Need to check on what's happening here

    """
    DB_NAMESPACE = uuid.uuid4()
    db_mapping = {
        DatabaseType.KLINES: "_klines",
        DatabaseType.INDICATORS: "_indicators",
        DatabaseType.ORDERBOOK: "_orderbook",
        DatabaseType.TRIGGERS: "_triggers",
        DatabaseType.LOGIC: "_logic",
        DatabaseType.POSITIONS: "_positions",
        DatabaseType.PORTFOLIO: "_portfolio",
        DatabaseType.INFO: "_info"
    }

    # Initialises
    def __init__(self, name:str="", db_type:DatabaseType=None, verbose:bool=False, **kwargs:List[Indicator]):
        self.db_type = db_type
        self.name = name
        self.verbose = verbose
        self.df = None
        self.arguments = kwargs

        # Create a custom name based on type and uuid
        if not name or name == "":
            """
            Hacky way to get good names
            """
            if self.db_type == DatabaseType.KLINES or self.db_type == DatabaseType.INDICATORS:
                self.name = f'{db_type.name}-{self.arguments["symbol"]}-{self.arguments["interval"]}'
            else:
                # TODO - Making sure to update later
                self.name = f'{db_type.name}-TEST'

    def __str__(self) -> str:
        # {self.db_type.name}_{self.arguments['symbol']}_{self.arguments['interval']}_{self.arguments['source'].name}
        return f"DATABASE >> Name: {self.name} | db_type: {self.db_type.name} | {self.arguments}"
    
    @property
    def intervals(self) -> list:
        pass
        # return
    
    def build(self, **kwargs):
        """
        Build based on the database type.
        """

        if self.db_type == DatabaseType.KLINES:
            self.df = getattr(self, self.db_mapping[self.db_type])(**self.arguments)
            return self.df
        
        elif self.db_type == DatabaseType.INDICATORS:
            self.df = getattr(self, self.db_mapping[self.db_type])(**kwargs)
            return self.df

        elif self.db_type == DatabaseType.SIGNALS:
            self._signals(signals=self.arguments['signals'])

        # elif self.db_type

        else:
            print("You input a build type that's not recognised!")

    def _klines(self, symbol:Symbol, interval:Interval, starttime:int, endtime:int, source:ExchangeType) -> pd.DataFrame:
        """
        This will build the klines dataframe, and add it to self.df
        """
        
        # Filepath based on inputs
        filepath = f"db/klines/{symbol.symbol.lower()}/{interval}/"

        # Start and endtime
        dt_start = datetime.fromtimestamp(starttime)
        dt_end = datetime.fromtimestamp(endtime)

        distance = endtime - starttime

        # Verbose print
        if self.verbose:
            print(line)
            print(f"CREATING DATABASE - {symbol.symbol} | {interval}")
            print(f"START: {datetime.fromtimestamp(starttime,  tz=timezone.utc)}")
            print(f"END: {datetime.fromtimestamp(endtime, tz=timezone.utc)}")
        
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
            # fn = filename(source.name.lower(), symbol.symbol.lower(), interval, f"{dt_start.year}", f"{dt_start.month:02d}")
            fn = filename(source.name.lower(), symbol.symbol, interval, f"{dt_start.year}", f"{dt_start.month:02d}")
            
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

    def _indicators(
            self, 
            # symbol:List[Symbol], 
            # interval:List[Interval], 
            indicator_list:List['Database'], 
            df:pd.DataFrame=None,
            recording:bool=False
            ) -> pd.DataFrame:
        
        # for kline
        # Add all the indicators
        for indicator in indicator_list:
            
            """
            This adds the indicator columns to the current df Database
            """
            df = pd.concat(
                [
                    df, # Existing DF
                    indicator.ret_indicator(df)
                ], # New DF
                axis=1, 
                # ignore_index=True # -> removed index
            )
        # Return DF after all indicators in list added
        return df

    def _orderbook(self, symbols:List[Symbol]):
        pass

    def _logic(self):
        print("_logic in database.py")
        exit()

    def _positions(self):
        pass

    # Create a signals dataframe
    def _triggers(self, triggers:List[Trigger]=[], dataframe:pd.DataFrame=None, recording:bool=False) -> pd.DataFrame:
        """
        I should note that the entries are just adding booleans for specific trading signals.
        I will need to update this so that it better generalises when I'm adding signals for everything, not just opening and closing positions
        """
        df = pd.DataFrame()
        if self.verbose:
            print("Adding Signals...")

        for trigger in triggers:
            print(trigger.settings.arguments)
            print(trigger.settings)
            df = trigger.build_trigger(dataframe)
            print(df)
        exit()

    # Create a portfolio dataframe
    def _portfolio(self) -> pd.DataFrame:
        # Your implementation here
        pass

    # Create an info dataframe
    def _info(self) -> pd.DataFrame:
        # Your implementation here
        pass

    
