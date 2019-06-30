# -*- coding: utf-8 -*-
# user = www

import re
from common.read_config import ReadConfig
from common.basic_data import Context

s = '{"mobilephone":"${normal_user}","pwd":"${pwd}"}'
p = '\$\{(.*?)\}'

m = re.search(p, s)
print(m.group())
print(m.group(1))
key = m.group(1)
user = getattr(Context, key)
print(user)
s = re.sub(p, user, s, count=1)
print(s)






