# Imports
import requests as req
from datetime import datetime
from pprint import pprint
import json

# Local Imports
from lib.api.binance.interface import Binance
from tests.battery import *


# Test
Binance().exchange_info()

exit()
binance = Binance()

test_exact(
    True,
    Binance().is_connected,
    None,
    True
)

print(binance.server_status())