# Imports
from time import time
from enum import Enum


def get_last_closed_time(interval_tc:int):
    return (int(time() - interval_tc) // interval_tc) * interval_tc

def get_next_closing_time(interval_tc:int):
    return ((int(time()) // interval_tc) + 1) * interval_tc

"""
Potentially how I can change my specific interval class to.
"""
class Interval(Enum):
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
