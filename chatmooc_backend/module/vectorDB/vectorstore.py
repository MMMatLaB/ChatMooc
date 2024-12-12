import os

from langchain_community.embeddings import DashScopeEmbeddings
from langchain_community.vectorstores import Milvus
from langchain_text_splitters import CharacterTextSplitter

COLLECTION_NAME = 'document_store'
# 设置 DashScope API 密钥
os.environ["DASHSCOPE_API_KEY"] = 'sk-651aa47bea79499daf2f3014d4bdfa28'
# 初始化 DashScope 嵌入模型
embeddings = DashScopeEmbeddings(
    model="text-embedding-v1"
)
CONNECTION_CONFIG = {"host": "127.0.0.1",
                     "port": "19530"}

import logging


def load2milvus(rid, parsed_path):
    rid = str(rid)
    logging.info(f"Loading {parsed_path} to Milvus")
    from langchain_community.document_loaders import TextLoader
    loader = TextLoader(parsed_path, encoding="utf-8")
    # data preprocessing
    spliter = CharacterTextSplitter(
        separator="\n\n",
        chunk_size=800,
        chunk_overlap=200,
        length_function=len,
        is_separator_regex=False,
    )
    documents = spliter.split_documents(loader.load())
    for doc in documents:
        doc.metadata["namespace"] = rid
    # 保存文档到 Milvus
    logging.info(f"begin to build Milvus")
    try:
        vectordb = Milvus(embedding_function=embeddings, connection_args=CONNECTION_CONFIG, drop_old=True)
        vectordb.from_documents(
            documents=documents,
            embedding=embeddings,
            collection_name=COLLECTION_NAME,
            connection_args=CONNECTION_CONFIG,
            partition_key_field="namespace"
        )
    except Exception as e:
        logging.error(f"Milvus build failed: {e}")
        return False
    logging.info(f"Milvus build success")
    return True


def query(rid):
    store = Milvus(
        collection_name='document_store',
        embedding_function=embeddings,
        connection_args=CONNECTION_CONFIG,
    )

    # 使用正确的过滤条件
    expr = f'namespace == "{rid}"'
    args = {"metric_type": "L2", "params": {}, "expr": expr}

    retriever = store.as_retriever(search_kwargs=args)
    res = retriever.invoke(" ", top_k=6)
    return res


def prin(res):
    for item in res:
        print(item.page_content)


def query_by_rid(rid):
    store = Milvus(
        collection_name='document_store',
        embedding_function=embeddings,
        connection_args=CONNECTION_CONFIG,
    )

    # 使用正确的过滤条件
    expr = f'namespace == "{rid}"'
    args = {"metric_type": "L2", "params": {}, "expr": expr}
    logging.info(f"search with args: {args}")
    retriever = store.as_retriever(search_kwargs=args)
    res = retriever.invoke(" ", top_k=6)
    print(res)
    return res


if __name__ == '__main__':
    # load("5", "txt", "s.txt")
    prin(query(5))
    # query("2", " what is the capital of india?")
    # get_text_fragments_by_rid(3)
    # query_by_rid(5)
