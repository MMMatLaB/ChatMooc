from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.text_splitter import CharacterTextSplitter
from langchain.llms import OpenAI
from langchain.chains import RetrievalQA
from langchain.document_loaders import TextLoader

# 加载文档
loader = TextLoader("../../state_of_the_union.txt")
documents = loader.load()

# 文本分割
text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
texts = text_splitter.split_documents(documents)

# 创建嵌入向量
embeddings = OpenAIEmbeddings()

# 使用Chroma创建文档搜索引擎
docsearch = Chroma.from_documents(texts, embeddings)

# 使用DuckDB创建一个内存数据库，数据是临时的
# Running Chroma using direct local API.
# Using DuckDB in-memory for database. Data will be transient.

# 创建问答系统
qa = RetrievalQA.from_chain_type(llm=OpenAI(), chain_type="stuff", retriever=docsearch.as_retriever())

# 运行问答查询
query = "What did the president say about Ketanji Brown Jackson"
qa.run(query)

    #
    # 文档加载：使用TextLoader从指定路径加载文本文件。这里的文件是美国总统的国情咨文。
    # 文本分割：使用CharacterTextSplitter将加载的文档分割成小块，每块1000个字符，不重叠。这有助于处理大文档，使其适应模型的处理能力。
    # 嵌入向量生成：使用OpenAIEmbeddings创建文本的嵌入向量。这些向量是用于文本相似性比较的数学表示。
    # 文档搜索引擎：使用Chroma和前面生成的嵌入向量来创建一个文档搜索引擎。这个搜索引擎基于向量空间模型，能够快速检索与查询最相关的文档块。
    # 问答系统：使用RetrievalQA结合OpenAI的大型语言模型和Chroma的检索器创建一个问答系统。这个系统可以根据用户的查询从文档中检索信息，并生成答案。
    # 查询执行：执行一个查询，询问总统在国情咨文中对Ketanji Brown Jackson有何评述。

