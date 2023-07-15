# Imports
from time import time
from enum import Enum


def get_last_closed_time(interval_tc:int):
    return (int(time() - interval_tc) // interval_tc) * interval_tc


"""
Potentially how I can change my specific interval class to.
"""
class _Interval(Enum):
    _1m = 60
    _5m = 300
    _15m = 900
    _1h = 3600
    _4h = 14400
    _1D = 86400
    _1W = 604800

    # Bypassing Enum's __new__ method
    def __new__(cls, seconds):
        obj = object.__new__(cls)
        obj._value_ = seconds
        return obj

    def __init__(self, seconds):
        self.ms = False

    def __str__(self) -> str:
        return self.name[1:]

    def tc_rep(self) -> int:
        return self.value
    
    
    def last_close(self) -> int:
        if self.ms:
            return get_last_closed_time(self.value) * 1000
        else:
            return get_last_closed_time(self.value)

# Not sure if a whole class is required yet - will leave in and go from there
class Interval():
    # _1m = 60
    # _5m = 300
    # _15m = 900
    # _1h = 3600
    # _4h = 14400
    # _1D = 86400
    # _1W = 604800

    def __init__(self, str_interval:str, ms:bool=False):
        self.str_interval = str_interval

        self.interval_table = {
            '1m': 60,
            '5m': 300,
            '15m': 900,
            '1h': 3600,
            '4h': 14400,
            '1D': 86400,
            '1W': 604800
        }

        self.ms = ms
        

    def tc_rep(self) -> int:
        return self.interval_table[self.str_interval]
    
    def str_rep(self) -> str:
        
        return self.str_interval
    
    def last_close(self) -> int:
        if self.ms:
            return get_last_closed_time(self.tc_rep()) * 1000
        else:
            return get_last_closed_time(self.tc_rep())