import unittest
import requests
import random
import string

class TestAPI(unittest.TestCase):
    URL = "http://localhost:5000"

    login_data = {
        "username": "test",
        "password": "test123"
    }
    random_string = ''.join(random.choices(string.ascii_uppercase +
                                 string.digits, k=7))

    main_store = {
        "name": "Annual sales report",
        "description": "For year 2022-23"
    }

    def test_1_register_user(self):
        resp = requests.post(self.URL + "/register", json=self.login_data)
        self.assertEqual(resp.content, b'{"message":"user created sucessully"}\n')
        self.assertEqual(resp.status_code, 201)

    def test_2_register_failed(self):
        resp = requests.post(self.URL + "/register", json=self.login_data)
        self.assertEqual(resp.status_code, 409)

    def test_3_login(self):
        resp = requests.post(self.URL+"/login", json = self.login_data )
        print(resp)
        self.assertEqual(resp.status_code, 200)

    def test_4_create_main_store(self):
        resp = requests.post(self.URL + "/mainstore", json=self.main_store)
        self.assertEqual(resp.status_code, 201)

    def test_4_create_main_store_to_fail(self):
        resp = requests.post(self.URL + "/mainstore", json=self.main_store)
        self.assertEqual(resp.status_code, 400)

    def test_4_create_meta_store(self):
        resp = requests.post(self.URL + "/metastore", json=self.main_store)
        self.assertEqual(resp.status_code, 201)


