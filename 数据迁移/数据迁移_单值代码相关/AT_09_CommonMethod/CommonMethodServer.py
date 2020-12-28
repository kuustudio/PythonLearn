import copy, json, random
from AT_00_SystemConstant import SystemConstant
from AT_04_DBDataProcess import ProcessConstant


def list_to_dict(list_data, *args) ->dict:
    data = copy.deepcopy(list_data)
    dict_data = {}
    for i in data:
        if args:
            if list(i.keys())[SystemConstant.Zero] in args[SystemConstant.Zero]:
                dict_data.update(i)
        else:
            dict_data.update(i)
    return dict_data


def list_filter_field_null(list_data, target, source):
    """
    根据 target 和 source 来 过滤list_data  过滤掉 target 或 source中全都为空的数据
    :param list_data: 元数据
    :param target: 过滤字段1
    :param source: 过滤字段2
    :return: 过滤后的数据
    """
    result = []
    for i in list_data:
        if (i[target] and i[source] ) is not None:
            result.append(i)
    return result


def code():
    pass


def add_comment_element(target, common)->list:
    """

    :param target:  目标列表 [{}]
    :param common:  公共map {}
    :return: [{}]
    """
    result = []
    for i in target:
        # 将 单值代码的所有的业务类型 变成 all
        key = i.keys()
        if ProcessConstant.ProcessConstantServer.TargetYwlxField in key:
            i[ProcessConstant.ProcessConstantServer.TargetYwlxField] = 'all'
        if ProcessConstant.ProcessConstantServer.SourceYwlxField in key:
            i[ProcessConstant.ProcessConstantServer.SourceYwlxField] = 'all'
        i.update(common)
        result.append(i)
    return result


def get_common(data):
    """

    :param data: 根据传过来的 字段表中的数据获取对应的模式 源库表名和目标库表名
    :return: dict
    """
    result = {}
    if isinstance(data,dict):
        for i in data.keys():
            if i in ProcessConstant.ProcessConstantServer.add_to_single_list:
                result.update({i:data[i]})
    return result


def change_dict_value(data, key_list, value_list):

    for item in data:
        for i, key in enumerate(key_list):
            if key in list(item.keys()):
                item[key] = value_list[i]
    return data


def extend_list_set(list1, list2):
    for i in list1:
        if i not in list2:
            list2.append(i)
    return list2


def dict_to_str(data) -> str:
    '''
                indent 为缩进
                separators 为指定分隔
                sort_keys 为 排序
    '''
    result = json.dumps(data, skipkeys=True, ensure_ascii=False, check_circular=True,
                            indent=2,sort_keys=True,
                            separators=(",",":"))

    return result

def get_pid():
    Pid = ''.join(str(i) for i in random.sample(range(0, 9), 8))  # sample(seq, n) 从序列seq中选择n个随机且独立的元素；
    return Pid


