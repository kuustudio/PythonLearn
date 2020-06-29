import xlrd
import re


class Method:
    pass


def get_one_smd_data(fliename, sheetname, title_row, start_row):
    """
    5st 通过 xlrd 将文件解析；
    :param fliename: 文件名称 带有绝对路径；
    :param sheetname: 获取的sheet 名称；
    :param title_row: sheet title 列 （作为键值）
    :param start_row: 开始解析的行
    :return: 该sheet 对应的数据 格式为[{},{},{}]
    """
    bk = xlrd.open_workbook(fliename)
    sh = bk.sheet_by_name(sheetname)
    row_num = sh.nrows
    data_list = []
    if sh.row_values(title_row)[0] == '':
        start_row += 1
        title_row += 1

    try:

        for i in range(start_row, row_num):
            row_data = sh.row_values(i)
            data = {}
            for index, key in enumerate(sh.row_values(title_row)):
                data[key] = row_data[index]
            if data not in data_list:
                data_list.append(data)
    except Exception as e:
        print("数据获取失败.，请小主检查对应文件配置...")
        print(e)
    print("数据获取完成...开始进行下一步,请小主喝杯咖啡继续等待......")
    return data_list


def spilt_content(word, flags, index):
    """
   切割字符串的方法
    :param word: 需要切割的内容
    :param flags:  切割的依据
    :param index:  获取切割内容的下标
    :return: 需要的内容 str
    """
    content = str(word).split(flags)
    return content[index]


def re_patten(rules, word):
    """
    正则匹配方法
    :param rules: 匹配规则
    :param word: 带匹配内容
    :return: 匹配结果 str
    """
    patten_list = re.findall(rules, word)
    result = ''.join(patten_list)
    return result


def float_two(float_data):
    """
    结果保留两位小数
    :param float_data: 小数结果
    :return:  保留两位小数的结果
    """
    float_data = round(float_data, 2)
    return float_data


def get_need_element(element_list, goal_list, smd_flags):
    """
    特殊的方法,适用于T3C 的 smd ；
    主要是批量解析 xlsx 文件后进行结果进行处理的方法
    根据配置 在结果中加入元素
    将获取的数据的键值替换成配置中的键值
        1st: 在获取的数据字典中加入 特定的元素，元素的键值是配置中的 value 值，value 是 数据字典中对应相同key 的value值；
        2st: 遍历 新的数据字典根据配置 取出需要的 元素 组成新的数据字典；
        3st： 加入其它需要的数据；
    :param element_list: 配置数据字典；
    :param goal_list: 解析 execl 获取的 data list ；
    :param smd_flags:  对数据来源进行标记； 标记依据是文件名的中文拼接；
    :return: 新的 数据字典
    """
    for i in element_list:
        for j in goal_list:
            j.update({"smd_flags": smd_flags})
            c = ''.join(i.keys())
            if c in j:
                j.update({i[c]:j[c]})

    return goal_list


def get_dict_element(cof_list, goal_dict, flags_key):
    goal_c = None
    new_dict = {}
    cof_list.append({flags_key: flags_key})
    for i in cof_list:
        c = ''.join(dict(i).values())
        if c in goal_dict:
            if ".0" in str(goal_dict[c]):
                goal_c = float_ch_string(goal_dict[c])
            else:
                goal_c = goal_dict[c]
            new_dict.update({c: str(goal_c)})
    return new_dict


def float_ch_string(target):
    """
    :param target: 要转换的目标
    :return: 转换后的结果
    """
    data = str(target).split(".")[0]

    return data








