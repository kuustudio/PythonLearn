import json
from functools import wraps

file = "D:\\SJT\\01_interfacedatacomparator\\T3-CSV\\Z-Config\\Config.txt"


def formatjson(get_content):
    @wraps(get_content)
    def wrapper(*args):
        file_content = get_content(*args)
        dict_config_content = eval(file_content)
        return dict_config_content

    return wrapper


class ReadFile(object):
    def __init__(self, filename):
        self.filename = filename

    @formatjson
    def get_content(self):
        f = open(self.filename, 'r', encoding="UTF-8")
        file_content = f.read()
        return file_content


if __name__ == '__main__':
    a = ReadFile(file)
    c = a.get_content()


