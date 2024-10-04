from fastapi import Depends, FastAPI, Request
from fastapi.responses import JSONResponse, PlainTextResponse

from ai import ai_reply
from config import LOGGER, WEWORK_CORPID, WEWORK_ENCODING_AES_KEY, WEWORK_TOKEN
from schema import WeChatMessage, WeChatTokenMessage, WechatMsgEntity, WechatMsgSendEntity
from util.wx_biz_json_msg_crypt import WXBizJsonMsgCrypt
from wework import check_signature, parse_wechat_message, select_msgs, send_text_msg


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

    msg_entities, has_more, next_cursor = select_msgs(cursor="", token=token_msg.Token)

    last: WechatMsgEntity = msg_entities[len(msg_entities)-1]

    content = last.text.get('content')


    send_text_msg(
        last.msgid,
        last.external_userid,
        last.open_kfid,
        ai_reply(content)
    )

    # 在这里处理消息数据
    return JSONResponse(content={"message": "Event received"})



if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
