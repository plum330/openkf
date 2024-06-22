from typing import List
# 导入langchain相关的模块
from langchain.embeddings.base import Embeddings
from langchain.embeddings import OpenAIEmbeddings
from langchain.schema import Document
from langchain.vectorstores import Milvus

# 定义向量数据库类
class MilvusDBService:
    '''
    MilvusDBService is a service that provides a simple interface to MilvusDB.
    '''
    # 实例初始化函数（设置默认参数）
    def __init__(self,
                 embeddings: Embeddings = OpenAIEmbeddings,
                 host: str = "localhost",
                 port: int = 19530,
                 top_k: int = 5,
                 score_threshold: float = 0.5):
        self.host = host
        self.port = port
        self.top_k = top_k
        self.score_threshold = score_threshold
        # 调用实例函数初始化参数
        self.milvus = self._load_db(embeddings=embeddings,
                                    host=host,
                                    port=port)

    def _load_db(self,
                 embeddings: Embeddings = OpenAIEmbeddings,
                 host: str = "localhost",
                 port: int = 19530) -> Milvus:
        # TODO: Now we only use default collection LangChainCollection
        return Milvus(embedding_function=embeddings,
                             connection_args={"host": host, "port": port})

    def search(self, query: str) -> List[Document]:
        return self.milvus.similarity_search(query, self.top_k, score_threshold=self.score_threshold)

    def insert(self, file_path: str) -> List[str]:
        # Now only use TextLoader for demo
        from langchain.document_loaders import TextLoader
        loader = TextLoader(file_path)
        docs = loader.load_and_split()


        return self.milvus.add_documents(docs)

    def delete(self, document: Document) -> List[str]:
        pass


# 直接运行当前.py文件以下代码才会执行，其余情况以下代码不会执行。
if __name__ == "__main__":
    db = MilvusDBService(
        embeddings=OpenAIEmbeddings(
            model="gpt-3.5-turbo"),
        host="127.0.0.1",
        port="19530",
        top_k=5,
        score_threshold=0.5
    )
    
    print(db.search("What is openim"))
    # db.insert("/test/asklv/OpenKF/bot/test/openim.txt")