import os

# 设置环境变量，存储讯飞语音技术的应用ID、API密钥、API密钥秘钥以及API URL
os.environ["IFLYTEK_SPARK_APP_ID"] = "3f9db013"
os.environ["IFLYTEK_SPARK_API_KEY"] = "6dafe3a2735d5b7af739f0a233b10dd0"
os.environ["IFLYTEK_SPARK_API_SECRET"] = "NWFmY2UzYzliNWI0ODg2ZmY2YTNmYjZi"
os.environ["IFLYTEK_SPARK_API_URL"] = "wss://spark-api.xf-yun.com/v1.1/chat"

# 导入需要使用的模块
from langchain_community.llms import SparkLLM
from langchain_core.prompts import PromptTemplate

# 创建一个SparkLLM对象
llm = SparkLLM()

# 定义一个问题模板，模板中包含一个占位符{question}，稍后会被实际的问题替换
template = """Question: {question}
Answer: Let's think step by step."""

# 使用PromptTemplate从模板中创建一个PromptTemplate对象
prompt = PromptTemplate.from_template(template)

# 创建一个链，将问题模板和SparkLLM对象组合起来
chain = prompt | llm

# 准备要提问的问题
question = "What NFL team won the Super Bowl in the year Justin Bieber was born?"

# 调用链的invoke方法，并传入包含问题的字典作为参数
res = chain.invoke({"question": question})

# 打印生成的答案结果
print(res)