import requests

from tests.base_testcase import BaseTestCase


class TestLogin(BaseTestCase):

    def test_login(self):
        r = requests.get(
            'http://127.0.0.1:5000/testcase',
            headers={'Authorization': f'Bearer {self.token}'}
        )
        print(r.json())
        assert r.status_code == 200

    def test_testcase_get(self):
        r=requests.get(
            'http://127.0.0.1:5000/testcase'
        )
        print(r.json())
        assert r.status_code == 401



