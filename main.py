from fastapi import Depends, FastAPI, Request
from fastapi.responses import JSONResponse, PlainTextResponse

from config import LOGGER, WEWORK_CORPID, WEWORK_ENCODING_AES_KEY, WEWORK_TOKEN
from schema import WeChatMessage, WeChatTokenMessage, WechatMsgSendEntity
from util.wx_biz_json_msg_crypt import WXBizJsonMsgCrypt
from wework import check_signature, parse_wechat_message, select_msgs, send_msg


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

    token_msg.Token

    msg_entities = select_msgs()

    first = msg_entities[0]

    content = first.text.get('content')

    send_msg(
        WechatMsgSendEntity(
            touser=first.external_userid,
            open_kfid=first.open_kfid,
            msgtype="text",
            text={
                "content": content + "瓜娃子"
            }
        )
    )


    # 在这里处理消息数据
    return JSONResponse(content={"message": "Event received"})



if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
