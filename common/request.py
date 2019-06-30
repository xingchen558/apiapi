# -*- coding: utf-8 -*-
# user = www
import requests
from common.read_config import ReadConfig
class Request:
    def __init__(self, method, url, data, cookies=None, headers=None):
        try:
            config = ReadConfig()
            url_pre = config.get('api', 'url_pre')
            url = url_pre + url  # 拼接请求地址
            if method == 'get':
                self.res = requests.get(url=url, data=data, cookies=cookies, headers=headers)
            elif method == 'post':
                self.res = requests.post(url=url, data=data, cookies=cookies, headers=headers)
            else:
                self.res = requests.delete(url=url, data=data, cookies=cookies, headers=headers)
        except Exception as e:
            print("执行出错{}".format(e))
            raise e

    def get_status_code(self):
        return self.res.status_code
    def get_text(self):
        return self.res.text
    def get_json(self):
        return self.res.json()
    def get_cookies(self):
        return self.res.cookies


if __name__ == '__main__':
    t = Request('post', 'http://test.lemonban.com/futureloan/mvc/api/member/login',
                {"mobilephone": "13555556666", "pwd": "123456"})
    print(t.get_json())
