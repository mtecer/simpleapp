from __future__ import print_function
from dateutil import parser
from flask import Flask, request
from pymongo import MongoClient

import datetime
import hashlib
import json


app = Flask(__name__)


def store_post(record):
    """Save data in mongodb.
    Adds a single document to mongodb
    """
    connection = MongoClient('127.0.0.1', 27017)
    db = connection.simpleapp
    collection = db.records
    collection.insert_one(record).inserted_id
    connection.close()


def verify_md5(j):
    """Verify md5 checksum of submitted data.
    Builds data dict to run md5 against
    data is converted to json object before md5 checksum is run
    md5 checksum match returns data dict
    """
    data = {}
    data['date'] = j.get('date')
    data['uid'] = j.get('uid')
    data['name'] = j.get('name')

    data_json = json.dumps(data)
    data_json_md5 = hashlib.md5(data_json).hexdigest()

    if data_json_md5 == j.get('md5checksum'):
        data['date'] = parser.parse(j.get('date'))
        return data
    else:
        return False


@app.route('/post', methods=['POST'])
def post():
    """POST endpoint.
    Acceps a json list and compares data with md5checksum supplied
    If md5 checksum matches record is sent to be stored in mongodb
    """
    json_list = request.get_json()

    for record in json_list:
        md5_check = verify_md5(record)
        if md5_check:
            store_post(md5_check)
    return "Completed\n"


@app.route('/query', methods=['GET'])
def get():
    """GET endpoint.
    Requires uid and date parameters to search for a match in mongodb
    Missing parameters trigger graceful message and 405
    """
    requested_uid = request.args.get('uid')
    requested_date = request.args.get('date')

    if (not requested_uid) or (not requested_date):
        return "Simpleapp requires uid and date as parameters", 405

    """Building day start and end objects for mongodb search here"""
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

    """Reports occurences of a searched data"""
    return "There are {} occurences of uid={} on {}\n".format(
        count, requested_uid, requested_date)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)
