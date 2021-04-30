# -*- coding: utf-8 -*-

# @Project  : PythonLearn
# @File     : os_03_removedirs.py
# @Date     : 2021-04-01
# @Author   : Administrator
# @Info     : 递归删除目录
# @Introduce:
"""
os.removedirs() 方法用于递归删除目录。
像rmdir(), 如果子文件夹成功删除,
removedirs()才尝试它们的父文件夹,直到抛出一个error(它基本上被忽略,因为它一般意味着你文件夹不为空)。
"""
"""
使用方法
    os.removedirs(path)
    path -- 要移除的目录路径
    
"""