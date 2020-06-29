from T3_Z_Method import T3_04_ResuitMethod, T3_07_T3Method


class SingleCode:
    pass


def create_single_code_address(single_code_address):
    reload_cache_address = single_code_address + "/api/v1/codes/actions/reload_cache"
    find_code_address = single_code_address + "/api/v1/codeTypes/"
    return reload_cache_address, find_code_address


def get_single_code_address(single_code_address, index):
    result = single_code_address[index]
    return result


def execute_reload_cache(single_code_address):
    post_address = get_single_code_address(single_code_address, 0)
    result = T3_04_ResuitMethod.send_str_get_request(post_address)
    execute_result = "执行刷新缓存的结果是" + result
    return result


def execute_get_code_address(swagger_data, single_code_address):
    find_code_address = get_single_code_address(single_code_address, 1)
    for one in swagger_data:
        pid = one["pid"]
        code_address = find_code_address + pid
        one["code_address"] = code_address
        one.pop("pid")
    return swagger_data


def get_pid_data(data):
    pid_list = []
    for i in data:
        if i['pid'] is None:
            pass
        else:
            pid_list.append(i)
    return pid_list


def get_code_content(swagger_data):
    for one in swagger_data:
        code_address = one["code_address"]
        code_dict = T3_04_ResuitMethod.send_get_request(code_address)
        code_content = T3_07_T3Method.get_need_dict_content(code_dict, "codes")
        code_list = T3_07_T3Method.get_new_dict_list(code_content, "code", "name")
        one["code_content"] = code_list
        one.pop("code_address")
    return swagger_data


def replace_array_code(code_content):
    for one_code in code_content:
        code_value = one_code["code"]

        array_code = str(code_value).split()
        one_code["code"] = array_code
    return code_content


def add_single_name(code_content, field):
    for code in code_content:
        code["field"] = field
    return code_content


def single_data_handle(single_data):
    for one in single_data:
        code_content = one["code_content"]
        code_content = add_single_name(code_content,one["name"])
        if one["type"] == "array":
            code_content = replace_array_code(code_content)
        one.pop("type")
        one.pop("name")
    return single_data


