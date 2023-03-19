# Imports
from time import time


def get_last_closed_time(interval_tc:int):
    return (int(time() - interval_tc) // interval_tc) * interval_tc




# Not sure if a whole class is required yet - will leave in and go from there
class Interval:
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