# -*- coding: utf-8 -*-
# user = www
import configparser
import os
from common import contants
class ReadConfig:
    def __init__(self):
        self.cf = configparser.ConfigParser()
        file_name = os.path.join(contants.configs_dir, "global.conf")
        self.cf.read(filenames=file_name, encoding='utf-8')
        if self.cf.getboolean("switch", "on"):
            online = os.path.join(contants.configs_dir, "online.conf")
            self.cf.read(filenames=online, encoding='utf-8')
        else:
            test = os.path.join(contants.configs_dir, "test.conf")
            self.cf.read(filenames=test, encoding='utf-8')
    def get(self, sections, options):
        return self.cf.get(sections, options)
    def getboolean(self, sections, options):
        return self.cf.getboolean(sections, options)
    def getint(self, sections, options):
        return self.cf.getint(sections, options)


if __name__ == '__main__':
    t = ReadConfig()
    url_pre = t.get('api', 'url_pre')
    print(type(url_pre), url_pre)

