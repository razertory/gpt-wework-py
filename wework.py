#
import json
import time
from typing import List

from fastapi import Request
from config import (
    LOGGER,
    WEWORK_CORPID,
    WEWORK_CORPSECRET,
    WEWORK_ENCODING_AES_KEY,
    WEWORK_TOKEN,
    WEWORK_TOKEN_API,
)
import requests

import xml.etree.ElementTree as ET
from schema import WeChatMessage, WechatMsgEntity, WechatMsgSendEntity
from util.wx_biz_json_msg_crypt import WXBizJsonMsgCrypt

token_cache = {}


async def parse_wechat_message(request: Request) -> WeChatMessage:
    body = await request.body()
    xml_data = body.decode('utf-8')
    root = ET.fromstring(xml_data)
    
    message_dict = {
        'ToUserName': root.find('ToUserName').text,
        'AgentID': root.find('AgentID').text,
        'Encrypt': root.find('Encrypt').text
    }
    
    return WeChatMessage(**message_dict)



# 检查签名
def check_signature(msg_signature, timestamp, nonce, echostr):
    msg_crypt = WXBizJsonMsgCrypt(WEWORK_TOKEN, WEWORK_ENCODING_AES_KEY, WEWORK_CORPID)
    ret, sEchoStr = msg_crypt.VerifyURL(msg_signature, timestamp, nonce, echostr)
    return ret, sEchoStr


def select_msgs(cursor: str, token: str) -> List[WechatMsgEntity]:
    resp = requests.post(
        "https://qyapi.weixin.qq.com/cgi-bin/kf/sync_msg",
        params={
            "access_token": _cachable_token()
        },
        data=json.dumps(
            {
                "limit": 1000
            }
        )
    )
    resp_data = resp.json()
    msgs = resp_data.get("msg_list", [])
    has_more = resp_data.get("has_more", 0)
    next_cursor = resp_data.get("next_cursor")
    msg_entities = [WechatMsgEntity(**msg) for msg in msgs]
    return msg_entities, has_more == 1, next_cursor


# 发送消息给用户
def send_text_msg(external_user_id, kf_id, content): 
    _send_msg(
        WechatMsgSendEntity(
            touser=external_user_id,
            open_kfid=kf_id,
            msgtype="text",
            text={
                "content": content
            }
        )
    )

def _send_msg(entity: WechatMsgSendEntity):
    payload = entity.model_dump_json()
    resp = requests.post(
        "https://qyapi.weixin.qq.com/cgi-bin/kf/send_msg",
        params={
            "access_token": _cachable_token()
        },
        data=payload,
    )

    LOGGER.info("ok to send msg with resp", resp, resp.content, payload)
    return resp


# 可以缓存的token
def _cachable_token():
    current_time = time.time()
    if (
        not "token" in token_cache.keys()
        or current_time - token_cache.get("timkestamp", 0) > 3600
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
    print(json_data)
    return json_data["access_token"]
