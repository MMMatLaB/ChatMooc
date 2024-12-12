from datetime import datetime

from flask import Blueprint, jsonify, request

from connectSQL.mysql_operate import db

folder_blueprint = Blueprint('folder', __name__)


@folder_blueprint.route('/cardfolder/<int:fid>/cards', methods=['GET'])
def select_card_from_folder(fid):
    logging.info(f"Fetching cards for folder ID: {fid}")

    try:
        # Assuming db is your database connection object
        db.connect()  # Connect to the database
    except Exception as e:
        logging.error(f"Error connecting to the database: {e}")
        return jsonify({"code": 500, "message": "Internal Server Error"}), 500

    # Create an empty list to store the final formatted cards
    formatted_cards = []

    # SQL query to select the relevant card details
    sql = f"SELECT cid, type, question, answer, status FROM card WHERE fid = '{fid}'"

    try:
        cards = db.select_db(sql)
    except Exception as e:
        logging.error(f"Error fetching cards for folder ID {fid}: {e}")
        # db.close()  # Close the database connection
        return jsonify({"code": 500, "message": "Internal Server Error"}), 500

    logging.debug("Raw cards data:", cards)

    if cards:
        for card in cards:
            # Ensure all required keys are present in the card dictionary
            if all(k in card for k in ('cid', 'type', 'question', 'answer', 'status')):
                formatted_card = {
                    "cid": card['cid'],
                    "question": {
                        "type": card['type'],
                        "content": card['question']
                    },
                    "answer": card['answer'],
                    "status": card['status']
                }
                formatted_cards.append(formatted_card)
            else:
                logging.warning("Card missing required keys:", card)

    response = {
        "code": 200,
        "data": formatted_cards
    }

    logging.info("Fetched cards for folder ID successfully")

    # db.close()  # Close the database connection
    return jsonify(response)


@folder_blueprint.route('/cardfolder', methods=['POST'])
def insert_cardfolder():
    fname = request.json.get('fname')
    sid = request.json.get('sid')
    createtime1 = datetime.now()
    createtime = createtime1.strftime('%Y-%m-%d')
    sql = f"INSERT INTO cardfolder (fname,createtime,sid) VALUES ('{fname}','{createtime}','{sid}')"
    print(sql)
    result = db.execute_db(sql)
    return jsonify({'message': result})


@folder_blueprint.route('/cardfolder/<int:fid>', methods=['PUT'])
def update_cardfolder(fid):
    fname = request.json.get('fname')
    sql = f"UPDATE cardfolder SET fname= '{fname}' WHERE fid='{fid}'"
    print(sql)
    result = db.execute_db(sql)
    return jsonify({'message': result})


@folder_blueprint.route('/cardfolder/<int:fid>', methods=['DELETE'])
def delete_card(fid):
    # 从 URL 路径中直接获取 id 参数
    sql = f"DELETE FROM cardfolder WHERE fid = {fid}"
    result = db.execute_db(sql)
    return jsonify({'message': result})


@folder_blueprint.route('/cardfolders', methods=['GET'])
def select_allfolder():
    logging.info("Fetching all card folders")

    try:
        # Assuming db is your database connection object
        db.connect()  # Connect to the database
    except Exception as e:
        logging.error(f"Error connecting to the database: {e}")
        return jsonify({"code": 500, "message": "Internal Server Error"}), 500

    sql = "SELECT fid, fname, createtime, sid FROM cardfolder"
    logging.debug(f"SQL Query: {sql}")

    try:
        folderinfo_list = db.select_db(sql)
    except Exception as e:
        logging.error(f"Error fetching folder info: {e}")
        db.close()  # Close the database connection
        return jsonify({"code": 500, "message": "Internal Server Error"}), 500

    folders = []

    for folderinfo in folderinfo_list:
        fid = folderinfo['fid']
        fname = folderinfo['fname']
        createtime = folderinfo['createtime']
        sid = folderinfo['sid']

        logging.debug(f"Processing folder ID: {fid}, Name: {fname}")

        try:
            sql1 = f"SELECT status, COUNT(*) as count FROM card WHERE fid = '{fid}' AND status IN (0, 1, 2) GROUP BY status;"
            logging.debug(f"SQL Query: {sql1}")
            card_stats = db.select_db(sql1)
        except Exception as e:
            logging.error(f"Error fetching card stats for folder ID {fid}: {e}")
            card_stats = []

        try:
            sql2 = f"SELECT name FROM section WHERE sid='{sid}'"
            logging.debug(f"SQL Query: {sql2}")
            sname = db.select_db(sql2)
            name = sname[0]['name'] if sname else "Unknown"
        except Exception as e:
            logging.error(f"Error fetching section name for SID {sid}: {e}")
            name = "Unknown"

        section = {
            "sid": sid,
            "name": name
        }

        statistics = {str(stat['status']): stat['count'] for stat in card_stats}
        for status in [0, 1, 2]:
            if str(status) not in statistics:
                statistics[str(status)] = 0

        formatted_folder = {
            "fid": fid,
            "name": fname,
            "statistics": statistics,
            "createtime": createtime,
            "section": section
        }

        folders.append(formatted_folder)

    response = {
        "code": 200,
        "data": folders
    }
    logging.info("Fetched all card folders successfully")

    # db.close()  # Close the database connection
    return jsonify(response)


import logging


@folder_blueprint.route('/cardfolder/<int:fid>', methods=['GET'])
def select_certainfolder(fid):
    logging.info(f"Fetching folder details for folder ID {fid}")

    try:
        # Connect to the database
        db.connect()

        # Retrieve folder information
        sql = f"SELECT fname, sid FROM cardfolder WHERE fid = '{fid}'"
        folder_info = db.select_db(sql)

        if not folder_info:
            logging.warning(f"Folder with ID {fid} not found")
            return jsonify({"code": 404, "message": "Folder not found"}), 404

        fname = folder_info[0]['fname']
        sid = folder_info[0]['sid']

        # Retrieve section name
        sql2 = f"SELECT name FROM section WHERE sid = '{sid}'"
        section_info = db.select_db(sql2)

        if not section_info:
            logging.warning(f"Section with SID {sid} not found")
            return jsonify({"code": 404, "message": "Section not found"}), 404

        section_name = section_info[0]['name']

        formatted_folder = {
            "fname": fname,
            "sname": section_name
        }

        response = {"code": 200, "data": formatted_folder}
        logging.info("Folder details fetched successfully")
        return jsonify(response)

    except Exception as e:
        logging.error(f"Error fetching folder details for folder ID {fid}: {e}")
        return jsonify({"code": 500, "message": "Internal Server Error"}), 500
