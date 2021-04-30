# -*- coding: utf-8 -*-

# @Project  : PythonLearn
# @File     : Python设计模式_Class继承.py
# @Date     : 2021-04-28
# @Author   : Administrator
# @Info     :
# @Introduce:
"""
    类的继承可以大幅度的减少代码的重复，核心就是子类继承父类所有属性和方法
    父类向子类传递 子类继承父类所有属性和方法 这是类的继承
    如果 父类中的某个方法不能满足子类时，则需要重写子类的方法 这个方法的关键函数是

"""


class A (object):

    def __init__(self, name):
        self.name = name

    def eat(self):

        print("{0}".format(self.name))

    def drink(self):
        print("{0}".format(self.name))


class B (A):

    def run(self):
        print("{0}".format(self.name))

# Test 方法的重写


class C (B):

    def run(self):
        """
            方法1:定义一个和父类相同的方法  方法重写  完全不同
        """
        print("{0}".format("重写Test"))


class D (C):

    def run(self):
        """
            定义一个和父类相同的方法  方法重写  拓展 super
            super 调用了父类的方法
        """
        print("{0}".format("第二次尝试拓展"))
        super().run() # 调用父类的方法
        print("上面的兄弟调用了父类的方法")


if __name__ == '__main__':

    c = D("test")
    c.run()
