# -*- coding: utf-8 -*-
# user = www
import os
import time
import logging
import HTMLTestRunnerNew
from common import contants
from common.read_config import ReadConfig

my_logger = logging.getLogger(ReadConfig().get("logs", "logger_name"))
my_logger.setLevel("DEBUG")

def set_handler(leves):
    if leves =='error':
        my_logger.addHandler(MyLog.error_handle)
    else:
        my_logger.addHandler(MyLog.handler)
    my_logger.addHandler(MyLog.ch)  # 全部输出到console
    my_logger.addHandler(MyLog.report_handler)  # 全部输出到report
def remove_handler(levels):
    if levels == 'error':
        my_logger.removeHandler(MyLog.error_handle)
    else:
        my_logger.removeHandler(MyLog.handler)

    my_logger.removeHandler(MyLog.ch)
    my_logger.addHandler(MyLog.report_handler)
def get_log_dir():
    log_dir = os.path.join(contants.logs_dir, get_current_day())
    if not os.path.join(log_dir):
        os.makedirs(log_dir)  # 不存在就创建
    return log_dir  # 存在就直接返回
def get_current_day():  # 获取当天
    return time.strftime('%Y%m%d', time.localtime(time.time()))

class MyLog:
    log_dir = get_log_dir()
    # 指定输出文件
    log_file = os.path.join(log_dir, 'info.log')
    error_file = os.path.join(log_dir, 'error.log')
    # 设置日志输出格式
    formatter = logging.Formatter('%(asctime)s-%(levelname)s-%(message)s')
    # 指定输出渠道
    # 控制台输出
    ch = logging.StreamHandler()
    ch.setLevel('DEBUG')
    ch.setFormatter(formatter)

    # INFO文件输出 自己扩展日志回滚
    handler = logging.FileHandler(filename=contants.logs_file, encoding='utf-8')
    handler.setLevel('INFO')
    handler.setFormatter(formatter)

    # 错误文件输出 自己扩展日志回滚
    error_handle = logging.FileHandler(filename=contants.error_file, encoding='utf-8')
    error_handle.setLevel('ERROR')
    error_handle.setFormatter(formatter)

    # 报表日志输出
    report_handler = logging.StreamHandler(HTMLTestRunnerNew.stdout_redirector)
    report_handler.setLevel('INFO')
    report_handler.setFormatter(formatter)

    @staticmethod
    def debug(msg):
        set_handler('debug')
        my_logger.debug(msg)
        remove_handler('debug')

    @staticmethod
    def info(msg):
        set_handler('info')
        my_logger.info(msg)
        remove_handler('info')

    @staticmethod
    def error(msg):
        set_handler('error')
        my_logger.error(msg, exc_info=True)  # 同时输出异常信息
        remove_handler('error')


if __name__ == '__main__':
    my_logger.error('error!!!!')
    # unittest.main()
    # try:
    #     raise AssertionError
    # except AssertionError as e:
    #     MyLog.error('error!!!!')


