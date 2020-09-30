import requests
import json
import random
import numpy as np
from AT_02_Constant import Constants


# 定义 requests 请求的主方法

class RunMain(object):
    headers = Constants.Headers
    RequestsErrorMessage = None

    # 定义初始化方法
    def __init__(self, Url,  method, name,data):
        self.url = Url
        self.data = data
        self.method = method
        self.RequestsErrorMessage = name + Constants.ErrorMessage
        # 在 __init__ 中构造函数可以避免调用一次 构造一次 自动构造
        self.res = self.run_main()

    def send_get(self):

        res = requests.get(url=self.url, params=self.data).json()
        return res

    def send_post(self):
        try:
            res = requests.post(url=self.url, data=json.dumps(self.data), headers=self.headers).json()

        except Exception as e:
            print(self.url)
            res = self.RequestsErrorMessage
        return res

    def send_delete(self):
        res = requests.delete(url=self.url, params=self.data).json()
        return res
    def run_main(self):
        result = None
        if self.method == Constants.Get:
            result = self.send_get()
        if self.method == Constants.Post:
            result = self.send_post()
        if self.method == Constants.Delete:
            result = self.send_delete()
        return result


if __name__ == '__main__':
    pass
