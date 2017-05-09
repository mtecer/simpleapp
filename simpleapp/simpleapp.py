from __future__ import print_function
from dateutil import parser
from flask import Flask, request
from pymongo import MongoClient

import datetime
import hashlib
import json

app = Flask(__name__)


def store_post(record):
    connection = MongoClient('127.0.0.1', 27017)
    db = connection.simpleapp
    collection = db.records
    collection.insert_one(record).inserted_id
    connection.close()


def verify_md5(j):
    data = {}
    data['date'] = j.get('date')
    data['uid'] = j.get('uid')
    data['name'] = j.get('name')

    data_json = json.dumps(data)
    data_json_md5 = hashlib.md5(data_json).hexdigest()

    if data_json_md5 == j.get('md5checksum'):
        data['date'] = parser.parse(j.get('date'))
        data['md5checksum'] = j.get('md5checksum')
        return data
    else:
        return False


@app.route('/post', methods=['POST'])
def post():
    json_list = request.get_json()

    for record in json_list:
        md5_check = verify_md5(record)
        if md5_check:
            print("Passed md5 checksum: {}".format(record))
            store_post(md5_check)
        else:
            print("Failed md5 checksum: {}".format(record))
    return "Completed\n"


@app.route('/query', methods=['GET'])
def get():
    requested_uid = request.args.get('uid')
    requested_date = request.args.get('date')

    daterange_start = parser.parse(requested_date)
    daterange_end = daterange_start + datetime.timedelta(days=1)

    connection = MongoClient('127.0.0.1', 27017)
    db = connection.simpleapp
    collection = db.records
    count = collection.count({
        "uid": requested_uid,
        "date": {"$gte": daterange_start, "$lt": daterange_end}
        })

    connection.close()

    return "There are {} occurences of uid={} on {}\n".format(
        count, requested_uid, requested_date)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080, debug=True)
