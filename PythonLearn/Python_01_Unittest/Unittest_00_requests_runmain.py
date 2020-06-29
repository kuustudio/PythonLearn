import requests
import json


# 定义 requests 请求的主方法

class RunMain():
    # 定义初始化方法
    def __init__(self):
        self.post = "发送Post请求..."
        self.get = "发送Get请求..."
        self.patch = "发送Patch请求..."
        self.delete = '发送Delete请求....'

    def send_get(self, url, data):
        print(self.get)
        res = requests.get(url=url, data=data).json()
        return json.dumps(res,indent=2, sort_keys=True)
