# -*- coding: utf-8 -*-
# user = www
import HTMLTestRunnerNew
import unittest

from common import contants
from testcases.test_recharge import TestRecharge

# suite = unittest.TestSuite()
# loader = unittest.TestLoader()
# suite.addTest(loader.loadTestsFromTestCase(TestRecharge))

# with open(contants.report_txt, "w+") as file:
#     runner = unittest.TextTestRunner(stream=file, verbosity=2)
#     runner.run(suite)

discover = unittest.defaultTestLoader.discover(contants.testcases_dir, pattern='test*.py', top_level_dir=None)

with open(contants.report_path, 'wb') as file:
    runner = HTMLTestRunnerNew.HTMLTestRunner(stream=file,
                                              verbosity=2,
                                              title='充值测试',
                                              description='充值接口测试结果',
                                              tester='星辰')
    runner.run(discover)


