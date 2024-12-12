# 输入：文本x，章节号sid
# 调用mysql——输入：sid，输出所有rid
# 调用vectorstore——输入：rid，和,对应信息,返回文本片段
# 将x作为问题，文本片段内容作为答案来源 喂给大模型 得到输出

# from getpass import getpass

# DASHSCOPE_API_KEY = getpass()
import os

from langchain_community.llms import Tongyi
from langchain_core.prompts import PromptTemplate

os.environ["DASHSCOPE_API_KEY"] = 'sk-651aa47bea79499daf2f3014d4bdfa28'


def gen(question):
    llm = Tongyi()
    template = """Question: {question}
    
    #提示词
    Answer: Let's think step by step."""
    prompt = PromptTemplate.from_template(template)
    chain = prompt | llm
    # question = "What NFL team won the Super Bowl in the year Justin Bieber was born?"
    res = chain.invoke({"question": question})
    print(res)


#
# def text_em():
#     from langchain_community.embeddings import DashScopeEmbeddings
#     embeddings = DashScopeEmbeddings(
#         model="text-embedding-v1"
#     )
#     text = "This is a test document."
#     query_result = embeddings.embed_query(text)
#     print(query_result)
#     doc_results = embeddings.embed_documents(["foo"])
#     print(doc_results)


if __name__ == '__main__':
    gen(question="What NFL team won the Super Bowl in the year Justin Bieber was born?")
