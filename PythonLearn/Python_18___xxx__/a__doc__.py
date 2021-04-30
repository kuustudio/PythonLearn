# -*- coding: utf-8 -*-

# @Project  : PythonLearn
# @File     : a__doc__.py
# @Date     : 2021-04-12
# @Author   : Administrator
# @Info     :
# @Introduce: __doc__：获取到注释内容 注意注释为 多行注释内容
def test():
    """测试__doc__"""
    c = 4
    return c
a= test()
print(a.__doc__)
