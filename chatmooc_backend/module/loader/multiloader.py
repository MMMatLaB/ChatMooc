import os.path


def clean_text(text):
    return text.encode('utf-8', errors='replace').decode('utf-8')


def save_content(content, output_path):
    if not os.path.exists(os.path.dirname(output_path)):
        os.makedirs(os.path.dirname(output_path))
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(clean_text(content))



def load2Milvus(uid, doc_type, path):
    pass


import logging


def load(input_path, doc_type, output_path):
    # loader = None
    # logging.info(f"Loading file {file_name} from {path}")
    # doc_type = file_name.split(".")[-1]
    logging.info(f"Loading file {input_path}")
    content = []
    if doc_type == "txt":
        from langchain_community.document_loaders import TextLoader
        logging.info(f"Loading txt file {input_path}")
        loader = TextLoader(input_path, encoding="utf-8")
        for doc in loader.load():
            content.append(doc.page_content)
        content = "\n\n".join(content)
    elif doc_type == "pdf":
        from langchain_community.document_loaders import PyPDFLoader
        logging.info(f"Loading pdf file {input_path}")
        loader = PyPDFLoader(input_path)
        for doc in loader.load():
            content.append(doc.page_content)
        # print(loader.load())
        content = "\n\n".join(content)
    elif doc_type == "md":
        from langchain_community.document_loaders import UnstructuredMarkdownLoader
        loader = UnstructuredMarkdownLoader(input_path)
        for doc in loader.load():
            content.append(doc.page_content)
        content = "\n\n".join(content)
    elif doc_type == "mp4":
        logging.info(f"Loading video file {input_path}")
        content = video2text(input_path)
    save_content(content, output_path)
    # return content
    # print(content)


from moviepy.editor import *
import uuid
import whisper
import time

TEMP_DIR = r"E:\ChatMooc\chatmooc_backend\data\temp"


def video2text(path):
    if not os.path.exists(TEMP_DIR):
        os.makedirs(TEMP_DIR)
    video = VideoFileClip(path)
    file_name = str(uuid.uuid1()) + ".mp3"
    audio_path = os.path.join(TEMP_DIR, file_name)
    video.audio.write_audiofile(audio_path)
    # Record the start time
    logging.info("Loading the model")
    model = whisper.load_model("medium", download_root="../model")
    start_time = time.time()
    result = model.transcribe(audio_path, language="Chinese")
    # Specify Chinese recognition
    transcription = result["text"]  # Extract the transcribed text from the dictionary
    from zhconv import convert
    simplified_text = convert(transcription, 'zh-cn')
    # manually split the text
    end_time = time.time()
    # Calculate the elapsed time
    elapsed_time = end_time - start_time
    logging.info(f"Elapsed time: {elapsed_time} seconds")
    # print("Elapsed time:", elapsed_time, "seconds")
    return simplified_text


if __name__ == '__main__':
    load(r"E:\ChatMooc\chatmooc_backend\data\mock\test2.mp4", "mp4", os.path.join(TEMP_DIR, "test.txt"))
    # path = "E:\ChatMooc\chatmooc_backend\data\mock"
    # files=["test.pdf","test.txt","test.md"]
    # for file in files:
    #     load(file, path + "\\" + file)
    # load("3", "txt", "test.txt")
    # query("2", " what is the capital of india?")
