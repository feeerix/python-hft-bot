# Import
from db.api.api import API

# Local Import
from .endpoints import ping

class Binance(API):
    def __init__(self) -> None:
        super().__init__("binance")

    def is_connected(self) -> bool:
        
        return True