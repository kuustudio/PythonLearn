# -*- coding: utf-8 -*-

# @Project  : PythonLearn
# @File     : UUID4.py
# @Date     : 2021-04-12
# @Author   : Administrator
# @Info     :
# @Introduce:

import uuid


def get_uuid():
    """
    获取 uuid 并且删除"-"
    :return: str
    :rtype str
    """
    return uuid.uuid4().hex
