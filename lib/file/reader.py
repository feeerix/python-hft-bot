# Import
import json

def get_json(path:str) -> dict:
    with open(path, 'r') as json_file:
        data = json.load(json_file)
    return data
