from T3_Z_Method import T3_03_StrMethod, T3_04_ResuitMethod, T3_06_ReMethod
import re


class SwaggerData:
    pass


def get_post_address(SwaggerAddress):
    post_address = T3_03_StrMethod.replace_string(SwaggerAddress,
                                                  "swagger-ui.html",
                                                  "v2/api-docs", 1)
    return post_address


def get_swagger_data(post_address):
    swagger_data = T3_04_ResuitMethod.send_get_request(post_address)
    return swagger_data


def get_definitions_data(data, key):
    definitions_data = data[key]
    return definitions_data


def get_path_value(path_data):
    value_list = []
    for key in path_data.keys():
        value = path_data[key]
        post_type = list(value.keys())[0]
        if post_type == "post":
            value_list.append(value[post_type])
    return value_list


def get_config_api_value(data, ApiDescription):
    for value in data:
        if value["summary"] == ApiDescription:
            api_value = value["parameters"]
            description_list = [i["name"] for i in api_value if i["in"] == "body"]
            description = "".join(description_list)
            return description
        else:
            pass


def get_config_definitions_data(definitions_data, description_dto):
    config_api_data = definitions_data[description_dto]["properties"]

    return config_api_data


def get_code_field(api_data):
    code_field_list = []
    keys = api_data.keys()
    for key in keys:
        value = api_data[key]
        value_description = value["description"]
        element_list = T3_03_StrMethod.spilt_string(value_description)
        value["ZWM"] = element_list[0]
        value["name"] = key
        num_list = re.findall('\d+', element_list[1])
        if num_list:
            if re.search(r'^1140', num_list[0]):
                value['single'] = num_list[0]
                value['vc'] = '100'
            elif num_list[0] == "100":
                value["single"] = ''
                value['vc'] = '100'
            elif num_list[0] == "600":
                value['vc'] = '600'
                value["single"] = ''
            elif num_list[0] == "32":
                value['vc'] = '32'
                value["single"] = ''
            else:
                value["single"] = ''
                value['vc'] = ''
        else:
            value["single"] = ''
            value['vc'] = ''
        code_field_list.append(value)
    return code_field_list


def get_final_result(code_field_list):
    result_list = []
    for code_field in code_field_list:
        field_type = code_field.get("type")
        field_name = code_field.get("name")
        code_type = T3_06_ReMethod.re_search_single_code(code_field["description"])
        list_code = ["11401179","11401216"]
        if code_type not in list_code:
            result_dict = {"type": field_type,
                           "name": field_name,
                           "pid": code_type}
            result_list.append(result_dict)
    return result_list
