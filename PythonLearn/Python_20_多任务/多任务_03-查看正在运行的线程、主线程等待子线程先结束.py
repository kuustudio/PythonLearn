# -*- coding: utf-8 -*-

# @Project  : PythonLearn
# @File     : 多任务_03-查看正在运行的线程、主线程等待子线程先结束.py
# @Date     : 2021-04-12
# @Author   : Administrator
# @Info     :
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
    time.sleep(1)
    print(l)


# 拆包的概念
    """
    https://blog.csdn.net/wzyaiwl/article/details/83079700
    """
# 创建线程的时间
    """
        调用类方法不会创建线程 创建的是实例对象
        调用 start 方法 时候创建线程并执行
    """