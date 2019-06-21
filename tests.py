import unittest
from nowstagram import app


class NowstagramTest(unittest.TestCase):
    def setUp(self):
        print('setup')

    # def setUpClass(cls):
    #     print('setupClass')

    def tearDown(self):
        print('tearDown')

    # def tearDownClass(cls):
    #     print('tearDownClass')

    def test_1(self):
        print('test1')

    def test_2(self):
        print('test2')
