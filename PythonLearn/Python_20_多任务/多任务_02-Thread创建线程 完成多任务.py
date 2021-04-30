# -*- coding: utf-8 -*-

# @Project  : PythonLearn
# @File     : 多任务_02-Thread创建线程 完成多任务.py
# @Date     : 2021-04-12
# @Author   : Administrator
# @Info     :
# @Introduce:
import time, threading


class TwoThread(object):
    def __init__(self):
        pass

    def no_more_thread(self):
        t1 = threading.Thread(target=self.sing)  # 注意 不需要 sing()
        t2 = threading.Thread(target=self.dance)
        t2.start()  # 创建了一个小线程  执行代码
        t1.start()

    @staticmethod
    def sing():
        for i in range(5):
            print("正在唱歌中....")
            time.sleep(1)

    @staticmethod
    def dance():
        for i in range(10):
            print("正在跳舞......")
            time.sleep(1)


if __name__ == '__main__':
    # 什么是线程
    """
        一个程序运行起来之后 一定有一个执行代码的东西 这个东西就叫做线程
    """
    # 多任务的核心
    """
    使用主线程创建子线程，指向不同的函数 子线程运行时 主线程暂停 自线程运行完 主线程开始向下运行
    """
    # 如何查看别人的代码
    """
    只要看它函数的调用就行
    """