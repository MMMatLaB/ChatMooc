# 导入所需模块
from langchain_community.document_loaders import TextLoader
from langchain_community.vectorstores import Milvus
from langchain_text_splitters import CharacterTextSplitter
from langchain_community.embeddings import DashScopeEmbeddings
import os

# 设置 DashScope API 密钥
os.environ["DASHSCOPE_API_KEY"] = 'sk-651aa47bea79499daf2f3014d4bdfa28'

# 初始化 DashScope 嵌入模型
embeddings = DashScopeEmbeddings(
    model="text-embedding-v1"
)
#
# # 加载文本数据
# loader = TextLoader("test.txt", encoding="utf-8")
# documents = loader.load()
#
# # chunk_size: 每个文本片段的大小。在这里设置为1000，表示每个文本片段包含1000个字符。如果一个文档的字符数超过1000，将会被分割成多个包含1000个字符的文本片段。
# chunk_size = 1000
# # chunk_overlap: 连续文本片段之间的重叠量。在这里设置为0，表示文本片段之间没有重叠。如果设置为一个正值，例如100，每个文本片段将会有100个字符的重叠。
# chunk_overlap = 0
# # 创建CharacterTextSplitter对象，用于将文本拆分成指定大小的片段。
# text_splitter = CharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
# docs = text_splitter.split_documents(documents)
# # 使用 Milvus 构建向量数据库
# vector_db = Milvus.from_documents(
#     docs,
#     embeddings,
#     # collection_name="text-embedding-v1",
#     connection_args={"host": "127.0.0.1", "port": "19530"},
# )
#
# # 执行相似度搜索
# query = "张景说了什么"
# docs = vector_db.similarity_search(query)
#
# # 打印匹配的页面内容
# print(docs[0].page_content)

from langchain_core.documents import Document
# docs = [
#     Document(page_content="i worked at kensho", metadata={"namespace": "harrison"}),
#     Document(page_content="i worked at facebook", metadata={"namespace": "ankush"}),
# ]
# 指定metadata中的namespace字段作为分区键
vectorstore = Milvus(
    # docs,
    # embeddings,
    # embeddings=embeddings,
    # embedding=embeddings,
    embedding_function=embeddings,
    connection_args={"host": "127.0.0.1", "port": "19530"},
    # drop_old=True,
    # partition_key_field="namespace",  # Use the "namespace" field as the partition key

)
# This will only get documents for Ankush
# This will only get documents for Ankush
# 使用 vectorstore 的 as_retriever 方法创建检索器，并指定搜索参数为 {'expr': 'namespace == "ankush"'}
# 这里的 'namespace == "ankush"' 表示要搜索的向量命名空间是 "ankush"。
retriever = vectorstore.as_retriever(search_kwargs={"expr": 'namespace == "ankush"'})
# similarity_search
# 调用检索器的 invoke 方法，并传入查询语句 "where did i work?"，以执行搜索。
# 查询语句表示要搜索包含特定内容的文档，这里是搜索包含 "where did i work?" 的文档。
res = retriever.invoke("where did i work?")

print(res)