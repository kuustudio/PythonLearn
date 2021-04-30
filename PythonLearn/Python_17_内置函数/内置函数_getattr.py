# -*- coding: utf-8 -*-

# @Project  : PythonLearn
# @File     : 内置函数_getattr.py
# @Date     : 2021-04-12
# @Author   : Administrator
# @Info     : getattr() 函数用于返回一个对象属性的值。返回对象属性值。
# @Introduce: getattr(object, name[, default])
class A(object):
    bar = 1
    def __init__(self):
        """vvv"""
        self.test = "test"
        pass
    def __str__(self):
        pass
    def __repr__(self):
        pass
a = A()
b = getattr(a, '__init__')# 获取属性 bar 值
print(b.__doc__)
c = dir(a)
print(c)
# getattr(a, 'bar2')       # 属性 bar2 不存在，触发异常


getattr(a, 'bar2', 3)    # 属性 bar2 不存在，但设置了默认值
