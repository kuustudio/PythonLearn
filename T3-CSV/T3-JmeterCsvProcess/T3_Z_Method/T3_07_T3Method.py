# 这里是 Python 的组合方法 用于这个程序


class T3Method:
    pass


def get_need_dict_content(data, key):
    need_content = data[key]
    return need_content


def get_new_dict_list(need_content, code_key, trans_key):
    need_list = []
    for field in need_content:
        need_dict = {code_key: field[code_key],
                     trans_key: field[trans_key]
                     }
        need_list.append(need_dict)
    return need_list
