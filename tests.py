import unittest
from nowstagram import app


class NowstagramTest(unittest.TestCase):
    def setUp(self):
        print(' setup')
        app.config['TESTING'] = True
        self.app = app.test_client()

    # def setUpClass(cls):
    #     print('setupClass')

    def tearDown(self):
        print('tearDown')

    # def tearDownClass(cls):
    #     print('tearDownClass')

    def register(self, username, password):
        return self.app.post('/reg/', data={"username": username, "password": password}, follow_redirects=True)

    def login(self, username, password):
        return self.app.post('/login/', data={"username": username, "password": password}, follow_redirects=True)

    def logout(self):
        return self.app.get('/logout/')

    def test_reg_login_logout(self):
        assert self.register("hello", "hello").status_code == 200

    # def test_1(self):
    #     print('test1')
    #
    # def test_2(self):
    #     print('test2')
