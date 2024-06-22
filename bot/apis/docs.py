import os

from constants.request import OpenAIChatMsgIn, KnowledgeBaseMsgIn
from fastapi.responses import StreamingResponse
# 对模块取别名
import db.milvus as milvus
import utils.config as config
import router.router as router
import constants.response as response

from fastapi import File, Form, Body, Query, UploadFile
from langchain.embeddings import OpenAIEmbeddings

# 异步函数（协程函数）https://doiiars.com/article/bb31213f-248e-426e-a9e5-f91a1b979a24
"""
async def count():
    print("One")
    await asyncio.sleep(1)
    print("Two")

async def main():
    # 但此处，main()只执行一次，所以会等3次count()执行结束后再继续执行。
    await asyncio.gather(count(), count(), count())

asyncio.run(main())
如上代码await表示，执行第一个count()后，运行到await处，代码不会一直阻塞在这里，而是会继续执行第二个count().
"""
async def doc_upload(file: UploadFile):
    config = router.kb_config
    
    # Save to temp file
    # await等待子函数执行完成再往下执行， await 只能在带有 async 关键字的函数中运行
    # asynico.run() 运行程序
    file_content = await file.read()
    
    # Create path
    if not os.path.exists(config.get_app_file_dir()):
        os.makedirs(config.get_app_file_dir())
    
    filepath = os.path.join(config.get_app_file_dir(), file.filename)
    
    try:
        with open(filepath, "wb") as f:
            f.write(file_content)
    except Exception as e:
        return response.BaseResponse(code=500, msg=f"{file.filename} Upload error: {e}")
    
    # Get db
    db = milvus.MilvusDBService(
        embeddings=OpenAIEmbeddings(
            model=config.get_fastchat_models_embedding_model_name()),
        host=config.get_milvus_host(),
        port=config.get_milvus_port(),
        top_k=config.get_milvus_top_k(),
        score_threshold=config.get_milvus_score_threshold()
    )

    db.insert(filepath)

    return response.BaseResponse(code=200, msg=f"{file.filename} Upload success")