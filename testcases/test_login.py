# -*- coding: utf-8 -*-
# user = www
import unittest
import json
from common import contants
from common.request import Request
from ddt import ddt, data
from common.do_excel import DoExcel

'''class TestLogin(unittest.TestCase):
    def setUp(self):
        print("开始测试")
    def tearDown(self):
        print("测试结束")
    def test_login(self):
        ww = DoExcel(contants.cases_path)
        cases = ww.get_cases('login')
        for case in cases:
            data = json.loads(case.data)
            res = Request(method=case.method, url=case.url, data=data)
            print(res.get_json())
            print(type(case.expected))
            try:
                self.assertEqual(eval(case.expected), res.get_json())
            except AssertionError as e:
                print("{} not found".format(e))
                raise e'''

ww = DoExcel(contants.cases_path)
cases = ww.get_cases('login')
@ddt
class TestLogin(unittest.TestCase):
    def setUp(self):
        print("开始测试")
    def tearDown(self):
        print("测试结束")
    @data(*cases)
    def test_login(self, case):  # 必须传输一条case
        data = json.loads(case.data)
        res = Request(method=case.method, url=case.url, data=data)
        print(res.get_json())
        try:
            self.assertEqual(eval(case.expected), res.get_json())
        except AssertionError as e:
            print("{} not found".format(e))
            raise e


if __name__ == '__main__':
    TestLogin().test_login()

