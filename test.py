# Imports
import pandas as pd

# Local Imports
from lib.api.binance.interface import Binance
from lib.api.binance.local import filename

# Test object
filepath = "db/klines/ethusdt/1m/"
months = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12']
file_list = []
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
for x in months:
    # file_list.append(filename("ETHUSDT", "1m", '2022', x))
    fn = filename("ETHUSDT", "1m", '2022', x)
    
    ret_data = pd.concat([ret_data, pd.read_csv(f'{filepath}{fn}')])


print(ret_data)