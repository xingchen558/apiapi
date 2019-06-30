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

# ww = DoExcel(contants.cases_path)
# cases = ww.get_cases('invest')
# @ddt
# class TestInvest(unittest.TestCase):
#     def setUp(self):
#         print("开始测试")
#         self.mysql = MysqlUtil()
#         self.select_member = 'select * from future.member where mobilephone = {0}'.format(Context.normal_user)
#         self.before_amount = self.mysql.fetch_one(self.select_member)['LeaveAmount']
#
#     @data(*cases)
#     def test_login(self, case):  # 必须传输一条case
#         my_logger = MyLog()
#         data = DoRegex.replace(case.data)  # 首先从excel中取出来，然后做正则
#         data = json.loads(data)  # 然后在loads
#         if hasattr(Context, 'cookies'):  # 第一次登陆没有cookies，所以要判断
#             # 参数化处理
#             cookies = getattr(Context, 'cookies')
#         else:
#             cookies = None
#         res = Request(method=case.method, url=case.url, data=data, cookies=cookies)
#         print(res.get_text())
#         res_dict = res.get_json()
#         print(res_dict)
#         self.assertEqual(case.expected, int(res_dict['code']))
#         print(int(res_dict['code']))
#         if res.get_cookies():
#             setattr(Context, 'cookies', res.get_cookies())
#         if res_dict['msg'] == '加标成功':
#             select_loan = 'select*from future.loan where memberId={} order by ' \
#                           'createtime desc'.format(Context.loan_member_id)
#             loan = self.mysql.fetch_one(select_loan)
#             print(loan)
#             if loan is not None:
#                 self.assertEqual(data['amount'], loan['Amount'])
#                 setattr(Context, 'loan_id', str(loan['Id']))  # 要正则处理，所以必须是字符串 (object, name, value)
#                 print('loan_id')
#             else:
#                 raise AssertionError
#         # if res_dict['msg'] == '审核成功':
#         #     select_type = 'select status from future.loan where memberId={}'.format(Context.loan_member_id)
#         #     self.assertEqual(4, int(select_type))
#         if res_dict['msg'] == '竞标成功':
#             amount = data['amount']  # 投资金额
#             actual = self.mysql.fetch_one(self.select_member)['LeaveAmount']
#             expect = float(self.before_amount) - float(amount)  # 期望=投资前-投资后
#             self.assertEqual(expect, actual)
#         elif res_dict['code'] != '10001':
#             actual = self.mysql.fetch_one(self.select_member)['LeaveAmount']
#             expect = float(self.before_amount)
#             self.assertEqual(expect, actual)
#
#     def tearDown(self):
#         print("测试结束")
#         print("--------------------------------------")

do_excel = DoExcel(contants.cases_path)  # 实例化一个DoExcel对象
cases = do_excel.get_cases('invest')

@ddt
class InvestTest(unittest.TestCase):

    def setUp(self):
        self.mysql = MysqlUtil()
        # 投资前账户余额
        self.select_member = 'select * from future.member where mobilephone = {0}'.format(Context.normal_user)
        self.before_amount = self.mysql.fetch_one(self.select_member)['LeaveAmount']
        # 自己去添加
        pass

    @data(*cases)
    def test_invest(self, case):
        # 参数化处理
        data = DoRegex.replace(case.data)
        # 将测试数据由字符串序列化成字典
        data = json.loads(data)
        if hasattr(Context, 'cookies'):  # 判断是否有cookies
            cookies = getattr(Context, 'cookies')  # 获取放到上下文里面的cookies
        else:
            cookies = None
        # 通过封装的Request类来完成接口的调用
        resp = Request(method=case.method, url=case.url, data=data, cookies=cookies)
        print(resp.get_text())
        resp_dict = resp.get_json()  # 获取请求响应，字典
        # 优先判断响应返回的code 是否与期望结果一致
        self.assertEqual(case.expected, int(resp_dict['code']))
        # 判断有没有cookie
        if resp.get_cookies():  # 判断返回里面是否有cookies
            setattr(Context, 'cookies', resp.get_cookies())  # 放入到上下文中
        # 当创建标的成功时，根据借款人ID查看数据库loan表是否与添加数据
        if resp_dict['msg'] == '加标成功':
            select_loan = 'select * from future.loan where memberId = {0} order by createtime desc limit 1'.format(Context.loan_member_id)
            loan = self.mysql.fetch_one(select_loan)
            if loan is not None:  # 如果从数据库里面查询出来不是空，则创建标的成功
                # 判断数据库里面的标的详情是否与测试数据一致
                self.assertEqual(data['amount'], loan['Amount'])  # 多个字段一致才assert通过
                # 其他的自己加
                # 将创建成功的标的ID写入到上下文中，用于之后投资用
                setattr(Context, 'loan_id', str(loan['Id']))  # 放一个str类型的进去，以备后面正则替换
            else:
                raise AssertionError  # 如果数据库里面没有数据，就测试失败
        # 当审核成功，需校验数据库loan表中status字段更改，自己添加
        # 当投资成功时，根据投资人ID查看数据member表中验证余额是否减少
        if resp_dict['msg'] == '竞标成功':
            amount = data['amount']  # 投资金额
            actual = self.mysql.fetch_one(self.select_member)['LeaveAmount']  # 投资后的金额
            expect = float(self.before_amount) - float(amount)  # 期望 = 投资前的余额 - 投资金额
            self.assertEqual(expect, actual)
        elif resp_dict['code'] != '10001':  # 投资失败，余额不变
            actual = self.mysql.fetch_one(self.select_member)['LeaveAmount']  # 投资后的金额
            expect = float(self.before_amount)  # 期望 = 投资前的余额
            self.assertEqual(expect, actual)

    def tearDown(self):
        self.mysql.close()
        pass
if __name__ == '__main__':
    unittest.main()

