# -*- coding: utf-8 -*-

# @Project  : PythonLearn
# @File     : dg_01_test.py
# @Date     : 2021-05-07
# @Author   : Administrator
# @Info     :
# @Introduce:


def recursion(n):
    v = n//2 # 地板除，保留整数
    print(v) # 每次求商，输出商的值
    if v==0:
        ''' 当商为0时，停止，返回Done'''
        return 'Done'
    v = recursion(v) # 递归调用，函数内自己调用自己


recursion(10) # 函数调用
