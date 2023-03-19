# Import
import os
import json

# Local Import

# Create folder
def create_folder(folder_name:str, folder_path:str) -> bool:
    os.mkdir(f"{folder_path}{folder_name}")
    return True

# Check if a folder exists
def folder_exists(folder_name:str, folder_path:str) -> bool:
    if os.path.isdir(f"{folder_path}{folder_name}"):
        return True
    else:
        return False
    
def write_json(file_data:dict, filename:str, folder_path:str):
    with open(f"{folder_path}{filename}") as outjson:
        json.dump(file_data, outjson)