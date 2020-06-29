"""这个用来获取默认入参"""
from T3_03_SwaggerData import T3_04_Parms_Rule


class One:
    pass


def get_require_field(definitions_data, description_dto):
    config_api_require_data = definitions_data[description_dto]["required"]
    return config_api_require_data


def get_not_required_data(value_code_field, config_api_require_data):
    require_list = []
    require_not_list = []
    for i in value_code_field:
        name = i["name"]
        if name in config_api_require_data:
            require_list.append(i)
        else:
            require_not_list.append(i)
    return require_list, require_not_list


def get_type_dict(data_list):
    type_list = []
    for item in data_list:
        type_dict = {}
        name = item['name']
        f_type = item['RCLX']
        single = item['single']
        type_dict['f_type'] = f_type
        type_dict['name'] = name
        type_dict['single'] = single
        type_list.append(type_dict)
    return type_list


def get_csv_value(type_value):
    csv_value = [['name', 'value']]
    for i in type_value:
        csv_dict = []
        key = i['name']
        value = T3_04_Parms_Rule.DefaultValue(i)
        csv_dict.append(key)
        csv_dict.append(value)
        csv_value.append(csv_dict)
    return csv_value
