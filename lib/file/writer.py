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

def create_file(filename:str, filepath: str) -> bool:
    f = open(f"{filepath}{filename}", "x")
    return True # Adjust to return correct boolean
    
def write_json(file_data:dict, filename:str, folder_path:str):
    if not file_exists(filename, folder_path):
        create_file(filename,folder_path)
    
    with open(f"{folder_path}{filename}", "r+") as outjson:
        json.dump(file_data, outjson)

