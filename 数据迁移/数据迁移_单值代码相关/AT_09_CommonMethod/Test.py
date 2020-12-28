# -*- coding: utf-8 -*-

# @Project : 数据迁移_单值代码相关
# @File    : Test.py
# @Date    : 2020-11-26
# @Author  : Administrator
# @Info    :

# a = [1,2,3,2,2,4,5]
# for i in a:
#     if i ==2:
#         a.remove(i)
# print(a)
import re
a = '10000'

y =re.search(r'\d+',a)
print(y.group())