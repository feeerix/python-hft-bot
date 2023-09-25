# IMPORT
import json
import hashlib


def hash_object(obj):
    obj_str = json.dumps(obj, sort_keys=True)
    obj_hash = hashlib.sha256(obj_str.encode())
    return obj_hash.hexdigest()

def hash_naming():
    pass

