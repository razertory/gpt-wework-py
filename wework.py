#
import time
from config import (
    WEWORK_CORPID,
    WEWORK_CORPSECRET,
    WEWORK_ENCODING_AES_KEY,
    WEWORK_TOKEN,
    WEWORK_TOKEN_API,
)
import requests

from util.wx_biz_json_msg_crypt import WXBizJsonMsgCrypt

token_cache = {}


# 检查签名
def check_signature(msg_signature, timestamp, nonce, echostr):
    msg_crypt = WXBizJsonMsgCrypt(WEWORK_TOKEN, WEWORK_ENCODING_AES_KEY, WEWORK_CORPID)
    ret, sEchoStr = msg_crypt.VerifyURL(msg_signature, timestamp, nonce, echostr)
    return ret, sEchoStr


# 可以缓存的token
def cachable_token():
    current_time = time.time()
    if (
        not token_cache.get("token")
        or current_time - token_cache.get("timestamp", 0) > 3600
    ):
        token_cache["token"] = _wework_token()
        token_cache["timestamp"] = current_time
    return token_cache["token"]


def _wework_token():
    response = requests.get(
        WEWORK_TOKEN_API,
        params={"corpid": WEWORK_CORPID, "corpsecret": WEWORK_CORPSECRET},
    )
    json_data = response.json()
    return json_data["AccessToken"]
