# -*- coding: utf-8 -*-

# @Project  : PythonLearn
# @File     : os_01_replace.py
# @Date     : 2021-03-31
# @Author   : Administrator
# @Info     :
# @Introduce:
"""
os.replace:
    参数 old ,new
    调用
        import os
        os.replace('1.txt','2.txt')
    详细链路
    import os
    os.remove('2.txt')
    os.rename('1.txt', '2.txt')

    重命名文件或目录，覆盖目标。

如果src_dir_fd或dst_dir_fd不是None，那么它应该是一个文件
打开到一个目录的描述符，以及相应的路径字符串(src或dst)
应该是相对的;然后，路径将相对于该目录。
src_dir_fd和dst_dir_fd可能无法在您的平台上实现。
如果它们不可用，则使用它们将引发NotImplementedError
如果找不到 则直接报错 NotImplementedError


"""