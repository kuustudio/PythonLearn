# coding : utf-8
# 连接 unittest
import unittest

# 使用unittest 必须 继承unittest
# 创建测试类
import unittest
from Python_01_Unittest import Unittest_00_requests_runmain

# 使用unittest 必须 继承unittest
# 创建测试类
from Python_01_Unittest.Unittest_00_requests_runmain import RunMain


class Test(unittest.TestCase):
    # 定义类方法 类方法只会执行一次
    url = "http://172.18.15.197:30101/v2/api-docs"
    data = None
    method = 'get'

    @classmethod
    def setUpClass(cls):
        print("这是类执行之前的方法")

    @classmethod
    def tearDownClass(cls):
        print("这是类执行之后的方法")

    # 创建测试之前的方法 setup
    def setUp(self):
        print(self.url)
        self.run = RunMain(self.url, self.data, self.method)

    # 创建测试之后的方法
    def tearDown(self):
        print('test -> tearDown')
        pass

    # 创建第一个case 如果 case不是test 开头 则 不能执行case
    def test_01(self):
        res = self.run.run_main()

        self.assertEqual(res['info']['description'], 'T3诉讼参与人服务', "测试失败")
        globals()['result'] = res['info']['description']
        #   下一个请求赋值参数
        Test.url = "http://172.18.15.197:30100/v2/api-docs"
        Test.method = 'get'
        '''
            first 结果 
            second 期望
            msg 提示信息
        '''
        #   跳过 case

    @unittest.skip("test_02")
    def test_02(self):
        print("这是第二个测试方法")
        res = self.run.run_main()
        print(res)
        self.assertEqual(res['info']['description'], 'T3诉讼参与人服务', "测试失败")
        globals()['result'] = res['info']['description']
        #   下一个请求赋值参数
        Test.url = "http://172.18.15.197:30100/v2/api-docs"
        Test.method = 'get'
        '''
            first 结果 
            second 期望
            msg 提示信息
        '''


if __name__ == '__main__':
    # 总体执行
    # unittest.main()
    # 套件执行
    suite = unittest.TestSuite()
    suite.addTest(TestMethod('test_01'))
    unittest.TextTestRunner().run(suite)
# class TestMethod(unittest.TestCase):
#     # 创建第一个case 如果 case不是test 开头 则 不能执行case
#     def test_01(self):
#         print("这是个测试方法")
#
#     def test_02(self):
#         print("这是第二个测试方法")
#
#
# if __name__ == '__main__':
#     unittest.main()
