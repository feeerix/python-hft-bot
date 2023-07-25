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
from backtest.strat.settings.settings import Settings
from lib.tools.symbol import Symbol
from lib.tools.interval import Interval

class DatabaseType(Enum):
    KLINES = 'klines'
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

    It's job is to maintain the data - and if something is being done live making sure it's
    up to date as well as correct. We can eventually move the hash and checking mechanism
    directly within this class
   
    TODO - Somehow the Database uuid's seem to be the same in some circumstances.
    Need to check on what's happening here

    """
    DB_NAMESPACE = uuid.uuid4()

    # Initialises
    def __init__(self, name:str="", db_type:DatabaseType=None, verbose:bool=False, **kwargs:List[Indicator]):
        self.db_type = db_type
        self.name = name
        self.verbose = verbose
        self.df = None
        self.arguments = kwargs

        self.db_mapping = {
            DatabaseType.KLINES: self._klines,
            DatabaseType.INDICATORS: self._indicators,
            DatabaseType.ORDERBOOK: self._orderbook,
            DatabaseType.SIGNALS: self._signals,
            DatabaseType.LOGIC: self._logic,
            DatabaseType.POSITIONS: self._positions,
            DatabaseType.PORTFOLIO: self._portfolio,
            DatabaseType.INFO: self._info
        }

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
        return f"DATABASE >> Name: {self.name} | db_type: {self.db_type.name}"
    
    def build(self, **kwargs):
        """
        This function builds any database. 
        We currently do not want the function to take arguments.
        """

        # Totally hacky way for now to specifically append df for klines at the moment
        if self.db_type == DatabaseType.KLINES or self.db_type == DatabaseType.INDICATORS:
            # kline_title = f"{self.db_type.name}_{self.arguments['symbol']}_{self.arguments['interval']}_{self.arguments['source'].name}"
            self.df = self.db_mapping[self.db_type](**self.arguments)

            return self.df
        
        if self.db_type == DatabaseType.SIGNALS:
            # kwargs['dataframe']
            for indicator in self.arguments['indicators']:
                print(indicator)
            # print(self.arguments)
            exit()
    

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
            fn = filename(source.name.lower(), symbol.symbol.lower(), interval, f"{dt_start.year}", f"{dt_start.month:02d}")
            
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

    def _indicators(self, symbol:Symbol, interval:Interval, indicators:List[Indicator], recording:bool=False) -> pd.DataFrame:
        
        # for kline
        # Add all the indicators
        for indicator in indicators:
            if self.verbose:
                print(f"ADDING: {indicator.settings.data['name']} -> {self.name}")

            """
            This adds the indicator columns to the current df Database
            """
            self.df = pd.concat(
                [
                    self.df, # Existing DF
                    indicator.ret_indicator(self.df)
                ], # New DF
                axis=1, 
                # ignore_index=True # -> removed index
            )
        
        # Return DF after all indicators in list added
        return self.df

    def _orderbook(self):
        pass

    def _logic(self):
        pass

    def _positions(self):
        pass

    # Create a signals dataframe
    def _signals(self, indicators:List[Indicator]=[], recording:bool=False) -> pd.DataFrame:
        """
        I should note that the entries are just adding booleans for specific trading signals.
        I will need to update this so that it better generalises when I'm adding signals for everything, not just opening and closing positions
        """
        
        for _settings in indicators:
            
            
            print(self.df[_settings.settings.data['arguments']['series_a']])
            exit()

            # Test print
            if self.verbose:
                print(_settings.data)
                

            

            # Let's figure out what the fuck is happening here first.
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
            # CLOSE -----------------------------------------------------------------------------------------

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


    # Create a portfolio dataframe
    def _portfolio(self) -> pd.DataFrame:
        # Your implementation here
        pass

    # Create an info dataframe
    def _info(self) -> pd.DataFrame:
        # Your implementation here
        pass

    
