from concurrent.futures import ThreadPoolExecutor
from fastapi import Depends, FastAPI, Request
from fastapi.responses import JSONResponse, PlainTextResponse

from ai import ai_reply
from config import LOGGER, WEWORK_CORPID, WEWORK_ENCODING_AES_KEY, WEWORK_TOKEN
from kv import get_cursor, get_msg_retry, set_msg_retry
from schema import WeChatMessage, WeChatTokenMessage, WechatMsgEntity, WechatMsgSendEntity
from util.wx_biz_json_msg_crypt import WXBizJsonMsgCrypt
from wework import check_signature, parse_wechat_message, select_msgs, send_text_msg


thread_pool = ThreadPoolExecutor(max_workers=5)  # 创建一个线程池，最大工作线程数为5

app = FastAPI()


@app.get("/ping")
async def ping():
    return {"message": "pong"}


@app.get("/wechat/hook")
async def wechat_hook_verification(
    msg_signature: str, timestamp: str, nonce: str, echostr: str
):
    ret, sEchoStr = check_signature(msg_signature, timestamp, nonce, echostr)
    if ret == 0:
        from fastapi.responses import PlainTextResponse

        return PlainTextResponse(
            content=sEchoStr, media_type="text/plain;charset=utf-8"
        )
    else:
        return JSONResponse(content={"error": "Verification failed"}, status_code=400)


@app.post("/wechat/hook")
async def wechat_hook_event(
    msg_signature: str, timestamp: str, nonce: str,
    message: WeChatMessage = Depends(parse_wechat_message)
    ):
    LOGGER.info("Received WeChat message: %s", message)
    msg_crypt = WXBizJsonMsgCrypt(WEWORK_TOKEN, WEWORK_ENCODING_AES_KEY, WEWORK_CORPID)
    ret, xml_content = msg_crypt.DecryptMsg(
        message.Encrypt,
        msg_signature,
        timestamp,
        nonce
    )
    token_msg = WeChatTokenMessage.from_xml(xml_str=xml_content)
    LOGGER.info(f"Received WeChat token message: {token_msg.model_dump_json()}")
    cursor = get_cursor()
    process_msg(token_msg.Token, cursor)
    return JSONResponse(content={"message": "Event received"})


def process_msg(token: str, cursor: str):
    msg_entities, has_more, next_cursor = select_msgs(cursor=cursor, token=token)
    last_5 = msg_entities[-5:] if len(msg_entities) >= 5 else msg_entities
    for msg in last_5:
        content = msg.text.get('content')
        thread_pool.submit(reply_msg, msg.msgid, msg.external_userid, msg.open_kfid, content)
    
def reply_msg(msgid: str, external_userid: str, open_kfid: str, content: str):
    if get_msg_retry(msgid):
        return
    send_text_msg(msgid, external_userid, open_kfid, ai_reply(content))
    set_msg_retry(msgid, 0)



if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
