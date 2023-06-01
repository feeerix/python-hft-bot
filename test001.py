import os
import requests as req
import json

from dotenv import load_dotenv

load_dotenv()
request_url = os.getenv("QUICKNODE_HTTP")
payload = {
    "method": "txpool_content",
    "params": [],
    "id": 1,
    "jsonrpc": "2.0"
}

headers = {
    'Content-Type': 'application/json'
}

response = req.post(request_url, headers=headers, data=json.dumps(payload))

print(response.text)