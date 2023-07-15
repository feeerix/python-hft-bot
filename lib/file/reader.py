# Import
import json
import os

def get_json(path:str) -> dict:
    with open(path, 'r') as json_file:
        data = json.load(json_file)
    return data

def file_exists(path:str) -> bool:
    if os.path.isfile(path):
        return True
    else:
        return False
    
def list_folders(path:str) -> list:
    return [name for name in os.listdir(path) if os.path.isdir(os.path.join(path, name))]

def list_files(path:str) -> list:
    return [name for name in os.listdir(path) if os.path.isfile(os.path.join(path, name))]