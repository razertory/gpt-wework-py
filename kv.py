from config import REDIS_CLIENT

def set_cursor(cursor: str):
    REDIS_CLIENT.set("cursor", cursor)

def get_cursor():
    return REDIS_CLIENT.get("cursor")




