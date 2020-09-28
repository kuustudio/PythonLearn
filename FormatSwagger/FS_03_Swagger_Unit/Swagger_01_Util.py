from FS_02_Config import Config_01_swagger_address_config, config_02_system_content
from FS_99_Util import Util_01_xlrd
from T3_Z_Method import T3_04_ResuitMethod, T3_05_DictMethod
from FS_04_Server_Map import SM_01_Swagger_Mapper
import re


def especial_server(server_list) -> list:
    #   行政的api docs 需要特殊处理
    for address in server_list:
        i = address.get("swagger_address")
        p = address.get("swagger_name")
        if ':30127' in i:
            server_list.remove(address)
            server_list.append({'swaggger_name':'司法制裁案件',
                                'swagger_address':'http://172.18.15.163:30127/v2/api-docs?group=司法制裁案件相关接口'})
            server_list.append({'swaggger_name':'破产案件',
                                'swagger_address':'http://172.18.15.163:30127/v2/api-docs?group=破产案件相关接口'})
            server_list.append({'swaggger_name':'案件公用',
                                'swagger_address':'http://172.18.15.163:30127/v2/api-docs?group=案件服务公用接口'})
            server_list.append({'swaggger_name':'管辖案件',
                                'swagger_address':'http://172.18.15.163:30127/v2/api-docs?group=管辖案件相关接口'})
            server_list.append({'swaggger_name':'行政案件',
                                'swagger_address':'http://172.18.15.163:30127/v2/api-docs?group=行政案件相关接口'})
            server_list.append({'swaggger_name':'赔偿案件',
                                'swagger_address':'http://172.18.15.163:30127/v2/api-docs?group=赔偿案件相关接口'})
            break
    for J in server_list:
        if ':30101' in J['swagger_address']:
            server_list.remove(J)
            server_list.append({'swaggger_name':'诉讼参与人',
                                'swagger_address':'http://172.18.15.163:30101/v2/api-docs?group=all'})
            break
    return server_list


def get_test_swagger_address():
    result = None
    try:
        comment_field = config_02_system_content.Content()
        swagger_address_doc = Config_01_swagger_address_config.swagger_address()
        sheet_data = config_02_system_content.Content.swagger_sheet_data
        swagger_address_data = Util_01_xlrd.get_one_smd_data(swagger_address_doc, sheet_data, 0, 1)
        # get swagger address
        server_name = config_02_system_content.Content.server_name
        result = []
        if server_name is None:
            for one_swagger_address in swagger_address_data:
                if 'swagger-ui.html' in one_swagger_address['中台联调环境（2.13更新）']:
                    name = one_swagger_address['名称']
                    for one_key in one_swagger_address:
                        if config_02_system_content.Content.evn_name in one_key:
                            swagger_address = one_swagger_address[one_key]
                            result.append({"swagger_address":swagger_address,'swagger_name':name})
                        # result = swagger_address.replace(comment_field.swagger_html, comment_field.swagger_docs)
        else:
            for one_swagger_address in swagger_address_data:
                if one_swagger_address['名称'] == server_name:
                    for one_key in one_swagger_address:
                        if config_02_system_content.Content.evn_name in one_key:
                            swagger_address = one_swagger_address[one_key]
                            result.append({"swagger_address":swagger_address,'swagger_name':one_swagger_address['名称']})
    except TypeError as e:
        return "获取swagger地址错误"
    return result


#    获取 必填项 排除 传入字段 可多个
def get_require_field(parameters_list, *args):
    result = []
    finally_bean = None
    for one in parameters_list:
        if one['required'] is True and one['name'] not in args:
            result.append(one['name'])
        if one['in'] == 'body':
            bean = one['schema']
            finally_bean = Util_01_xlrd.spilt_content(bean, "/", -1)
    return result, finally_bean


