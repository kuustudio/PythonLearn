import os
import time
import json

from T3_Z_Method import T3_01_FileMethod, T3_06_ReMethod


class WriteResult:
    pass


def get_result_dir_path():
    father_path = T3_01_FileMethod.get_file_path()
    result_dir = father_path + "\\Z-Result"
    if not os.path.exists(result_dir):
        os.mkdir(result_dir)
    return result_dir


def get_api_dir(api, result_dir):
    name = T3_06_ReMethod.re_search_chinese(api)
    api_dir = result_dir + "\\" + name
    if not os.path.exists(api_dir):
        os.mkdir(api_dir)
    return api_dir


def get_save_dir(api, result_dir):
    api_dir = get_api_dir(api, result_dir)
    LocateTime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    RQ = str(LocateTime).split()[0]
    SJ = str(LocateTime).split()[1]
    a = "".join([x for x in (RQ.split("-"))])
    b = "".join([x for x in (SJ.split(":"))])
    dictionaryMC = a + b + api
    save_dir = api_dir + "\\" + dictionaryMC
    if not os.path.exists(save_dir):
        os.mkdir(save_dir)
    return save_dir


def get_write_data(data):
    data_length = len(data)
    for i in range(0, data_length + 1):
        if i == data_length:
            return "\n"
        else:
            return str(data[i]) + ","


def write_csv_file(data, save_dir, api, flags):
    csv_file = save_dir + flags + api + ".txt"
    file = open(csv_file, "a+", encoding="UTF-8")
    for i in data:
        file.write(",".join(i))
        file.write("\n")
    file.close()
    return "csv写入完成"


def get_json_data(code_data):
    data = {}
    for i in code_data:
        code_content = i["code_content"]
        for j in code_content:
            field = j["field"]
            field_value = "${" + field + "}"
            data.update({field: field_value})
    json_data = json.dumps(data, indent=4)
    return json_data


def write_json_data(json_data, save_dir, api, flags):
    json_file = save_dir + flags + api + "json" + ".txt"
    file = open(json_file, "a+", encoding="UTF-8")
    file.write(json_data)
    file.close()
    return "json数据写入完成"


def write_single_data(json_data, save_dir, api, flags):
    json_file = save_dir + flags + api + "single_data" + ".txt"
    file = open(json_file, "a+", encoding="UTF-8")
    for i in json_data:
        if type(i[1]) == str:
            file.write(",".join(i))
            file.write("\n")
        else:
            file.write(i[0])
            file.write(",")
            file.write(str(i[1]))
            file.write("\n")
    file.close()
    return "单一入参csv文件写入完场"
