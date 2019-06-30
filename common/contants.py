# -*- coding: utf-8 -*-
# user = www

import os
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
configs_dir = os.path.join(base_dir, 'conf')
testcases_dir = os.path.join(base_dir, 'testcases')

read_path = os.path.join(configs_dir, 'read.conf')
global_path = os.path.join(configs_dir, 'global.conf')
online_path = os.path.join(configs_dir, 'online.conf')
test_path = os.path.join(configs_dir, 'test.conf')

datas_dir = os.path.join(base_dir, 'datas')
cases_path = os.path.join(datas_dir, 'test_cases.xlsx')
# print(cases_path)
report_path = os.path.join(os.path.join(base_dir, 'reports'), 'report1.html')
report_txt  = os.path.join(os.path.join(base_dir, 'reports'), 'report.txt')
print(report_path)
logs_path = os.path.join(os.path.join(base_dir, 'logs'), 'log.txt')

logs_dir = os.path.join(base_dir, 'logs')  # logs文件夹路径
logs_file = os.path.join(logs_dir, 'logs.log')  # logs文件夹路径
error_file = os.path.join(logs_dir, 'error.log')  # logs文件夹路径
testcases_dir = os.path.join(base_dir, 'testcases')  # logs文件夹路径
