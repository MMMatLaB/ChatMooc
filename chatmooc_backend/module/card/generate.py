from datetime import datetime, timezone, timedelta
# from pprint import pprint
from fsrs import *

f = FSRS()


# 他这套逻辑是utc+0的，所以我这里要转换成utc+0
def parser_utc8(utc_time):
    # type datatime
    return utc_time.replace(tzinfo=timezone.utc).astimezone(timezone(timedelta(hours=8))).replace(tzinfo=None)

# Rating.Again # forget; incorrect response
# Rating.Hard # recall; correct response recalled with serious difficulty
# Rating.Good # recall; correct response after a hesitation
# Rating.Easy # recall; perfect response


# card = Card()
# # (py-fsrs cards use UTC)
# now = datetime.now(datetime.now().astimezone().tzinfo).replace(tzinfo=None)
# # card = f.repeat(card, now)
# # print(type(card.due))
# print(parser_utc8(card.due))
# print(f.repeat(card, now))
# Rating.Again # forget; incorrect response
# Rating.Hard # recall; correct response recalled with serious difficulty
# Rating.Good # recall; correct response after a hesitation
# Rating.Easy # recall; perfect response
# card = f.repeat(card, now)
# card = card[Rating.Good].card
# print(parser_utc8(card.due))
def now_utc():
    return datetime.now(datetime.now().astimezone().tzinfo).replace(tzinfo=None)


if __name__ == '__main__':
    card = Card() # 创建一个新卡片
    schedule_info = f.repeat(card, now_utc()) # 重复一次
    new_card = schedule_info[Rating.Hard].card # 选择了good
    print(parser_utc8(new_card.due)) # 打印出来
    print(card.scheduled_days)



