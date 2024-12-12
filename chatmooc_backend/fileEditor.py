import os.path
import pymysql

import uuid
from flask import Flask, request, send_file, jsonify
from flask_cors import CORS
from connectSQL.mysql_operate import db
from datetime import datetime
import os.path
import pymysql
from flask import Blueprint

file_blueprint = Blueprint('file', __name__)
PARSE_SAVE_PATH = 'data/parse/'
POSTER_SAVE_PATH = 'data/poster/'
FILE_SAVE_PATH = 'data/file/'
if not os.path.exists(POSTER_SAVE_PATH):
    os.makedirs(POSTER_SAVE_PATH)
if not os.path.exists(FILE_SAVE_PATH):
    os.makedirs(FILE_SAVE_PATH)


@file_blueprint.route('/file', methods=['POST'])
def upload():
    file = request.files['file']
    store_id = '.'.join([str(uuid.uuid1()), file.filename.split('.')[-1]])
    file.save(os.path.join(FILE_SAVE_PATH, store_id))
    # 从文件中截取poster
    name, ext = os.path.splitext(file.filename)
    # 删除后缀
    file_name = name.rstrip(ext)
    file_type = file.content_type
    if file_type not in ['video/mp4', 'application/pdf', 'text/plain']:
        return jsonify({
            "code": 400,
            "message": "Unsupported file type"
        })
    poster_store_id = store_id.replace(ext, '.jpg')
    if file_type == 'video/mp4':
        os.system(
            f'ffmpeg -i {os.path.join(FILE_SAVE_PATH, store_id)} -y -f image2 -t 0.001 -s 800x600 {os.path.join(POSTER_SAVE_PATH, poster_store_id)}')
    elif file_type == 'application/pdf':
        output_path = os.path.join(POSTER_SAVE_PATH, poster_store_id)
        input_path = os.path.join(FILE_SAVE_PATH, store_id)
        extract_cover(input_path, output_path)
    elif file_type == 'text/plain':
        output_path = os.path.join(POSTER_SAVE_PATH, poster_store_id)
        input_path = os.path.join(FILE_SAVE_PATH, store_id)
        w2p(input_path, output_path)

    url = "http://localhost:9999/file/" + store_id
    posterurl = "http://localhost:9999/poster/" + poster_store_id

    response = {
            "code": 200,
            "data": {
                # "rid": store_id,
                "url": url,
                "name": file_name,
                "type": file_type,
                "posterurl":posterurl
            }
        }

    return jsonify(response)


#
@file_blueprint.route('/parse/<filename>', methods=['GET'])
def get_parse(filename):
    # print(filename, "POSTER")
    # 前端使用el-upload组件上传音频文件，后端接收音频文件并返回给前端
    return send_file(os.path.join(PARSE_SAVE_PATH, filename))


@file_blueprint.route('/poster/<filename>', methods=['GET'])
def get_poster(filename):
    # print(filename, "POSTER")
    # 前端使用el-upload组件上传音频文件，后端接收音频文件并返回给前端
    return send_file(os.path.join(POSTER_SAVE_PATH, filename))


@file_blueprint.route('/file/<filename>', methods=['GET'])
def get_file(filename):
    # print(filename, "POSTER")
    # 前端使用el-upload组件上传音频文件，后端接收音频文件并返回给前端
    return send_file(os.path.join(FILE_SAVE_PATH, filename))


def extract_cover(pdf_path, output_path):
    import fitz
    doc = fitz.open(pdf_path)
    page = doc[0]
    zoom_x = 2.0
    zoom_y = 2.0
    trans = fitz.Matrix(zoom_x, zoom_y)
    pm = page.get_pixmap(matrix=trans, alpha=False)
    pm.save(output_path)
    pass


import textwrap
from PIL import Image, ImageDraw, ImageFont
import logging

def w2p(input_path, output_path):
    lines = []
    max_lines = 20
    line_width = 35

    # 逐行读取文件内容
    with open(input_path, 'r', encoding='utf-8') as f:
        for i in range(max_lines):
            line = f.readline()
            if not line:
                break
            # 将每行文本按照指定宽度换行
            wrapped_line = "\n".join(textwrap.wrap(line.strip(), width=line_width))
            lines.append(wrapped_line)

    # 将处理后的文本拼接成一个字符串
    text = "\n".join(lines)

    # 获取文字列表的最大字符数量
    max_len = max(len(line) for line in text.split("\n"))

    # 转换文字为图片并保存为图片
    line_height = 26
    h = line_height * len(text.split("\n")) + 10
    w = int(max_len * 19.5 + 10)

    # 限制图片的最大尺寸
    max_dim = 65500
    if h > max_dim or w > max_dim:
        ratio = min(max_dim / h, max_dim / w)
        h = int(h * ratio)
        w = int(w * ratio)

    try:
        im = Image.new("RGB", (w, h), (255, 255, 255))
        dr = ImageDraw.Draw(im)
        fpath = r'E:\ChatMooc\chatmooc_backend\static\font\msyh.ttf'
        font = ImageFont.truetype(fpath, 20)
        dr.text((5, 5), text, font=font, fill="#000000")

        im.save(output_path)
    except OSError as e:
        logging.error(f"Error saving image: {e}")
        raise


