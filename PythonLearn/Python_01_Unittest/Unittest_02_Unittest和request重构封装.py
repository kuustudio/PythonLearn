# coding : utf-8
# 连接 unittest
import unittest


# 使用unittest 必须 继承unittest
# 创建测试类
class TestMethod(unittest.TestCase):
    # 创建第一个case 如果 case不是test 开头 则 不能执行case
    def test_01(self):
        print("这是个测试方法")

    def test_02(self):
        print("这是第二个测试方法")


if __name__ == '__main__':
    unittest.main()
