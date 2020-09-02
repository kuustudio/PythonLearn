import requests
import json


# 定义 requests 请求的主方法

class RunMain():
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
        res = requests.get(url=self.url, data=self.data).json()
        return res

    def send_post(self):
        print(self.post)
        res = requests.post(url=self.url, data=self.data).json()
        return res

    def run_main(self):
        result = None
        if self.method == "get":
            result = self.send_get()
        if self.method == "post":
            result = self.send_post()
        return result


if __name__ == '__main__':
    url = 'http://172.18.15.197:30101/v2/api-docs'
    my_request = RunMain(url, method="get", data=None)
