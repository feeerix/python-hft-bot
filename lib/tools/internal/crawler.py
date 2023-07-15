# IMPORTS
import os
import hashlib
from datetime import datetime

# LOCAL 
from db.database import DatabaseType
from lib.tools.internal.chunk import Chunk
from lib.tools.symbol import Symbol as Symbol
from lib.tools.interval import Interval
from lib.file.writer import write_json
from lib.file.reader import list_files, list_folders

""""
This is just going to be a quick tool to add information into the db.
We want to make sure we have all information and can retreive it correctly.

"""




class Crawler:
    
    def __init__(self, verbose:bool=False):
        self.verbose = verbose
        self.function_map = {
            DatabaseType.kline: self.verify_kline,
            DatabaseType.signals: self.verify_signals,
            DatabaseType.portfolio: self.verify_portfolio,
            DatabaseType.info: self.verify_info
        }

    
    def verify(self, verify_type:DatabaseType, **kwargs):
        self.function_map[verify_type](**kwargs)
        

    def verify_kline(self, symbol:Symbol=None, interval:Interval=None):
        
        filepath = f"db/klines/"

        if not symbol:
            symbols = list_folders(filepath)
            for _symbol in symbols:
                self.verify_kline(_symbol)
        else:
            filepath += symbol+"/"

        if not interval and symbol:
            intervals = list_folders(filepath)
            for _interval in intervals:
                self.verify_kline(symbol, _interval)
        else:
            filepath += interval + "/"

        # filepath = f"db/klines/{symbol}/{interval}/"
        print(f"FILEPATH: {filepath}")
        all_data = []
        all_hashes = []

        # all filenames
        filenames =  [f for f in os.listdir(filepath) 
                      if os.path.isfile(os.path.join(filepath, f)) and f.endswith('.csv')]

        for filename in filenames:
            chunk = Chunk(filepath, filename)
            file_data = chunk.data()
            file_hash = file_data['hash']
            
            # Check for duplicates
            if file_hash in all_hashes:
                print("duplicate found")
                break
        
            # output
            all_data.append(file_data)
            all_hashes.append(file_hash)

        
        # Concatenate all hashes into a single string
        concatenated_hashes = "".join(all_hashes)
        # Compute the hash of the concatenated string
        all_hashes_hash = hashlib.sha256(concatenated_hashes.encode()).hexdigest()
        
        output = {
            "hash": all_hashes_hash,
            "last_update": int(datetime.utcnow().timestamp()),
            "data": all_data
        }

        # write json
        write_json(
            output,
            "check.json",
            filepath
        )

        print(f"Verified folder: {filepath}")

    def verify_signals(self):
        pass

    def verify_portfolio(self):
        pass
        
    def verify_info(self):
        pass