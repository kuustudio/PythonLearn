import requests
import json


class RequestMethod(object):
    # 定义类变量  header 消息头
    header = {"Content-Type": "application/json"}

    def __init__(self, url, data):
        self.url = url
        self.data = data

    def send_get(self, data):
        res = requests.get(self.url, self.data)
        if res.status_code =='200':
            response = json.dumps()
