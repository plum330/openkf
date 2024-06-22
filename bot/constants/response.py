# pydantic常用于数据接口schema定义与检查的库
# 在python中定义响应结构即是定义class类变量
import pydantic
from pydantic import BaseModel

class BaseResponse(BaseModel):
    # 定义并初始化
    # code: int 说明定义字段将被赋值的对象类型
    code: int = pydantic.Field(200, description="HTTP status code")
    msg: str = pydantic.Field("success", description="HTTP status message")
    data: dict = pydantic.Field({}, description="HTTP response data")