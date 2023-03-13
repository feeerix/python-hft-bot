# Imports
import requests as req
from zipfile import ZipFile
import hashlib

def download_file(url, path, filename):
    # https://data.binance.vision/data/spot/monthly/klines/ETHBTC/1m/ETHBTC-1m-2017-09.zip
    r = req.get(f'{url}')
    print(r.status_code)
    f = open(f'{path}{filename}', 'wb')
    if r.status_code == 200:
        for chunk in r.iter_content(1024):
            f.write(chunk)
    f.close()

def get_checksum(filename, hash_function):
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


def unzip_file(filepath, filename):
    print(filepath+filename+".zip")
    # exit()
    with ZipFile(filepath+filename+".zip", 'r') as zf:
        zf.extractall(
            path=filepath
        )
        print(f'Unzipped: {filename}.zip')
    zf.close()



def compare_checksum(file, checksum):
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

def link_exists(path) -> bool:
    r = req.head(path)
    return r.status_code == req.codes.ok