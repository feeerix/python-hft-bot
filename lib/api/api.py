# Imports
import json

# Local Imports
from lib.file.writer import create_folder, folder_exists

# class API:
#     def __init__(self, name:str) -> None:
#         self.name = name

#         # Initialising all required folder structure
#         if not folder_exists(self.name,"db/info/"):
#             create_folder(self.name,"db/info/")
        
    
#     def base_url(self, url_index) -> str:
#         # Get base URL
#         with open(f"lib/api/{self.name}/base_urls.json", "r") as urls:
#             return json.load(urls)[url_index]