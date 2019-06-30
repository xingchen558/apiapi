# -*- coding: utf-8 -*-
# user = www

import json
import unittest
from common.basic_data import Context, DoRegex
from common import contants
from common.do_excel import DoExcel
from ddt import ddt, data
from common.request import Request
from common.log_http import MyLog
ww = DoExcel(contants.cases_path)
cases = ww.get_cases('list')
@ddt
class TestList(unittest.TestCase):
    def setUp(self):
        print("开始测试")
    @data(*cases)
    def test_list(self, case):
        my_logger = MyLog()
        if case.data != None:
            data = DoRegex.replace(case.data)  # 正则调用，替换正则表达式的数据
            data = json.loads(data)
            if hasattr(Context, 'cookies'):
                cookies = getattr(Context, 'cookies')
            else:
                cookies = None
            res = Request(method=case.method, url=case.url, data=data, cookies=cookies)
            print(res.get_json())
            if res.get_cookies():
                setattr(Context, 'cookies', res.get_cookies())
        else:  # data为空，所以输入None，打印第一个data中的数据
            if hasattr(Context, 'cookies'):
                cookies = getattr(Context, 'cookies')
            else:
                cookies = None
            res = Request(method=case.method, url=case.url, data=None, cookies=cookies)
            print(res.get_json()['data'][0])
            if res.get_json()['code'] == '10001':
                print("获取列表成功")
            else:
                print("获取列表失败")

    def tearDown(self):
        print("结束测试")
if __name__ == '__main__':
    unittest.main()
