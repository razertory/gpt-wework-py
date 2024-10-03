from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from config import WEWORK_CORPID, WEWORK_ENCODING_AES_KEY, WEWORK_TOKEN
from wx_biz_json_msg_crypt import WXBizJsonMsgCrypt

app = FastAPI()

@app.get("/ping")
async def ping():
    return {"message": "pong"}

@app.get("/wechat/hook")
async def wechat_hook_verification(msg_signature: str, timestamp: str, nonce: str, echostr: str):
    # 这里需要实现企业微信服务器验证逻辑
    # 验证成功后返回echostr
    print(msg_signature, timestamp, nonce, echostr)

    msg_crypt = WXBizJsonMsgCrypt(WEWORK_TOKEN,
                                  WEWORK_ENCODING_AES_KEY, 
                                  WEWORK_CORPID)

    print(WEWORK_TOKEN, WEWORK_ENCODING_AES_KEY, WEWORK_CORPID)

    ret, sEchoStr = msg_crypt.VerifyURL(msg_signature, timestamp, nonce, echostr)
    print(f"VerifyURL ret: {ret}, sEchoStr: {sEchoStr}")
    return sEchoStr

@app.post("/wechat/hook")
async def wechat_hook_event(request: Request):
    # 处理企业微信服务器推送的事件
    event_data = await request.json()
    # 在这里处理事件数据
    return JSONResponse(content={"message": "Event received"})

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)