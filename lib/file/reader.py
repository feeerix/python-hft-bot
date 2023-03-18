# Import
import json
import os

def get_json(path:str) -> dict:
    with open(path, 'r') as json_file:
        data = json.load(json_file)
    return data

def file_exists(path) -> bool:
    if os.path.isfile(path):
        return True
    else:
        return False