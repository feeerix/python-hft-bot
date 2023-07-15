# IMPORTS
import os
import hashlib
from datetime import datetime

# LOCAL IMPORTS
from lib.tools.internal.chunk import Chunk
from lib.file.writer import write_json

""""
This is just going to be a quick tool to add information into the db.
We want to make sure we have all information and can retreive it correctly.

"""

class Crawler:
    def __init__(self, filepath:str, verbose:bool=False):
        self.filepath = filepath
        self.verbose = verbose
        

    def verify(self):
        all_data = []
        all_hashes = []

        # all filenames
        filenames =  [f for f in os.listdir(self.filepath) 
                      if os.path.isfile(os.path.join(self.filepath, f)) and f.endswith('.csv')]

        for filename in filenames:
            chunk = Chunk(self.filepath, filename)
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
            self.filepath
        )

        if self.verbose:
            print(f"Verified folder: {self.filepath}")