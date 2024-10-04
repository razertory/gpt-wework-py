import logging
import os
from dotenv import load_dotenv
import redis

# 加载 .env 文件中的环境变量
load_dotenv()

# WeWork 配置
WEWORK_TOKEN_API = "https://qyapi.weixin.qq.com/cgi-bin/gettoken"
WEWORK_CORPID = os.getenv("WEWORK_CORPID")
WEWORK_CORPSECRET = os.getenv("WEWORK_CORPSECRET")
WEWORK_ENCODING_AES_KEY = os.getenv("WEWORK_ENCODING_AES_KEY")
WEWORK_TOKEN = os.getenv("WEWORK_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# 应用配置
DEBUG = os.getenv("DEBUG", "False").lower() == "true"

# Redis 配置
REDISHOST = os.getenv("REDISHOST", "localhost")
REDISPORT = int(os.getenv("REDISPORT", 6379))
REDIS_DB = int(os.getenv("REDIS_DB", 0))
REDIS_PASSWORD = os.getenv("REDIS_PASSWORD", None)

REDIS_CLIENT = redis.Redis(host=REDISHOST, port=REDISPORT, db=REDIS_DB, password=REDIS_PASSWORD)

# 日志配置
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
LOGGER = logging.getLogger(__name__)