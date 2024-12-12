import logging

from flask import Blueprint, jsonify

from connectSQL.mysql_operate import db

LLM_blueprint = Blueprint('LLM', __name__)

from module.chat.QwenLLM import summary_generate


@LLM_blueprint.route('/generatecontent/<int:rid>', methods=['GET'])
def get_generatecontent(rid):
    sql = "SELECT  abstract, keyword, summary FROM gc WHERE rid=%s" % (rid)
    results = db.select_db(sql)
    # = generate_answers(rid)
    if not results:
        return jsonify({
            "code": 404,
            "msg": "gc not found"
        })
    abstract = results[0]['abstract']
    keywords = results[0]['keyword'].split(',')
    summary = results[0]['summary']
    return jsonify({
        "code": 200,
        "data": {
            "abstract": abstract,
            "keywords": keywords,
            "summary": summary
        }
    })


# ('resource/'+rid+'generatecontent')
@LLM_blueprint.route('/resource/<int:rid>/generatecontent', methods=['POST'])
def generatecontent(rid):
    logging.info(f"Generating content for rid {rid}")
    try:
        abstract, keywords, summary = summary_generate(str(rid))
        logging.info(f"a:{abstract}, k:{keywords}, s:{summary}")
        sql = "INSERT INTO gc (rid, abstract, keyword, summary) VALUES (%s, %s, %s, %s)"
        data = (rid, abstract, keywords, summary)
        db.execute_db(sql, data)
    except Exception as e:
        logging.error(f"Generate content failed: {e}")
        return jsonify({
            "code": 500,
            "msg": "Generate content failed"
        })
    return jsonify({
        "code": 200,
        "msg": "success"
    })


# getAnswer: (
#   sid: string,
#   question: string,
# ) => api.post('section/' + sid + '/answer',
#   {
#     question
#   }),
from module.chat.QwenLLM import chat_with_llm
from flask import request


@LLM_blueprint.route('/section/<int:sid>/answer', methods=['POST'])
def getAnswer(sid):
    logging.info(f"Getting answer for sid {sid}")
    # logging.info(f"")
    # question :object
    question = request.json.get('question')
    role = question['role']
    name = question['name']
    avatar = question['avatar']
    content = question['content']
    sql = f"INSERT INTO message (sid, role, name, avatar, content) VALUES ('{sid}', '{role}', '{name}', '{avatar}', '{content}')"
    db.execute_db(sql)
    answer = chat_with_llm(question, sid)
    role = "ai"
    name = "Qwen"
    avatar = "https://img.alicdn.com/imgextra/i4/O1CN01FOwagl1XBpyVA2QVy_!!6000000002886-2-tps-512-512.png"
    sql = f"INSERT INTO message (sid, role, name, avatar, content) VALUES ('{sid}', '{role}', '{name}', '{avatar}', '{answer}')"
    db.execute_db(sql)
    return jsonify({
        "code": 200,
        "data": {
            "role": role,
            "name": name,
            "avatar": avatar,
            "content": answer
        }
    })


@LLM_blueprint.route('/section/<int:sid>/messages', methods=['GET'])
def getMessages(sid):
    logging.info(f"Getting messages for sid {sid}")
    sql = f"SELECT * FROM message WHERE sid = {sid}"
    result = db.select_db(sql)
    messages = []
    if result:
        for row in result:
            message = {
                "mid": row['mid'],
                "sid": row['sid'],
                "role": row['role'],
                "name": row['name'],
                "avatar": row['avatar'],
                "content": row['content'],
            }
            messages.append(message)
    return jsonify({"code": 200, "data": messages}), 200


from module.chat.QwenLLM import generateQA


@LLM_blueprint.route('/cardfolder/<int:fid>/QA', methods=['GET'])
def getQA(fid):
    sql2 = f"SELECT sid FROM cardfolder WHERE fid = {fid}"
    result = db.select_db(sql2)
    sid = result[0]['sid']
    logging.info(f"Getting QA for sid {sid}")
    Q, A = generateQA(sid)
    return jsonify({"code": 200, "data":
        {
            "question": Q,
            "answer": A
        }}), 200
