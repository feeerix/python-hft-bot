# IMPORT
import pandas as pd

# LOCAL IMPORT
from lib.file.reader import *
from lib.file.writer import *
# from lib.file.finder import *

class Chunk:
    def __init__(self, filepath:str, filename:str):
        self.filepath = filepath
        self.filename = filename
        self.df = pd.read_csv(f"{filepath}/{filename}")
    
    def __str__(self) -> str:
        return f"CHUNK: {self.filename}"
    
    