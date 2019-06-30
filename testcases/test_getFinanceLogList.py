# -*- coding: utf-8 -*-
# user = www
import unittest
import json
from common.log_http import MyLog
from common import contants
from common.request import Request
from ddt import ddt, data
from common.do_excel import DoExcel
from common.basic_data import DoRegex, Context
from common.mysql_util import MysqlUtil

ww = DoExcel(contants.cases_path)
cases = ww.get_cases('getFinanceLogList')

@ddt
class TestGetFinanceLogList(unittest.TestCase):
    def setUp(self):
        print("开始测试")
        self.mysql = MysqlUtil()
        pass
    def tearDown(self):
        self.mysql.close()
        print("测试结束")
        print("--------------------------------------")

    @data(*cases)
    def test_getFinanceLogListd(self, case):  # 必须传输一条case
        my_logger = MyLog()
        data = DoRegex.replace(case.data)  # 首先从excel中取出来，然后做正则
        data = json.loads(data)  # 然后在loads
        if hasattr(Context, 'cookies'):  # 第一次登陆没有cookies，所以要判断
            cookies = getattr(Context, 'cookies')
        else:
            cookies = None
        res = Request(method=case.method, url=case.url, data=data, cookies=cookies)
        # 判断有没有cookies
        if res.get_cookies():
            setattr(Context, 'cookies', res.get_cookies())
        my_logger.debug(res.get_json())
        try:
            self.assertEqual(str(case.expected), res.get_json()['code'])
        except AssertionError as e:
            my_logger.error("断言失败")
            raise e
        resp_dict = res.get_json()
        if resp_dict['msg'] == '获取用户流水记录成功！':
            my_logger.debug("获取用户流水记录成功！")
if __name__ == '__main__':
    unittest.main()

