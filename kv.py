from config import REDIS_CLIENT

def set_cursor(cursor: str):
    REDIS_CLIENT.set("cursor", cursor)

def get_cursor():
    return REDIS_CLIENT.get("cursor")


def set_msg_retry(msgid: str, retry: int):
    REDIS_CLIENT.set(f"msg_retry_{msgid}", retry)

def get_msg_retry(msgid: str):
    return REDIS_CLIENT.get(f"msg_retry_{msgid}")

