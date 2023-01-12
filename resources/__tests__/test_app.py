import unittest
from flask import Flask, jsonify
from app import create_app
app = Flask(__name__)

from app import create_app
@app.route('/')
def hello_world():
    return jsonify({'message': 'Hello, World!'})


class MyTestCase(unittest.TestCase):
    def setUp(self):
        app.testing = True
        self.client = app.create_app()

    def test_hello_world(self):
        response = self.client.get('/')
        data = response.get_json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['message'], 'Hello, World!')


if __name__ == '__main__':
    unittest.main()