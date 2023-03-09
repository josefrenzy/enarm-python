import unittest
import json

from rest_srv import app


class TestAuth(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()

    def test_successfull_login(self):
        payload = json.dumps({
            "username": "guzmangordillojose@icloud.com",
            "password": "123Pesos$"
        })
        response = self.app.post(
            '/auth/signin',
            headers={"Content-Type": "application/json"},
            data=payload)
        self.assertEqual(
            str, type(response.json['AuthenticationResult']['AccessToken']))
        self.assertEqual(200, response.status_code)
