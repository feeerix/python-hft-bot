# Imports
import requests as req

# Local Imports
from db.api.binance.interface import Binance


# Test
test_obj = Binance()
test_obj.is_connected()

# ret_dat = req.get("https://data.binance.com/api/v3/exchangeInfo")
# print(ret_dat)
# print(ret_dat.json())