def get_swagger_data(address,name):
    global api_name
    comment_field = config_02_system_content.Content()
    result_list = []
    swagger_info = T3_04_ResuitMethod.send_get_request(address)
    paths_info = swagger_info['paths']
    api_num = len(paths_info)
    for i in paths_info:
        try:
            method = list(dict(paths_info[i]).keys())[0]
            result_dict = {'api': i, 'method': method,'swagger_name':name}
            api_name = paths_info[i][method]['summary']
            controller = paths_info[i][method]['tags']
            parameters = paths_info[i][method]['parameters']
            require_list = get_require_field(parameters, 'dto', 'vo')
            if require_list[0]:
                result_dict.update({'require_list': require_list[0]})
            if require_list[1]:
                result_dict.update({'DTO/VO': require_list[1]})
            result_dict['api_name'] = api_name
            if controller[0]:
                result_dict['controller'] = controller[0]
            #   获取测试接口的swagger data
            if not comment_field.api_name_list:
                result_list.append(result_dict)
            else:
                if api_name in comment_field.api_name_list:
                    result_list.append(result_dict)
        except KeyError as e:
            print("获取swagger数据失败,失败的原因是 服务：[%s],失败的接口是[%s],失败的原因是实体类中没有key值[%s]"
                  % (address, api_name, e))
    return result_list,api_num


def get_test_definitions_info(test_api_list, definitions_info):
    result = []
    try:
        for i in test_api_list:
            for j in definitions_info.keys():
                if 'DTO/VO' in i.keys():
                    if j == str(i['DTO/VO']).split("'")[0]:
                        i['parameters'] = definitions_info[j]
                        result.append(i)
                        break
    except TypeError as e:
        print(e)
    except UnicodeDecodeError as w:
        print(w)

    return result


def get_server_bean_info(result_list, address):
    #   获取测试接口的bean中字段
    swagger_info = T3_04_ResuitMethod.send_get_request(address)
    definitions_info = swagger_info["definitions"]
    test_definitions_info = get_test_definitions_info(result_list, definitions_info)
    if test_definitions_info:
        return test_definitions_info
    else:
        return "没有找到借口描述的键值"


def field_attribute_handle(one_result, num_list):
    if num_list:
        if re.search(r'^1140', num_list[0]):
            one_result['single'] = num_list[0]
            one_result['vc'] = '100'
        elif num_list[0] == "100":
            one_result["single"] = ''
            one_result['vc'] = '100'
        elif num_list[0] == "600":
            one_result['vc'] = '600'
            one_result["single"] = ''
        elif num_list[0] == "32":
            one_result['vc'] = '32'
            one_result["single"] = ''
        else:
            one_result["single"] = ''
            one_result['vc'] = ''
    else:
        one_result["single"] = ''
        one_result['vc'] = ''
    return one_result


def init_properties_data(properties):
    # 初始化 接口字段
    result = []
    for key in properties:
        one_result = {}
        if key:
            one_result["field"] = key
            value = properties[key]
            if value['description']:
                spilt = re.split('-| |\t|（|\(|,|，|。|}', value['description'])
                field_name = "".join(spilt[0])
                one_result["name"] = field_name
                if value['type']:
                    one_result['type'] = value['type']
                if len(spilt) > 1:
                    num_list = re.findall('\d+', spilt[1])
                    dict_data = field_attribute_handle(one_result, num_list)
                    finally_data = SM_01_Swagger_Mapper.swagger_attribute_handle(dict_data)
                    result.append(finally_data)
                else:
                    one_result['single'] = ''
                    one_result['vc'] = ''
                    finally_data = SM_01_Swagger_Mapper.swagger_attribute_handle(one_result)
                    result.append(finally_data)
            else:
                if value['items']:
                    one_result['single'] = '内嵌'
                    one_result['vc'] = value['items']
    return result


def format_definitions_info(test_definitions_info):
    # 初始化 bean信息
    for bean_info in test_definitions_info:
        try:
            parameters = T3_05_DictMethod.get_value(bean_info, "parameters")
            properties = T3_05_DictMethod.get_value(parameters, "properties")
            data = init_properties_data(properties)
            bean_info.update({"parameters": data})
        except KeyError as e:
            print("初始化【%s】失败,失败原因是 init 数据中不存在key值[%s]" % (bean_info['api_name'], e))

    return test_definitions_info
