# -*- coding: utf-8 -*-

# @Project  : PythonLearn
# @File     : os_04_access.py
# @Date     : 2021-04-01
# @Author   : Administrator
# @Info     :
# @Introduce:
# os.access() 方法使用当前的uid/gid尝试访问路径。
# 大部分操作使用有效的 uid/gid, 因此运行环境可以在 suid/sgid 环境尝试。

import os


def access_dir():
    tmp = os.getcwd()
    can_find = os.access(tmp, os.F_OK) # 是否能找到
    can_read = os.access(tmp,os.R_OK) # 是否能读
    can_write = os.access(tmp,os.W_OK) # 是否能写
    can_x = os.access(tmp,os.X_OK)  #   是否可执行
    print(can_find)
    print(can_read)
    print(can_write)
    print(can_x)


if __name__ == '__main__':
    access_dir()
