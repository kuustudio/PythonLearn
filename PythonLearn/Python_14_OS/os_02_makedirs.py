# -*- coding: utf-8 -*-

# @Project  : PythonLearn
# @File     : os_02_makedirs.py
# @Date     : 2021-03-31
# @Author   : Administrator
# @Info     :
# @Introduce:

import os, sys

# 创建的目录
path = "/tmp/home/monthly/daily"
os.makedirs(path,0o755,exist_ok=False)
# 如果exist_ok是False（默认），当目标目录（即要创建的目录）已经存在，会抛出一个OSError。
# 如果 byte 则需要在 定义变量时候 b''
"""
           if isinstance(p, bytes):
            sep = b'\\'
            altsep = b'/'
            colon = b':'
        else:
            sep = '\\'
            altsep = '/'
            colon = ':'
        normp = p.replace(altsep, sep)
"""

"""
os.makedir:
    参数 path  权限
    调用
        
    详细链路
    # 创建的目录
path = "/tmp/home/monthly/daily"
os.makedirs(path,0o755,exist_ok=False)
使用 字符串切割的方法 切割传过来的参数 之后调用os.makedir 递归创建目录
"""
