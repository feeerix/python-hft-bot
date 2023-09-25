import requests as req

def get_data(base_url:str, path:str, verbose:bool):
    if verbose:
        print(f"Request: GET -> {base_url}{path}")
    return req.get(f"{base_url}{path}")
