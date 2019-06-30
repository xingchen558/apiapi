# -*- coding: utf-8 -*-
# user = www
import json
import unittest
from common.basic_data import Context, DoRegex
from common import contants
from common.do_excel import DoExcel
from ddt import ddt, data
from common.mysql_util import MysqlUtil
from common.request import Request
from common.log_http import MyLog

ww = DoExcel(contants.cases_path)
cases = ww.get_cases('withdraw')
@ddt
class TestWithdraw(unittest.TestCase):
    def setUp(self):
        print("开始测试")
        self.mysql = MysqlUtil()
        self.sql = "select l.LeaveAmount from future.member l where l.MobilePhone ={}".format(Context.normal_user)
        self.start_amount = self.mysql.fetch_one(self.sql)['LeaveAmount']
    @data(*cases)
    def test_withdraw(self, case):
        my_logger = MyLog()
        my_logger.debug("执行第{}条案例".format(case.case_id))
        data = DoRegex.replace(case.data)
        data = json.loads(data)
        if hasattr(Context, 'cookies'):
            cookies = getattr(Context, 'cookies')
        else:
            cookies = None
        res = Request(method=case.method, url=case.url, data=data, cookies=cookies)
        if res.get_cookies():
            setattr(Context, 'cookies', res.get_cookies())
        my_logger.debug(res.get_json())
        try:
            self.assertEqual(case.expected, int(res.get_json()['code']))
        except AssertionError as e:
            my_logger.error("断言失败！")
            raise e
        if res.get_json()['msg'] == '取现成功':
            expected = float(self.start_amount) - float(data['amount'])
            actual = self.mysql.fetch_one(self.sql)['LeaveAmount']
            try:
                self.assertEqual(expected, actual)
            except AssertionError as e:
                raise e
        else:
            expected = float(self.start_amount)
            actual = self.mysql.fetch_one(self.sql)['LeaveAmount']
            self.assertEqual(expected, actual)

    def tearDown(self):
        self.mysql.close()
        print("测试结束")
if __name__ == '__main__':
    unittest.main()


