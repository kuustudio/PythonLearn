# 这是python操作json的方法
import json


class JsonMethod:
    pass


def change_to_json(content):
    json_content = json.dumps(content)
    print(type(json_content))
    return json_content


def change_to_dict(json_content):

    str_content = json.loads(json_content,encoding="UTF-8")
    print(str_content)
    print(type(str_content))
    exit()
    dict_content = dict(str_content)
    return dict_content
