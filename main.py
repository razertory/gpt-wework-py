from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, PlainTextResponse

from config import LOGGER
from wework import check_signature

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
async def wechat_hook_event(request: Request):
    # 处理企业微信服务器推送的事件
    event_data = await request.body()
    LOGGER.info("Received XML data", event_data)
    # 在这里处理事件数据
    return JSONResponse(content={"message": "Event received"})


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
