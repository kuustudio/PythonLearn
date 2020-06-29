# 这是Python操作re正则的方法
import re


class ReMethod:
    pass


def re_search_data(data):
    result = re.search(r'1140',data)
    return result


def re_search_single_code(data):
    n = re.search(r'1140\d+', data)
    if n:
        result = re.search(r'1140\d+', data).group()
        return result
    else:
        pass


def re_search_chinese(data):
    Name = (re.search(r'[\u4e00-\u9fa5]+', data)).group()
    return Name

