import unittest
import json
from unittest.mock import patch
from cumulus import Cumulus
from cumulus.base import Request, RequestError, InvalidData

TEST_URL = 'https://localhost:8765'
TEST_AUTH = ('cumulus', 'something')


class MockRequestBody:

    def __init__(self, body="") -> None:
        self.body = body


class MockRequest:

    def __init__(self,
                 url: str = TEST_URL,
                 status_code: int = 200,
                 reason: str = "",
                 text: str = "",
                 data: dict = {}) -> None:

        self.data = json.dumps(data) if isinstance(data, dict) else data
        # needed for custom Errors
        self.url = url
        self.status_code = status_code
        self.reason = reason
        self.text = text
        self.request = MockRequestBody()

    @property
    def ok(self):
        return bool(self.status_code < 400)

    def json(self):
        return json.loads(self.data)


class TestRequest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.api = Cumulus(url=TEST_URL, auth=TEST_AUTH)
        cls.request = Request(cls.api.url, cls.api.http_session)

    @patch(
        'requests.Session.request',
        return_value=MockRequest(status_code=500)
    )
    def test__send_request_status_code_failure(self, _):
        with self.assertRaises(RequestError):
            self.request._send_request(method="get")

    @patch(
        'requests.Session.request',
        return_value=MockRequest(data="invalid json")
    )
    def test__send_request_invalid_json(self, _):
        with self.assertRaises(InvalidData):
            self.request._send_request(method="post")

    @patch(
        'requests.Session.request',
        return_value=MockRequest(data={"key": "value"})
    )
    def test__send_request_success(self, _):
        response = self.request._send_request(method="get")
        self.assertIsInstance(response, dict)

    @patch(
        'cumulus.base.Request._send_request',
        return_value=dict()
    )
    def test_get(self, _):
        get = self.request.get()
        self.assertIsInstance(get, dict)

    @patch(
        'cumulus.base.Request._send_request',
        return_value=dict()
    )
    def test_post(self, _):
        post = self.request.post()
        self.assertIsInstance(post, dict)

    @patch(
        'cumulus.base.Request._send_request',
        return_value=dict()
    )
    def test_patch(self, _):
        patch = self.request.patch()
        self.assertIsInstance(patch, dict)

    @patch(
        'cumulus.base.Request._send_request',
        return_value=dict()
    )
    def test_delete(self, _):
        delete = self.request.delete()
        self.assertIsInstance(delete, dict)
