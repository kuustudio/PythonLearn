import requests
import json
from Python_04_函数 import RandomData
import random
import numpy as np


# 定义 requests 请求的主方法

class RunMain():
    headers = {"Content-Type": "application/json"}

    # 定义初始化方法
    def __init__(self, Url, data, method):
        self.post = "发送Post请求..."
        self.get = "发送Get请求..."
        self.patch = "发送Patch请求..."
        self.delete = '发送Delete请求....'
        self.url = Url
        self.data = data
        self.method = method
        # 在 __init__ 中构造函数可以避免调用一次 构造一次 自动构造
        self.res = self.run_main()

    def send_get(self):
        print(self.get)
        res = requests.get(url=self.url, params=self.data).json()
        return res

    def send_post(self):
        print(self.post)
        res = requests.post(url=self.url, data=json.dumps(self.data), headers=self.headers).json()
        return res

    def send_delete(self):
        res = requests.delete(url=self.url, params=self.data).json()
        return res

    def run_main(self):
        result = None
        if self.method == "get":
            result = self.send_get()
        if self.method == "post":
            result = self.send_post()
        if self.method == "delete":
            result = self.send_delete()
        return result


if __name__ == '__main__':
    url = 'http://172.18.4.211:30100/api/v1/msajpczrxzjjsl'
    data = {
        "bzjse": RandomData.RandomData().INTRandomData(4,4),
        "bhAj": "50bfd418cdf34702845b25ef4d59824d",
        "jbfy": "2400",
        "ywlx": "0301"
    }
    print(data)
    my_request = RunMain(url, method="post", data=data)
    a = my_request.run_main()
    print(a)
