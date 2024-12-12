path =r"E:\ChatMooc\data\3.1 问题提出：我在哪？.mp4"
from moviepy.editor import *
import uuid
video = VideoFileClip(path)
video.audio.write_audiofile(path.replace(".mp4", ".mp3"))