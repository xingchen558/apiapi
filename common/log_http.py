# -*- coding: utf-8 -*-
# user = www
import logging
from common import contants
from common.read_config import ReadConfig

class MyLog:
    def my_log(self, level, msg):
        my_logger = logging.getLogger(ReadConfig().get('logs', 'logger_name'))
        my_logger.setLevel(ReadConfig().get('logs', 'logger_level'))
        formatter = logging.Formatter(ReadConfig().get('logs', 'formatter'))
        aa_handle = logging.StreamHandler()
        aa_handle.setLevel(ReadConfig().get('logs', 'handle_level'))
        bb_handle = logging.FileHandler(contants.logs_path, encoding='utf-8')
        bb_handle.setLevel(ReadConfig().get('logs', 'file_level'))
        aa_handle.setFormatter(formatter)
        bb_handle.setFormatter(formatter)
        my_logger.addHandler(aa_handle)
        my_logger.addHandler(bb_handle)
        if level == "DEBUG":
            my_logger.debug(msg)
        if level == "INFO":
            my_logger.info(msg)
        if level == "WARNING":
            my_logger.warning(msg)
        if level == "ERROR":
            my_logger.error(msg)
        if level == "CRITICAL":
            my_logger.critical(msg)

        my_logger.removeHandler(aa_handle)
        my_logger.removeHandler(bb_handle)
    def debug(self, msg):
        self.my_log("DEBUG", msg)
    def info(self, msg):
        self.my_log("INFO", msg)
    def warning(self, msg):
        self.my_log("WARNING", msg)
    def error(self, msg):
        self.my_log("ERROR", msg)
    def critical(self, msg):
        self.my_log("CRITICAL", msg)

if __name__ == '__main__':
    my_logger = MyLog()
    my_logger.debug(111)
    my_logger.info("asf安分点")
    my_logger.warning("用户如何")
    my_logger.error("发到手机号")
    my_logger.critical("合格方可")

