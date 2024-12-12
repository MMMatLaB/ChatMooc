import logging
from datetime import datetime

from flask import Blueprint, jsonify, request

from connectSQL.mysql_operate import db

chapter_blueprint = Blueprint('section', __name__)


@chapter_blueprint.route('/sections', methods=['GET'])
def select_chapter():
    print("111")
    sql = "SELECT sid,name,createtime FROM section"
    users = db.select_db(sql)

    response = {
        "code": 200,
        "data": users
    }
    return jsonify(response)


@chapter_blueprint.route('/section/<int:sid>', methods=['GET'])
def select_section(sid):
    print("111")
    sql = f"SELECT sid,name,createtime FROM section where sid = {sid}"
    row = db.select_db(sql)[0]

    response = {
        "code": 200,
        "data": {
            "sid": row['sid'],
            "name": row['name'],
            "createtime": row['createtime']
        }
    }
    return jsonify(response)


@chapter_blueprint.route('/section', methods=['POST'])
def insert_chapter():
    sname = request.json.get('sname')
    rids = request.json.get('rid')
    ownerid = 1
    createtime1 = datetime.now()
    createtime = createtime1.strftime('%Y-%m-%d %H:%M:%S')
    print("createtime", createtime)

    sql = f"INSERT INTO section (ownerid,name,createtime) VALUES ('{ownerid}', '{sname}','{createtime}')"
    result1 = db.execute_db(sql)
    sql2 = "SELECT sid FROM section ORDER BY sid DESC LIMIT 1"
    # sid = last_id_result[0][0].encode('utf-8').decode('utf-8')
    # 解析字符串为Python对象
    sid = db.select_db(sql2)[0]['sid']
    # new_sid_list = json.loads(new_sid)
    print(sid, "sid")
    for rid in rids:
        print(rid, "rid")
        sql1 = f"INSERT INTO sectionhasresource (rid, sid) VALUES ('{rid}', '{sid}')"
        print("sql1", sql1)
        result2 = db.execute_db(sql1)
    return jsonify({'message': result1 + result2})


@chapter_blueprint.route('/section/<int:id>', methods=['DELETE'])
def delete_chapter(id):
    # 从 URL 路径中直接获取 id 参数
    sql = f"DELETE FROM section WHERE sid = {id}"
    result = db.execute_db(sql)
    return jsonify({'message': result})


@chapter_blueprint.route('/section/<int:id>', methods=['PUT'])
def update_chapter(id):
    # 从请求体中获取新的章节内容
    name = request.json.get('sname')
    # print("name" + name)
    # print("id: " + str(id))
    # 使用从 URL 路径中获取的 id 来更新数据库中的记录
    sql = f"UPDATE section SET name = '{name}' WHERE sid = {id}"
    result = db.execute_db(sql)
    return jsonify({'message': result})


@chapter_blueprint.route('/section/<int:sid>/resource/<int:rid>', methods=['DELETE'])
def delete_sectionhasresource(sid, rid):
    # 从 URL 路径中直接获取 id 参数
    logging.info(f"DELETE sid: {sid}, rid: {rid}")
    sql = f"DELETE FROM sectionhasresource WHERE sid = {sid} AND rid = {rid}"
    result = db.execute_db(sql)
    return jsonify({'message': result})


@chapter_blueprint.route('/section/<int:sid>/resources', methods=['GET'])
def select_certain_resource(sid):
    sql2 = f"SELECT rid FROM sectionhasresource WHERE sid = {sid}"
    result = db.select_db(sql2)
    logging.info(f"result: {result}")
    resources = []
    if result:
        for rid in result:
            sql = f"SELECT rid, name, posterurl, type, updatetime, url, status,text FROM resource WHERE rid = {rid['rid']}"
            row = db.select_db(sql)[0]
            resource = {
                "rid": row['rid'],
                "name": row['name'],
                "posterurl": row['posterurl'],
                "type": row['type'],
                "updatetime": row['updatetime'],
                "url": row['url'],
                "status": row['status'],
                "text": row['text']

            }
            resources.append(resource)

    return jsonify({"code": 200, "data": resources}), 200


# addSubResource: (
#     sid: string,
# rid: number[],
# ) = > api.post('section/' + sid + '/resource', {
#     rid,
# }),
@chapter_blueprint.route('/section/<int:sid>/resource', methods=['POST'])
def add_sub_resource(sid):
    rids = request.json.get('rid')
    for rid in rids:
        sql = f"INSERT INTO sectionhasresource (rid, sid) VALUES ('{rid}', '{sid}')"
        result = db.execute_db(sql)
    return jsonify({'message': result})
