# -*- coding: utf-8 -*-
# user = www
import unittest
import json
from common.log_http import MyLog
from common import contants
from common.request import Request
from ddt import ddt, data
from common.do_excel import DoExcel
from common.mysql_util import MysqlUtil

ww = DoExcel(contants.cases_path)
cases = ww.get_cases('register')
@ddt
class TestRegister(unittest.TestCase):
    def setUp(self):
        print("开始测试")
        self.mysql = MysqlUtil()
        self.sql = "select l.MobilePhone from future.member l where l.MobilePhone !='' " \
                   "order by l.MobilePhone desc limit 1"
        self.max_phone = self.mysql.fetch_one(self.sql)['MobilePhone']  # ['MobilePhone']

    def tearDown(self):
        self.mysql.close()
        print("测试结束")
    @data(*cases)
    def test_register(self, case):  # 必须传输一条case
        data = json.loads(case.data)
        if data['mobilephone'] == '${register}':
            data['mobilephone'] = str(int(self.max_phone) + 1)
            print(data)
        res = Request(method=case.method, url=case.url, data=data)
        print(res.get_json())
        self.assertEqual(str(case.expected), res.get_json()['code'])
        # 数据库数据校验
        sql = "select l.MobilePhone from future.member l where l.MobilePhone ={}".format(int(self.max_phone) + 1)
        # print(sql)
        expected = int(self.max_phone) + 1
        member = self.mysql.fetch_one(sql)
        if member is not None:
            self.assertEqual(expected, member['MobilePhone'])

if __name__ == '__main__':
    unittest.main()



