from typing import Optional
from pydantic import BaseModel, Field
import xml.etree.ElementTree as ET

class WeChatMessage(BaseModel):
    ToUserName: str = Field(..., description="接收消息的用户")
    AgentID: Optional[str] = Field(None, description="企业应用的id")
    MsgType: str = Field(None, description="消息类型")
    Encrypt: str = Field(..., description="加密后的消息内容")
    class Config:
        allow_population_by_field_name = True

class WeChatTokenMessage(BaseModel):
    ToUserName: str = Field(..., description="接收消息的企业微信ID")
    CreateTime: int = Field(..., description="消息创建时间（时间戳）")
    MsgType: str = Field(..., description="消息类型，这里是'event'")
    Event: str = Field(..., description="事件类型，这里是'kf_msg_or_event'")
    Token: str = Field(..., description="消息令牌")
    OpenKfId: str = Field(..., description="客服帐号ID")

    class Config:
        allow_population_by_field_name = True

    @classmethod
    def from_xml(cls, xml_str: str):
        root = ET.fromstring(xml_str)
        data = {}
        for child in root:
            if child.tag == 'CreateTime':
                data[child.tag] = int(child.text)
            else:
                data[child.tag] = child.text
        return cls(**data)
    
class WeChatTextMessage(BaseModel):
    ToUserName: str = Field(..., description="接收消息的用户")
    FromUserName: str = Field(..., description="发送消息的用户")
    CreateTime: int = Field(..., description="消息创建时间（时间戳）")
    MsgType: str = Field(..., description="消息类型，这里应该是'text'")
    Content: str = Field(..., description="消息内容")
    MsgId: str = Field(..., description="消息ID")
    AgentID: Optional[str] = Field(None, description="企业应用的id")

    class Config:
        allow_population_by_field_name = True 
    
    
class WechatMsgEntity(BaseModel):
    msgid: str = Field(..., description="消息ID")
    open_kfid: str = Field(..., description="客服帐号ID")
    external_userid: str = Field(..., description="外部用户ID")
    send_time: int = Field(..., description="消息发送时间（时间戳）")
    origin: int = Field(..., description="消息来源")
    msgtype: str = Field(..., description="消息类型")
    text: Optional[dict] = Field(None, description="文本消息内容")

    class Config:
        allow_population_by_field_name = True
    

class WechatMsgSendEntity(BaseModel):
    touser: str = Field(..., description="外部用户ID")
    open_kfid: str = Field(..., description="客服帐号ID")
    #msgid: Optional[str] = Field(..., description="消息ID")
    msgtype: str = Field(..., description="消息类型")
    text: Optional[dict] = Field(None, description="文本消息内容")

    class Config:
        allow_population_by_field_name = True  