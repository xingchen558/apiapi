# -*- coding: utf-8 -*-
# user = www
import unittest
import json
from common.request import Request
from common import contants
from ddt import ddt,data
from common.mysql_util import MysqlUtil
from common.do_excel import DoExcel
from common.basic_data import Context, DoRegex

ww = DoExcel(contants.cases_path)
cases = ww.get_cases('bidLoan')

@ddt
class TestBidLoan(unittest.TestCase):
    def setUp(self):
        print("开始测试")
        self.mysql = MysqlUtil()
        self.sql = "select * from future.member where MobilePhone ={}".format(Context.normal_user)
        self.start_amount = self.mysql.fetch_one(self.sql)['LeaveAmount']
    @data(*cases)
    def test_bidLoan(self, case):
        data = DoRegex.replace(case.data)
        data = json.loads(data)
        print("执行第{}条案例".format(case.case_id))
        if hasattr(Context, 'cookies'):
            cookies = getattr(Context, 'cookies')
        else:
            cookies = None
        res = Request(method=case.method, url=case.url, data=data, cookies=cookies)
        print(res.get_json())
        if res.get_cookies():
            setattr(Context, 'cookies', res.get_cookies())

        if res.get_json()['msg'] == "竞标成功":
            expect = float(self.start_amount) - float(data['amount'])
            actual = self.mysql.fetch_one(self.sql)['LeaveAmount']
            try:
                self.assertEqual(expect, actual)  # 一直报错，实际值不正确，数据库数据没有变化 ？？？
                print(expect)
                print(actual)
            except Exception as e:
                print("投标成功断言失败！")
                raise e
        else:
            expect = float(self.start_amount)
            actual = self.mysql.fetch_one(self.sql)['LeaveAmount']
            try:
                self.assertEqual(expect, actual)
                print(expect)
                print(actual)
            except Exception as e:
                print("投标失败断言失败！")
                raise e

    def tearDown(self):
        self.mysql.close()
        print("结束测试")
if __name__ == '__main__':
    unittest.main()


