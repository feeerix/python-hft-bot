# Imports
import requests as req
from zipfile import ZipFile
import hashlib

def download_file(url, path, filename):
    r = req.get(f'{url}{filename}')
    f = open(f'{path}{filename}', 'wb')
    if r.status_code == 200:
        for chunk in r.iter_content(1024):
            f.write(chunk)
    f.close()

def get_checksum(filename, hash_function):
    """Generate checksum for file baed on hash function (MD5 or SHA256).
    Args:
        filename (str): Path to file that will have the checksum generated.
        hash_function (str):  Hash function name - supports MD5 or SHA256
    Returns:
        str`: Checksum based on Hash function of choice.
    Raises:
        Exception: Invalid hash function is entered.
    """
    hash_function = hash_function.lower()
    with open(filename, "rb") as f:
        bytes_data = f.read()  # read file as bytes
        if hash_function == "md5":
            readable_hash = hashlib.md5(bytes_data).hexdigest()
        elif hash_function == "sha256":
            readable_hash = hashlib.sha256(bytes_data).hexdigest()
        else:
            print("Invalid hash function. Please Enter MD5 or SHA256")

    return readable_hash


def unzip_file(filepath, dest_dir):
    file_msg = filepath.split('/')[-1]
    with ZipFile(filepath, 'r') as zf:
        zf.extractall(
            path=dest_dir
        )
        print(f'Unzipped: {file_msg}')


def compare_checksum(file, checksum):
    """
    Compares checksum to file, making sure it is the correct file.
    Currently set to SHA256
    :return: bool
    """
    f = open(checksum, "r")
    if f.read().split(' ')[0] == get_checksum(file, 'SHA256'):
        return True
    else:
        return False
    
def get_checksum(filename, hash_function):
    hash_function = hash_function.lower()
    with open(filename, "rb") as f:
        bytes_data = f.read()  # read file as bytes
        if hash_function == "md5":
            readable_hash = hashlib.md5(bytes_data).hexdigest()
        elif hash_function == "sha256":
            readable_hash = hashlib.sha256(bytes_data).hexdigest()
        else:
            print("Invalid hash function.")

    return readable_hash