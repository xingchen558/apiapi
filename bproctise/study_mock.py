# -*- coding: utf-8 -*-
# user = www
from unittest import mock
import unittest
from bproctise.study_payment import Payment
# 前段和后端的条用
# 单元测试  unittest方法测试
# 第三方接口的依赖
'''# assert_called(*args,**kwargs) 判断该方法至少被调用一次
assert_called_once(*args,**kwargs) 判断该方法 只 被调用一次
assert_called_with(*args,**kwargs) 判断该方法调用时使用了正确的参数
assert_called_once_with(*args,**kwargs) 判断该方法使用参数且只调用一次
assert_any_call(*args,**kwargs) 判断mock对象被调用过
assert_has_calls(calls,any_order=False) 判断多次被调用
assert_not_called(*args,**kwargs) 从未被调用
called: mock对象是否被调用
call_count ： 被调用几次
call_args ： 获取最近被调用时的参数
call_args_list ：获取工厂调用时的所有参数
method_calls ：测试当前mock对象都调用了那些
'''
class PaymentTest(unittest.TestCase):
    def setUp(self):
        print("开始测试")
        self.payment = Payment()
    def testSuccess(self):
        # 模拟 payment requestOutofSystem的返回值是200 # 不需要括号
        self.payment.requestOutofSystem = mock.Mock(return_value=200)
        res = self.payment.dopay(user_id=1, card_num="123456", amount=100)
        self.assertEqual('success', res, "支付成功！")
        self.payment.requestOutofSystem.assert_called_once_with("123456", 100)
    def testFail(self):
        # mock 模拟 一个方法，方法名：requestOutofSystem
        self.payment.requestOutofSystem = mock.Mock(return_value=500)
        res = self.payment.dopay(user_id=2, card_num='12345678', amount=1000000)
        self.assertEqual('fail', res, "支付失败！")
    def testRetrySuccess(self):  # 先超时在成功
        # 模拟 payment requestOutofSystem的返回值 返回超时  # side_effect必须是可迭代对象
        self.payment.requestOutofSystem = mock.Mock(return_value=500,  # 不起作用
                                                    side_effect=[TimeoutError, 200])
        res = self.payment.dopay(user_id=3, card_num='123456789', amount=100)
        self.assertEqual('success', res, "支付成功！")
        print("模拟对象是否被调用", self.payment.requestOutofSystem.called)
        print("模拟对象被调用次数", self.payment.requestOutofSystem.call_count)
        print("最近被调用的参数", self.payment.requestOutofSystem.call_args)
        self.payment.requestOutofSystem.assert_called("123456789", 100)
    def testRetryFail(self):
        self.payment.requestOutofSystem = mock.Mock(side_effect=[TimeoutError, 500])
        res = self.payment.dopay(user_id=4, card_num='1234567890', amount=100)
        self.assertEqual('fail', res, "支付失败！")
        print("模拟对象是否被调用", self.payment.requestOutofSystem.called)
        print("模拟对象被调用次数", self.payment.requestOutofSystem.call_count)
        print("最近被调用的参数", self.payment.requestOutofSystem.call_args)
    def tearDown(self):
        print("测试结束！")

