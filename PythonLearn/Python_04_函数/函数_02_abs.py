""" 函数abs:
    ：:return 数字绝对值
    ：:arg abs( x )
    """


class Coordinate(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __pos__(self):  # 在对象前加“+”的操作
        return self

    def __neg__(self):  # 在对象前加“-”的操作
        new_coordinate = Coordinate(-self.x, -self.y)
        return new_coordinate

    """ 方法2：
        self.x = -self.x
        self.y = -self.y
        return self
    """

    def __abs__(self):
        new_coordinate = Coordinate(abs(self.x), abs(self.y))
        return new_coordinate


a = Coordinate(-12, 5)

a = -a
print(a.x)