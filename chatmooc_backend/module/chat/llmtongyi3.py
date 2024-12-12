# 输入rid
# 输出摘要
# 输出关键词
# 输出总结

import os

from module.vectorDB.vectorstore import query_by_rid
from langchain_community.embeddings import DashScopeEmbeddings
from langchain_community.llms import Tongyi
from langchain_core.prompts import PromptTemplate

# 设置环境变量DASHSCOPE_API_KEY

os.environ["DASHSCOPE_API_KEY"] = 'sk-651aa47bea79499daf2f3014d4bdfa28'

# 初始化 DashScope嵌入模型
embeddings = DashScopeEmbeddings(
    model="text-embedding-v1"
)

# 定义 Milvus 连接配置
CONNECTION_CONFIG = {"host": "127.0.0.1",
                     "port": "19530"}


# 从向量数据库中获取文本片段
def gettxt(rid):
    fragments = []
    for i in query_by_rid(rid):
        fragment = i.page_content
        if fragment:
            fragments.append(fragment)
    return " ".join(fragments)


# 初始化大模型
llm = Tongyi()

# 定义提示模板-摘要
prompt_template = PromptTemplate(
    input_variables=["question", "context"],
    template="问题: {question}\n\n答案来源: {context}\n\n请根据以上内容回答问题。"
)


# 定义函数来生成答案
def generate_answers(questions, context):
    answers = []
    for question in questions:
        prompt = prompt_template.format(question=question, context=context)
        response = llm(prompt)
        answers.append(response)
    return answers


if __name__ == '__main__':

    x1 = "请根据答案来源生成一篇50字左右的摘要"
    x2 = "请根据答案来源生成5个关键词,每个关键词之间用逗号隔开"
    x3 = "请根据答案来源生成一篇300词左右的总结，要求与摘要不同"
    # 获取 rid 列表
    rid = 22
    # 获取文本片段
    fragments = gettxt(rid)
    # 生成答案
    questions = [x1, x2, x3]
    abstract,keywords,summary = generate_answers(questions, fragments)

    # # 打印答案
    # for answer in answers:
    #     print(answer + "\n\n")
