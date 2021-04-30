# -*- coding: utf-8 -*-

# @Project  : PythonLearn
# @File     : 内置函数_dir.py
# @Date     : 2021-04-12
# @Author   : Administrator
# @Info     : dir ir() 函数不带参数时，返回当前范围内的变量、方法和定义的类型列表；带参数时，返回参数的属性、方法列表。
# 如果参数包含方法__dir__()，
# 该方法将被调用。如果参数不包含__dir__()，该方法将最大限度地收集参数信息。
# @Introduce:
print(dir())
print(dir({}))