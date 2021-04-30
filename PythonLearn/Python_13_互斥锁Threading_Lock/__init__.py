# -*- coding: utf-8 -*-

# @Project  : PythonLearn
# @File     : __init__.py.py
# @Date     : 2021-03-31
# @Author   : Administrator
# @Info     :
# @Introduce:
"""
每个线程互相独立，相互之间没有任何关系，但是在同一个进程中的资源，
线程是共享的，如果不进行资源的合理分配，对数据造成破坏，使得线程运行的结果不可预期。这种现象称为“线程不安全”。
eg : 多线程并发 在前一个没有处理完后一个就得到了该资源做下一步处理导致数据不准确
"""
# -*- coding: utf-8 -*-
import threading
import time


def test_xc():
    f = open("test.txt", "a")
    f.write("test_dxc" + '\n')
    time.sleep(1)
    f.close()


"""
线程同步能够保证多个线程安全访问竞争资源，最简单的同步机制是引入互斥锁。互斥锁为资源引入一个状态：锁定/非锁定。
某个线程要更改共享数据时，先将其锁定，此时资源的状态为“锁定”，其他线程不能更改；
直到该线程释放资源，将资源的状态变成“非锁定”，其他的线程才能再次锁定该资源。
互斥锁保证了每次只有一个线程进行写入操作，从而保证了多线程情况下数据的正确性。
#创建锁
mutex = threading.Lock()
#锁定
mutex.acquire([timeout])#timeout是超时时间
#释放
mutex.release()

其中，锁定方法acquire可以有一个超时时间的可选参数timeout。如果设定了timeout，
则在超时后通过返回值可以判断是否得到了锁，从而可以进行一些其他的处理。



"""
import threading
import time


def test_xc_x():
    f = open("test.txt", "a")
    f.write("test_dxc" + '\n')
    time.sleep(1)
    mutex.acquire()  # 取得锁
    f.close()
    mutex.release()  # 释放锁


if __name__ == '__main__':
    mutex = threading.Lock()  # 创建锁

