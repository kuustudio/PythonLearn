import random


class CsvHandle:
    pass


def get_csv_data_num(code_data):
    num_list = []
    for one_data in code_data:
        code_content = one_data["code_content"]
        content__length = len(code_content)
        num_list.append(content__length)
    return max(num_list)


def supple_one_code_list(code_list, num):
    for i in range(0, num):
        code_length = len(code_list)
        if code_length < num:
            supple_data = random.choice(code_list)
            code_list.append(supple_data)
        else:
            return code_list


def replace_key(code_list):
    for one in code_list:
        field = one["field"]
        translate = one["name"]
        one[field + "TranslateText"] = translate
    return code_list


def supple_code_data(code_data, num):
    for one_data in code_data:
        key = "code_content"
        code_content = one_data[key]
        code_content = supple_one_code_list(code_content, num)

    return code_data


def get_translate_field(code_data):
    for one_data in code_data:
        key = "code_content"
        code_content = one_data[key]
        trans_data = replace_key(code_content)
    return code_data


def get_csv_title(code_data):
    write_data_list = []
    title_list = []
    for one in code_data:
        code_content = one["code_content"]
        for one_content in code_content:
            field = one_content["field"]
            fieldTranslateText = field + "TranslateText"
            if (field and fieldTranslateText) not in title_list:
                title_list.append(field)
                title_list.append(fieldTranslateText)
    write_data_list.append(title_list)
    return write_data_list


def get_need_index_data(i, code_content):
    result_list = []
    for one in code_content:
        code = one["code_content"]
        content = code[i]
        result_list.append(content["code"])
        result_list.append(content["name"])

    return result_list


def get_csv_content(csv_list, code_content, num):
    for i in range(0, num):
        result = get_need_index_data(i, code_content)
        csv_list.append(result)
    return csv_list


def change_data_list(data):
    for i in data:
        for j in i:
            if type(j) != str:
                a = list(i).index(j)
                i[a] = str(j)
    return data
