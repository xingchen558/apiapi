# -*- coding: utf-8 -*-
# user = www
import re
from common.read_config import ReadConfig
class DoRegex:
    @staticmethod
    def replace(target):
        pattern = '\$\{(.*?)\}'
        while re.search(pattern, target):  # 找到一个就match
            m = re.search(pattern, target)
            key = m.group(1)  # 区第一个分组里面的字符，就替换
            user = getattr(Context, key)
            target = re.sub(pattern, user, target, count=1)
        return target

class Context:
    config = ReadConfig()
    normal_user = config.get("basic", "normal_user")  # 类变量
    normal_pwd = config.get("basic", "normal_pwd")
    admin_user = config.get("basic", "admin_user")  # 类变量
    admin_pwd = config.get("basic", "admin_pwd")
    loan_member_id = config.get("basic", "loan_member_id")
    normal_member_id = config.get("basic", "normal_member_id")

    loan_id = config.get("basic", "loan_member_id")
    loan_member_id_1 = config.get("basic", "loan_member_id_1")

if __name__ == '__main__':
    # DoRegex.replace()
    t = getattr(Context, 'admin_user')
    setattr(Context, 'loan_id', 7941)
    # setattr(Context, 'admin_user', '333')
    a = getattr(Context, 'loan_id')
    print(type(a))
    # if hasattr(Context, 'a'):
    #     delattr(Context, 'a')
    # else:
    #     print("没有这个属性，不执行删除")


