# IMPORT
import pandas as pd
import hashlib
import io

# LOCAL IMPORT
from lib.file.reader import *
from lib.file.writer import *
# from lib.file.finder import *

class Chunk:
    def __init__(self, filepath:str, filename:str):
        self.filepath = filepath
        self.filename = filename
        self.df = pd.read_csv(f"{filepath}{filename}")
    
    def __str__(self) -> str:
        return f"CHUNK: {self.filename}"
    
    def data(self) -> dict:
        return {
            "filename": self.filename,
            "starttime": str(self.df['time'].iloc[0]),
            "endtime": str(self.df['time'].iloc[-1]),
            "hash": self.hash_dataframe()
        }
    
    # Hash dataframe function
    def hash_dataframe(self):
        # chunk_size=100000
        # Define the hash object
        hash_object = hashlib.sha256()
        
        # Create a buffer
        buffer = io.BytesIO()

        # Convert the dataframe to binary and write to buffer
        self.df.to_pickle(buffer)

        # Update the hash object with the binary data
        hash_object.update(buffer.getvalue())

        # Get the hexadecimal representation of the hash
        hash_hex = hash_object.hexdigest()

        # # Determine the number of chunks
        # num_chunks = len(self.df) // chunk_size + 1

        # # Iterate over each chunk
        # for i in range(num_chunks):
        #     # Select the chunk
        #     chunk = self.df.iloc[i*chunk_size:(i+1)*chunk_size]

        #     # Convert the chunk to a string and then to bytes
        #     chunk_bytes = chunk.to_string(index=False).encode()

        #     # Update the hash object with the bytes of the chunk
        #     hash_object.update(chunk_bytes)

        # # Get the hexadecimal representation of the hash
        # hash_hex = hash_object.hexdigest()

        return hash_hex