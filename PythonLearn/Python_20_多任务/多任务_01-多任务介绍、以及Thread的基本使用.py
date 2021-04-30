# -*- coding: utf-8 -*-

# @Project  : PythonLearn
# @File     : 多任务_01-多任务介绍、以及Thread的基本使用.py
# @Date     : 2021-04-12
# @Author   : Administrator
# @Info     : threading
# @Introduce:
import time, threading


class TwoThread(object):
    def __init__(self):
        pass

    def no_more_thread(self):
        t1 = threading.Thread(target=self.sing)     # 注意 不需要 sing()
        t2 = threading.Thread(target=self.dance)
        t2.start()
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
    a = TwoThread()
    a.no_more_thread()
    l =len(threading.enumerate())
    print(l)

    # 多任务的概念
"""
    1.什么是多任务？
        多个任务一起执行 一般解释为并发
"""