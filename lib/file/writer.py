# Import
import os

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