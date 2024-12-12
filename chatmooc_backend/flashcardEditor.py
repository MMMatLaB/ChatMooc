from datetime import datetime, timedelta, timezone

from fsrs import Rating, FSRS, Card

from connectSQL.mysql_operate import db
from flask import Blueprint, jsonify, request

card_blueprint = Blueprint('card', __name__)


# 获取某个卡片
@card_blueprint.route('/card/<int:cid>', methods=['GET'])
def select_card(cid):
    print("111")
    sql = f"SELECT cid, type, question, answer, status FROM card WHERE cid = '{cid}'"
    card = db.select_db(sql)
    print("caa" + str(card))

    if not card:
        return jsonify({"code": 404, "message": "Card not found"})

    formatted_card = {
        "cid": card[0]['cid'],
        "question": {
            "type": card[0]['type'],
            "content": card[0]['question']
        },
        "answer": card[0]['answer'],
        "status": card[0]['status']
    }

    response = {
        "code": 200,
        "data": formatted_card
    }
    return jsonify(response)


@card_blueprint.route('/card', methods=['POST'])
def insert_card():
    question = request.json.get('question')
    answer = request.json.get('answer')
    type = request.json.get('type')
    # sid = request.json.get('sid')
    fid = request.json.get('fid')
    createtime1 = datetime.now()
    createtime = createtime1.strftime('%Y-%m-%d')
    nextTime = createtime1.strftime('%Y-%m-%d %H:%M:%S')
    status = 0
    sql = f"INSERT INTO card (question,answer,nextTime,createtime,type,status,fid) VALUES ('{question}', '{answer}','{nextTime}','{createtime}','{type}','{status}','{fid}')"
    print(sql)
    result = db.execute_db(sql)

    return jsonify({'message': result})


@card_blueprint.route('/card/<int:cid>', methods=['PUT'])
def update_card(cid):
    # 从请求体中获取新的章节内容
    question = request.json.get('question')
    print(str(question)+"question")
    question1=question["content"]
    print(str(question1)+"question1")
    answer = request.json.get('answer')
    print(answer)
    # print("name" + name)
    print("cid: " + str(cid))
    # 使用从 URL 路径中获取的 id 来更新数据库中的记录
    sql = f"UPDATE card SET question = '{question1}',answer='{answer}' WHERE cid = {cid}"
    result = db.execute_db(sql)
    return jsonify({'message': result})


@card_blueprint.route('/card/<int:cid>', methods=['DELETE'])
def delete_card(cid):
    # 从 URL 路径中直接获取 id 参数
    sql = f"DELETE FROM card WHERE cid = {cid}"
    result = db.execute_db(sql)
    return jsonify({'message': result})


f = FSRS()


def parser_utc8(utc_time):
    return utc_time.replace(tzinfo=timezone.utc).astimezone(timezone(timedelta(hours=8))).replace(tzinfo=None)


def now_utc():
    return datetime.now(datetime.now().astimezone().tzinfo).replace(tzinfo=None)


@card_blueprint.route('/card/<int:cid>/score', methods=['POST'])
def score_card(cid):
    # print("111111")
    # 从请求体中获取新的章节内容
    score = request.json.get('score')
    # print(str(score)+"ssssss")
    if score == 1:
        rating = Rating.Hard
    elif score == 2:
        rating = Rating.Good
    elif score == 3:
        rating = Rating.Easy
    else:
        rating = Rating.Again
    print("cid: " + str(cid))
    sql = f"SELECT nextTime FROM card WHERE cid='{cid}'"
    # lastTime1=db.select_db(sql)
    # lastTime=lastTime1[0]['nextTime']
    card = Card()
    now = now_utc()
    card = f.repeat(card, now)
    new_card = card[rating].card
    new_due_utc8 = parser_utc8(new_card.due)
    print(new_due_utc8)
    nextTime = new_due_utc8.strftime("%Y-%m-%d %H:%M:%S")
    print(nextTime)

    # scheduleddays = (new_due_utc8 - now).days
    # nextTime = lastTime + scheduleddays
    # 使用从 URL 路径中获取的 id 来更新数据库中的记录
    sql = f"UPDATE card SET nextTime = '{nextTime}' WHERE cid = '{cid}'"
    result = db.execute_db(sql)
    sql1 = f"UPDATE card SET status= 1 WHERE cid = '{cid}' "
    result1 = db.execute_db(sql1)
    return jsonify({'message': result + " " + result1})


def compare_time(time_str1, time_str2):
    time_format = "%Y-%m-%d %H:%M:%S"
    time1 = datetime.strptime(time_str1, time_format)
    time2 = datetime.strptime(time_str2, time_format)
    print(time1,"  ", time2)

    if time1 < time2:
        return 1
    else:
        return 0

import logging
from datetime import datetime
@card_blueprint.route('/cardfolder/<int:fid>/cards/study', methods=['GET'])
def statu_card(fid):
    logging.info(f"Retrieving cards for folder ID {fid} with status 2")

    try:
        # Connect to the database
        db.connect()

        # Get the current datetime
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Update the status of cards whose nextTime has passed
        sql_update_status = f"UPDATE card SET status = 2 WHERE nextTime <= '{now}' AND status <> 2"
        db.execute_db(sql_update_status)

        # Retrieve the cards with status 2 for the given folder ID
        sql_select_cards = f"SELECT cid, type, question, answer, status FROM card WHERE fid = '{fid}' AND status = 2"
        cards_info = db.select_db(sql_select_cards)

        # Format the retrieved cards
        formatted_cards = []
        for card_info in cards_info:
            formatted_card = {
                "cid": card_info['cid'],
                "question": {
                    "type": card_info['type'],
                    "content": card_info['question']
                },
                "answer": card_info['answer'],
                "status": card_info['status']
            }
            formatted_cards.append(formatted_card)

        response = {"code": 200, "data": formatted_cards}
        logging.info("Retrieved cards for folder ID successfully")
        return jsonify(response)

    except Exception as e:
        logging.error(f"Error retrieving cards for folder ID {fid}: {e}")
        return jsonify({"code": 500, "message": "Internal Server Error"}), 500

    # finally:
        # Close the database connection
        # db.close()

