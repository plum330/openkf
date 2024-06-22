# pydantic常用于数据接口schema定义与检查的库
# 在python中定义请求结构即是定义class类变量
import pydantic
from pydantic import BaseModel
# typing用于对类型提示的支持 https://cuiqingcai.com/7071.html
from typing import List

class OpenAIMessage(BaseModel):
    role: str = "user"
    content: str = "hello"

# 通过class类把相关的对象变量组织成一个class类(作用类似struct)作为一个整体
class OpenAIChatMsgIn(BaseModel):
    model: str = "gpt-3.5-turbo"
    messages: List[OpenAIMessage]
    temperature: float = 0.7
    n: int = 1
    max_tokens: int = 1024
    stop: List[str] = []
    stream: bool = False
    presence_penalty: int = 0
    frequency_penalty: int = 0

class KnowledgeBaseMsgIn(BaseModel):
    query: str = "What is openim"