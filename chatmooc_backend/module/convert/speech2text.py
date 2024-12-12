import whisper  # 导入whisper库，用于语音识别
import torch  # 导入torch库，用于深度学习模型

# 指定音频文件路径
path = r"E:\ChatMooc\data\3.1 问题提出：我在哪？.mp3"

# 加载预训练的Whisper模型，medium表示中等大小的模型，download_root指定模型下载的根目录
model = whisper.load_model("medium", download_root="../model")

import time  # 导入时间模块

# 记录开始时间
start_time = time.time()

# 对音频文件进行语音识别，指定识别语言为中文
result = model.transcribe(path, language="Chinese")

# 从识别结果字典中提取转录文本
transcription = result["text"]

from zhconv import convert  # 导入中文繁简转换模块

# 将转录文本转换为简体中文并写入文件
with open("result3.txt", "w", encoding="utf-8") as f:
    f.write(convert(transcription, 'zh-cn'))

end_time = time.time()

# 计算经过的时间
elapsed_time = end_time - start_time

print("Elapsed time:", elapsed_time, "seconds")