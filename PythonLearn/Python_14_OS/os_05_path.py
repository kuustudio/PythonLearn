# -*- coding: utf-8 -*-

# @Project  : PythonLearn
# @File     : os_05_path.py
# @Date     : 2021-04-12
# @Author   : Administrator
# @Info     :
# @Introduce:
import os


def format_path(path):
    a = os.path.join()
    return a

# Python模块__all__变量
"""
也就是说，只有以“from 模块名 import *”形式导入的模块，当该模块设有 __all__ 变量时，
只能导入该变量指定的成员，未指定的成员是无法导入的。
"""


def say():
    print("人生苦短，我学Python！")


def CLanguage():
    print("C语言中文网：http://c.biancheng.net")


def disPython():
    print("Python教程：http://c.biancheng.net/python")


__all__ = ["say", "CLanguage"]
"""
#test.py
from demo import *
say()
CLanguage()
disPython()
在这种情况下 执行 disPython 函数报错 因为 不能引入该函数
"""
if __name__ == '__main__':
    path = "C:\\python"
    a = format_path(path)
    print(a)