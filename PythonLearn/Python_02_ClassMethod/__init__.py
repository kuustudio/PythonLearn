# 类方法
# 如果 该class 没有要继承的类 则一般需要继承 object 基类
# __name = 类方法私有属性
# __dict__ map 展示类中所有的 属性
# __str__方法需要返回一个字符串，当做这个实例化对象的描写

class ClassMethodBase(object):
    # 起手初始化 以示尊敬
    # 定义私有属性,私有属性在类外部无法直接进行访问

    def __init__(self, name):
        # 定义类属性
        self.name = name
        self.__data = 'weight'

    # 定义类方法
    # self 就是 对象/实例 属性的集合，self代表类的实例，而非类
    def class_base(self):
        """这是文档字符串"""
        print("hello word")
        return "什么东西"

    def __str__(self):
        return self.name


if __name__ == '__main__':
    # 实例化 对象 ClassMethodBase
    Base = ClassMethodBase(name='我怕')
    # 调用 类方法
    a = Base.class_base()
    print(a)  # 什么东西
    print(Base.__dict__)
