from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from config import WEWORK_CORPID, WEWORK_ENCODING_AES_KEY
from wework import cachable_token
from wx_biz_json_msg_crypt import WXBizJsonMsgCrypt

app = FastAPI()

@app.get("/ping")
async def ping():
    return {"message": "pong"}

@app.get("/wechat/hook")
async def wechat_hook_verification(signature: str, timestamp: str, nonce: str, echostr: str):
    # 这里需要实现企业微信服务器验证逻辑
    # 验证成功后返回echostr
    msg_crypt = WXBizJsonMsgCrypt(cachable_token(),
                                  WEWORK_ENCODING_AES_KEY, 
                                  "1")
    ret, sEchoStr = msg_crypt.VerifyURL(signature, timestamp, nonce, echostr)
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