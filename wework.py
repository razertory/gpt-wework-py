# 
import time
from config import WEWORK_CORPID, WEWORK_CORPSECRET, WEWORK_TOKEN_API
import requests

token_cache = {}


def check_signature(signature, timestamp, nonce):
    return True

def cachable_token():
    current_time = time.time()
    if not token_cache.get('token') or current_time - token_cache.get('timestamp', 0) > 3600:
        token_cache['token'] = _wework_token()
        token_cache['timestamp'] = current_time
    return token_cache['token']


def _wework_token():
    response = requests.get(WEWORK_TOKEN_API, params={"corpid": WEWORK_CORPID, "corpsecret": WEWORK_CORPSECRET})
    json_data =  response.json()
    return json_data['AccessToken']

