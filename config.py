import logging
import os
from dotenv import load_dotenv

# 加载 .env 文件中的环境变量
load_dotenv()

# WeWork 配置
WEWORK_TOKEN_API = "https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid=%s&corpsecret=%s"
WEWORK_CORPID = os.getenv("WEWORK_CORPID")
WEWORK_CORPSECRET = os.getenv("WEWORK_CORPSECRET")
WEWORK_ENCODING_AES_KEY = os.getenv("WEWORK_ENCODING_AES_KEY")
WEWORK_TOKEN = os.getenv("WEWORK_TOKEN")

# 应用配置
DEBUG = os.getenv("DEBUG", "False").lower() == "true"

# 日志配置
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
LOG_FILE = os.getenv("LOG_FILE", "app.log")
