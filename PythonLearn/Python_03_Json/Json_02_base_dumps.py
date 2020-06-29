import json


class JsonMethod(object):
    def __init__(self, dict_data):
        self.data = dict_data

    def dict_to_str(self) -> str:
        result = json.dumps(self.data, skipkeys=True, ensure_ascii=False, check_circular=True,
                            indent=2,sort_keys=True,
                            separators=(",",":"))
        '''
             indent 为缩进
             separators 为指定分隔
             sort_keys 为 排序
        '''
        return result


if __name__ == '__main__':
    data = {'Explain': '这是T3自动生成CSV文件的程序配置', 'Swagger': 'http://172.16.15.34:13582/swagger-ui.html',
            'DzdmAddress': 'http://172.18.15.163:62245/ref-server',
            'ApiDescription': '添加破产案件收立案信息', 'BodyKey': '破产案件收立案信息DTO',
            'DBtable': 'T_POCHAN_AJ_SLA', 'FileFlags': 'a',
            'custom_data_list':
                [{'code_content': [{'code': '1109', 'name': '破产监督', 'field': 'ywlx'}]},
                 {'code_content': [{'code': '2400', 'name': '湖南省高级人民法院',
                                    'field': 'jbfy'}]}]}

    except_result = JsonMethod(data)
    c = except_result.dict_to_str()
    print(c)

