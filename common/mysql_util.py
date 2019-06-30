# -*- coding: utf-8 -*-
# user = www
# 1：连接数据库  2：编写sql  3：建立游标  4：执行

import pymysql
from common.read_config import ReadConfig
class MysqlUtil:
    def __init__(self):
        config = ReadConfig()
        host = config.get('mysql', 'host')
        user = config.get('mysql', 'usr')
        password = config.get('mysql', 'pwd')
        port = config.getint('mysql', 'port')
        try:
            self.mysql = pymysql.connect(host=host, user=user, password=password,
                                         port=port, cursorclass=pymysql.cursors.DictCursor)
            # cursorclass=pymysql.cursors.DictCursor 要求返回字典格式
        except Exception as e:
            print("报错：{}".format(e))
            raise e
    def fetch_one(self, sql):
        cursor = self.mysql.cursor()  # 返回的数据是元组
        cursor.execute(sql)
        return cursor.fetchone()
    def close(self):
        self.mysql.close()


if __name__ == '__main__':
    sql = " select * from future.loan where id ='6666';"
    mysql = MysqlUtil()
    s = mysql.fetch_one(sql)['Id']
    print(type(s))
    print(s)
