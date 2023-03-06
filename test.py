# Imports
import requests as req
from datetime import datetime

# Local Imports
from lib.api.binance.interface import Binance
from tests.battery import *

# Test
test_exchange = Binance()

test_exact(
    True,
    Binance().is_connected,
    None,
    True
)

print(test_exchange.server_status())