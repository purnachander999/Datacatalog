import unittest
import requests

class TestAPI(unittest.TestCase):
    URL = "http://localhost:5000"

    login_data = {
        "username": "abcd12",
        "password": "abcd12"
    }
    def test_1_get_all(self):
        resp  = requests.get(self.URL)
        self.assertEqual(resp.status_code, 404)

    def test_2_register_user(self):
        resp = requests.post(self.URL + "/register", json=self.login_data)
        self.assertEqual(resp.status_code, 201)


    def test_3_register_failed(self):
        resp = requests.post(self.URL + "/register", json=self.login_data)
        self.assertEqual(resp.status_code, 409)

    def test_4_login(self):
        resp = requests.post(self.URL+"/login", json = self.login_data )
        self.assertEqual(resp.status_code, 200)

# if __name__ == "__main__":
#     tester = TestAPI()
#     tester.test_1_get_all()
#     tester.test_login()