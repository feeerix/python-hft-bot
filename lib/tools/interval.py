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
    # def __new__(cls, seconds):
    #     obj = object.__new__(cls)
    #     obj._value_ = seconds
    #     return obj
    
    @property
    def str(self):
        return self.name[1:]

    @classmethod
    def from_string(cls, interval_str: str):
        # Prepend underscore for our internal representation
        interval_key = f"_{interval_str}"
        if interval_key in cls._member_names_:
            return cls[interval_key]
        else:
            raise ValueError(f"No interval found for '{interval_str}'")
        
    @classmethod
    def from_seconds(cls, seconds: int):
        for member in cls:
            if member.value == seconds:
                return member
        raise ValueError(f"No interval found for '{seconds}' seconds")

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
