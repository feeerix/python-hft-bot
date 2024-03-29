# Import
import json
import os
from typing import Union

# TODO - probably good to update this to "get_dict" to align with below function
# def get_json(path:str) -> dict:
#     with open(path, 'r') as json_file:
#         data = json.load(json_file)
#     return data

def get_json(path:str, filename:str) -> Union[dict, list]:
    # print(path)
    # print(filename)
    with open(path+filename, 'r') as json_file:
        data = json.load(json_file)
    return data

def get_list(path:str) -> list:
    with open(path, 'r') as json_file:
        data = json.load(json_file)
    return data

def file_exists(filename:str, filepath:str) -> bool:
    if os.path.isfile(f"{filepath}{filename}"):
        return True
    else:
        return False
    
def list_folders(path:str) -> list:
    return [name for name in os.listdir(path) if os.path.isdir(os.path.join(path, name))]

def list_files(path:str) -> list:
    return [name for name in os.listdir(path) if os.path.isfile(os.path.join(path, name))]

def db_check(path:str) -> dict:
    # If the file exists
    path += "/check.json"
    if file_exists(path):
        get_json(path)
    else:
        print("File does not exist!")