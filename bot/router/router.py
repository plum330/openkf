# 在模块中通过import导入系统包， 第三方依赖包，自定义包...
import sys
import os
# fastapi是一个python rest api框架
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from apis.chat import knowledge_base_chat
from apis.docs import doc_upload
import utils.config as config

# Add parent dir to sys.path so we can import from parent dir
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
# 定义模块可导出的全局变量
kb_config = None
# 定义函数，函数形参是配置类
def get_api(config: config.KBConfig) -> FastAPI:
    app = FastAPI()
    # global作用是使局部变量变成全局变量 https://blog.csdn.net/weixin_45417815/article/details/123930182
    global kb_config
    kb_config = config
    # 设置跨域中间件
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    # 定义http api接口
    app.post("/api/v1/ask")(knowledge_base_chat)
    app.post("/api/v1/doc/upload")(doc_upload)
    
    return app