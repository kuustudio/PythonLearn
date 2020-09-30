from FS_02_Config import Config_01_swagger_address_config, config_02_system_content
from FS_99_Util import Util_01_xlrd
from FS_03_Swagger_Unit import Swagger_01_Util
from FS_05_Mongodb import Mongodb_client


def get_test_swagger_address():
    result = None
    new = None
    try:
        comment_field = config_02_system_content.Content()
        swagger_address_doc = Config_01_swagger_address_config.swagger_address()
        sheet_data = config_02_system_content.Content.swagger_sheet_data
        swagger_address_data = Util_01_xlrd.get_one_smd_data(swagger_address_doc, sheet_data, 0, 1)
        # get swagger address
        for one_swagger_address in swagger_address_data:
            if one_swagger_address['名称'] == config_02_system_content.Content.server_name:
                for one_key in one_swagger_address:
                    if config_02_system_content.Content.evn_name in one_key:
                        swagger_address = one_swagger_address[one_key]
                        result = swagger_address.replace(comment_field.swagger_html, comment_field.swagger_docs)
                        new = result.replace(comment_field.dev_swagger_ip, comment_field.swagger_ip)
    except TypeError as e:
        return "获取swagger地址错误"
    return new


class CallRule(object):
    error_swagger_data = None

    def __init__(self):
        pass

    @staticmethod
    def call_method():
        num = 0
        comment_field = config_02_system_content.Content()
        swagger__address_list = Swagger_01_Util.get_test_swagger_address()
        esp_swagger_address = Swagger_01_Util.especial_server(swagger__address_list)
        for tow in esp_swagger_address:
            one = tow.get("swagger_address")
            swagger_name = tow.get('swagger_name')
            try:
                CallRule.error_swagger_data = one

                swagger_docs_address = one.replace(comment_field.swagger_html, comment_field.swagger_docs)
                without_bean_data = Swagger_01_Util.get_swagger_data(swagger_docs_address, swagger_name)
                num += without_bean_data[1]
                Test_bean_info = Swagger_01_Util.get_server_bean_info(without_bean_data[0], swagger_docs_address)

                format_bean_info = Swagger_01_Util.format_definitions_info(Test_bean_info)
                db_op = Mongodb_client.MongoCLient("LMK_DB", "swagger_data", "insert", format_bean_info)
                db_op.MongoCLient()
                print("获取服务【%s】数据成功" % one)
            except Exception as e:
                print('获取【%s】数据失败,请启动服务！ ' % CallRule.error_swagger_data)
        print("一共拥有服务[%s],接口[%s]" % (len(esp_swagger_address), num))

    def main(self):
        self.call_method()


if __name__ == '__main__':
    CallRule().main()
