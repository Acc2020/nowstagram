import unittest,traceback, sys
from nowstagram import app


class NowstagramTest(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        self.app = app.test_client()
        print ('setUp')

    def tearDown(self):
        print ('teardown')
        pass

    def register(self, username, password):
        return self.app.post('/reg/', data={"username":username, "password":password}, follow_redirects=True)

    def login(self, username, password):
        return self.app.post('/login/', data={"username": username, "password": password}, follow_redirects=True)

    def logout(self):
        return self.app.get('/logout/')

    def test_reg_logout_login(self):
        try:
            assert self.register("hello", "world").status_code == 200
            #assert '-hello'.encode() in self.app.open('/').data
            self.logout()
            assert '-hello'.encode() not in self.app.open('/').data
            self.login("hello", "world")
            assert '-hello'.encode() in self.app.open('/').data
        except AssertionError:
            _, _, tb = sys.exc_info()
            traceback.print_tb(tb)  # Fixed format
            tb_info = traceback.extract_tb(tb)
            filename, line, func, text = tb_info[-1]
            print('An error occurred on line {} in statement {}'.format(line, text))


    def test_profile(self):
        try:
            r = self.app.open('/profile/3/', follow_redirects=True)
            assert r.status_code == 200
            assert "password".encode() in r.data
            self.register("hello2", "world")
            #assert "hello2".encode() in self.app.open('/profile/1/', follow_redirects=True).data
        except AssertionError:
            _, _, tb = sys.exc_info()
            traceback.print_tb(tb)  # Fixed format
            tb_info = traceback.extract_tb(tb)
            filename, line, func, text = tb_info[-1]
            print('An error occurred on line {} in statement {}'.format(line, text))

    # def test_1(self):.
    #     print('test1')
    #
    # def test_2(self):
    #     print('test2')
