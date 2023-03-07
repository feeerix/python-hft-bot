# Imports


# Local Imports
from ..file.writer import *

class API:
    def __init__(self, name:str) -> None:
        self.name = name

        # Initialising all required folder structure
        if not folder_exists(self.name,"db/info/"):
            create_folder(self.name,"db/info/")
        
        