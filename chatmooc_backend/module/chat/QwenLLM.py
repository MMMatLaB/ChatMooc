# 输入：文本x，章节号sid
import logging
import os

from langchain_community.embeddings import DashScopeEmbeddings
from langchain_community.llms import Tongyi
from langchain_core.prompts import PromptTemplate

from connectSQL.mysql_operate import db
from module.vectorDB.vectorstore import query_by_rid

# 调用mysql——输入：sid，输出所有rid
# 调用vectorstore——输入：rid，和,对应信息,返回文本片段
# 将x作为问题，文本片段内容作为答案来源 喂给大模型 得到输出

# 设置环境变量DASHSCOPE_API_KEY
# from chatmooc_backend.module.vectorDB.vectorstore import COLLECTION_NAME

os.environ["DASHSCOPE_API_KEY"] = 'sk-651aa47bea79499daf2f3014d4bdfa28'

# 初始化 DashScope 嵌入模型
embeddings = DashScopeEmbeddings(
    model="text-embedding-v1"
)

# 定义 Milvus 连接配置
CONNECTION_CONFIG = {"host": "127.0.0.1",
                     "port": "19530"}

llm = Tongyi()

# 定义提示模板
prompt_template = PromptTemplate(
    input_variables=["question", "context"],
    template="上下文：{context}\n\n请根据上下文，完成我的问题:[{question}],直接将答案输出即可\n\n"
)


# 定义从 MySQL 数据库获取 rid 的函数
def select_rid(mysid):
    sql = "SELECT rid FROM sectionhasresource WHERE sid=%s" % (mysid)
    results = db.select_db(sql)
    # data = []
    data = []
    for result in results:
        data.append(result['rid'])
    return data


# 从向量数据库中获取文本片段
def gettxt(data:list):
    fragments = []
    for rid in data:
        for i in query_by_rid(rid):
            fragment = i.page_content
            if fragment:
                fragments.append(fragment)
    return " ".join(fragments)


def get_context_byRid(rid):
    fragments = []
    for i in query_by_rid(rid):
        fragment = i.page_content
        if fragment:
            fragments.append(fragment)
    return " ".join(fragments)


# 初始化大模型


# 定义函数来生成答案
def generate_answer(question, context):
    prompt = prompt_template.format(question=question, context=context)
    response = llm(prompt)
    return response

def generateQA(sid):
    rid_list = select_rid(sid)
    # 获取文本片段
    fragments = gettxt(rid_list)
    question = "出一道题题目,包括问题和答案，2部分之间通过换行隔开，回复语言为中文，，严格按照输出格式:Q:xxxxxx\nA:xxxxxxx"
    # 生成答案
    Q,A = generate_answer(question, fragments).split('\n')
    Q = clean_text(Q)
    A = clean_text(A)
    return Q,A
def chat_with_llm(question, sid):
    # 获取 rid 列表
    rid_list = select_rid(sid)
    # 获取文本片段
    fragments = gettxt(rid_list)
    # 生成答案
    answer = generate_answer(question, fragments)
    return answer


def generate_answers(questions, context):
    answers = []
    for question in questions:
        prompt = prompt_template.format(question=question, context=context)
        response = llm(prompt)
        answers.append(response)
    return answers


def summary_generate(rid):
    x1 = "请根据上下文生成一篇50字左右的摘要(直接返回摘要内容，禁止以‘摘要：’开始,如果不满足要求则返回空字符串）"
    x2 = "请根据上下文生成5个关键词(从原文中选择关键词，关键词之间用逗号隔开,如果不满足要求则返回空字符串)"
    x3 = "请根据上下文生成一篇300词左右的总结(直接返回总结,如果不满足要求则返回空字符串)"
    # 获取 rid 列表
    # rid = 22
    # 获取文本片段
    fragments = get_context_byRid(rid)
    logging.info(f"fragments: {fragments}")
    # 生成答案
    questions = [x1, x2, x3]
    abstract, keywords, summary = generate_answers(questions, fragments)
    if abstract == "" or keywords == "" or summary == "":
        raise Exception("Failed to generate summary")
    abstract = clean_text(abstract)
    keywords = clean_text(keywords)
    summary = clean_text(summary)
    return abstract, keywords, summary


def clean_text(text:str):
    if "：" in text:
        return text.split("：")[1]
    if ":" in text:
        return text.split(":")[1]
    return text