@file_blueprint.route('/resources', methods=['GET'])
def select_resource():
    # 构建参数化 SQL 查询语句
    sql = "SELECT rid, name, posterurl, type, updatetime, url, status,text FROM resource"
    result = db.select_db(sql)
    resources = []
    if result:
        for row in result:
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


@file_blueprint.route('/resource', methods=['POST'])
def post_resource():
    # 获取请求数据
    url = request.json.get('url')
    posterurl = request.json.get('posterurl')
    ownerid = request.json.get('uid')
    name = request.json.get('name')
    type = request.json.get('type')
    updatetime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    status = 0

    # 构建参数化 SQL 语句
    sql = """
        INSERT INTO resource (name, type, updatetime, ownerid, url, status, posterurl)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """
    params = (name, type, updatetime, ownerid, url, status, posterurl)

    # 执行 SQL 语句
    try:
        result = db.execute_db(sql, params)
        return jsonify({
            "code": 200,
            "data": result
        })
    except Exception as e:
        logging.error(f"Error inserting resource: {e}")
        return jsonify({
            "code": 500,
            "message": "Internal server error"
        }), 500

@file_blueprint.route('/resource/<int:rid>', methods=['DELETE'])
def delete_resource(rid):
    sql = f"DELETE FROM resource WHERE rid = {rid}"
    result = db.execute_db(sql)
    return jsonify({'message': result})


@file_blueprint.route('/resource/<int:rid>', methods=['PUT'])
def update_resource(rid):
    name = request.json.get('name')
    sql = f"UPDATE resource SET name = '{name}' WHERE rid = {rid}"
    result = db.execute_db(sql)
    return jsonify({'message': result})


@file_blueprint.route('/resource/<int:rid>', methods=['GET'])
def get_resource(rid):
    sql = f"SELECT rid, name, posterurl, type, updatetime, url, status,text FROM resource WHERE rid = {rid}"
    result = db.select_db(sql)
    if result:
        resource = {
            "rid": result[0]['rid'],
            "name": result[0]['name'],
            "posterurl": result[0]['posterurl'],
            "type": result[0]['type'],
            "updatetime": result[0]['updatetime'],
            "url": result[0]['url'],
            "status": result[0]['status'],
            "text": result[0]['text']
        }
        return jsonify({"code": 200, "data": resource}), 200
    else:
        return jsonify({"code": 404, "message": "Resource not found"}), 404

# /resource/{rid}/parse
@file_blueprint.route('/resource/<int:rid>/parse', methods=['POST'])
def parse_resource(rid):
    # 获取资源的 URL
    sql = f"SELECT url FROM resource WHERE rid = {rid}"
    result = db.select_db(sql)
    if not result:
        return jsonify({"code": 404, "message": "Resource not found"}), 404
    url = result[0]['url']
    file_path = os.path.join(FILE_SAVE_PATH, url.split('/')[-1])
    # 根据资源类型调用不同的解析函数
    from module.loader.multiloader import load
    doc_type = url.split('.')[-1]
    output_path = os.path.join(PARSE_SAVE_PATH, f"{uuid.uuid1()}.txt")
    db.execute_db(f"UPDATE resource SET status = 3 WHERE rid = {rid}")
    load(file_path, doc_type,output_path)
    from module.vectorDB.vectorstore import load2milvus
    load2milvus(rid, output_path)
    text_url = "http://localhost:9999/parse/" + output_path.split('/')[-1]
    # 更新资源的 text 字段
    sql = f"UPDATE resource SET text = '{text_url}' WHERE rid = {rid}"
    db.execute_db(sql)

    sql2 = f"SELECT rid, name, posterurl, type, updatetime, url, status,text FROM resource WHERE rid = {rid}"
    result = db.select_db(sql2)
    db.execute_db(f"UPDATE resource SET status = 1 WHERE rid = {rid}")
    if result:
        resource = {
            "rid": result[0]['rid'],
            "name": result[0]['name'],
            "posterurl": result[0]['posterurl'],
            "type": result[0]['type'],
            "updatetime": result[0]['updatetime'],
            "url": result[0]['url'],
            "status": result[0]['status'],
            "text": result[0]['text']
        }
        return jsonify({"code": 200, "data": resource}), 200
    else:
        return jsonify({"code": 404, "message": "Resource not found"}), 404