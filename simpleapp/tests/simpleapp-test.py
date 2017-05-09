import json
import sys
import unittest

sys.path.insert(0, '/usr/local/python/simpleapp')

from pymongo import MongoClient
from simpleapp import app

get_route_params = 'uid=3&date=2017-05-08'
nonexisting_record = 'uid=2&date=2015-05-13'
payload = [
    {'date': '2015-05-12T14:36:00.451765', 'uid': '1', 'name': 'John Doe',
        'md5checksum': 'e8c83e232b64ce94fdd0e4539ad0d44f'},
    {'date': '2015-05-13T14:36:00.451765', 'uid': '2', 'name': 'Jane Doe',
        'md5checksum': 'b419795d50db2a35e94c8364978d898f'},
    {'date': '2017-05-08T19:24:37.681036', 'uid': '3', 'name': 'Liam Campbell',
        'md5checksum': '3d3eb30464eff0f785bc4da8fffad915'},
    {'date': '2017-05-08T19:24:37.681036', 'uid': '4', 'name': 'Adam Murphy',
        'md5checksum': 'a05baf98e7a2ca496339a86c508ab2e5'},
    {'date': '2017-05-08T19:24:37.681036', 'uid': '5', 'name': 'Jenson King',
        'md5checksum': '1ffde47a01000e7bc48674b2dac45d1d'},
    {'date': '2017-05-08T19:24:37.681036', 'uid': '6', 'name': 'Max Mason',
        'md5checksum': '9653db9b41fb9b9cc7ad3fb5125aaf02'},
    {'date': '2017-05-08T19:24:37.681036', 'uid': '7', 'name': 'Corey Morris',
        'md5checksum': 'fd5f79e91af249de523cf419b270c13e'},
    {'date': '2017-05-08T19:24:37.681036', 'uid': '8', 'name': 'Tristen Daugherty',
        'md5checksum': 'c17368689b478a7fae49669b5fee6fc3'},
    {'date': '2017-05-08T19:24:37.681036', 'uid': '9', 'name': 'Jared Puckett',
        'md5checksum': 'd8879c836c35987ff3344b8114ac0dcc'},
    {'date': '2017-05-08T19:24:37.681036', 'uid': '10', 'name': 'Reed Graham',
        'md5checksum': 'a58779b9fe772c7cb8d8378e269b205e'},
    {'date': '2017-05-08T19:24:37.681036', 'uid': '11', 'name': 'Trace Dixon',
        'md5checksum': '4831dfba0ad9e54c018c9eec5ae4dae9'},
    {'date': '2017-05-08T19:24:37.681036', 'uid': '12', 'name': 'Nicolas Small',
        'md5checksum': '5241b2b9bb54be2fa32f5c1f6f1d166b'},
]


class SimpleAppTest(unittest.TestCase):

    global get_route_params, nonexisting_record, payload

    def test_empty_query(self):
        """GET call to /query without parameters.
        Succeeds
        """
        tester = app.test_client(self)
        response = tester.get('/query', content_type='html/text')
        self.assertEqual(response.status_code, 405)
        self.assertEqual(response.data, u'Simpleapp requires uid and date as parameters')

    def test_root_route(self):
        """GET call to / should generate 404
        Succeeds
        """
        tester = app.test_client(self)
        response = tester.get('/', content_type='html/text')
        self.assertEqual(response.status_code, 404)

    def test_query_route(self):
        """GET call to /query for existing record.
        Succeeds
        """
        tester = app.test_client(self)
        response = tester.get('/query', query_string=get_route_params, content_type='html/text')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, u'There are 1 occurences of uid=3 on 2017-05-08\n')

    def test_query_route_nonexisting(self):
        """GET call to /query for a nonexisting record.
        Succeeds
        """
        tester = app.test_client(self)
        response = tester.get('/query', query_string=nonexisting_record, content_type='html/text')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, u'There are 0 occurences of uid=2 on 2015-05-13\n')

    def test_post_route(self):
        """POST call to /post.
        Succeeds
        """
        tester = app.test_client(self)
        response = tester.post('/post', data=json.dumps(payload), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, u'Completed\n')

    @staticmethod
    def cleanup():
        """Clean up test records in MongoDB"""
        connection = MongoClient('127.0.0.1', 27017)
        db = connection.simpleapp
        collection = db.records
        collection.remove({})
        connection.close()

    @classmethod
    def tearDownClass(cls):
        cls.cleanup()


if __name__ == '__main__':
    unittest.main()
