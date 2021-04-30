import json
from functools import wraps

file = "D:\\SJT\\01_interfacedatacomparator\\T3-CSV\\Z-Config\\Config.txt"


def test(my_method):
    @wraps(my_method)
    def wrapper(*args):
        a = 3
        return a
    return wrapper


def formatjson(get_content):
    @wraps(get_content)
    def wrapper(*args):
        file_content = get_content(*args)
        dict_config_content = eval(file_content)
        return dict_config_content

    return wrapper


class ReadFile(object):
    json_data = None

    def __init__(self, filename):
        self.filename = filename

    @formatjson
    def get_content(self):

        f = open(self.filename, 'r', encoding="UTF-8")
        file_content = f.read()
        ReadFile.json_data = file_content
        return file_content
    print(get_content.__name__)
    @formatjson
    def get_json_to_str(self) -> str:
        result = json.dumps(self.json_data, ensure_ascii=False, indent=4, skipkeys=True, sort_keys=True,
                            separators=(",", ":"))
        return result


if __name__ == '__main__':
    a = ReadFile(file)
    c = a.get_content()
    print(type(c))
    b = a.get_json_to_str()
    print(b)    
