from T3_Z_Method import T3_01_FileMethod
from T3_02_ReadConfig import T3_01_ReadConfig
from T3_03_SwaggerData import T3_01_SwaggerData
from T3_04_SingleCode import T3_01_SingleCode
from T3_05_CsvHandle import T3_01_CsvHandle
from T3_06_WriteResult import T3_01_WriteResult

if __name__ == '__main__':
    config_path = T3_01_ReadConfig.spilt_config_path("Z-Config", "Config.txt")
    dict_config_content = T3_01_ReadConfig.get_config_content(config_path)
    swagger_address = dict_config_content["Swagger"]
    ApiDescription = dict_config_content["ApiDescription"]
    # 从这往下是swagger数据处理方法
    post_address = T3_01_SwaggerData.get_post_address(swagger_address)
    swagger_data = T3_01_SwaggerData.get_swagger_data(post_address)
    definitions_data = T3_01_SwaggerData.get_definitions_data(swagger_data, "definitions")
    path_data = T3_01_SwaggerData.get_definitions_data(swagger_data, "paths")
    path_value_list = T3_01_SwaggerData.get_path_value(path_data)
    description_dto = dict_config_content["BodyKey"]
    #   T3_01_SwaggerData.get_config_api_value(path_value_list,ApiDescription)
    config_api_data = T3_01_SwaggerData.get_config_definitions_data(definitions_data, description_dto)
    value_code_field = T3_01_SwaggerData.get_code_field(config_api_data)
    swagger_result = T3_01_SwaggerData.get_final_result(value_code_field)
    # 从这 往下是单值代码的方法
    single_code_address = dict_config_content["DzdmAddress"]
    reload_cache_address = T3_01_SingleCode.create_single_code_address(single_code_address)
    execute_reload_cache = T3_01_SingleCode.execute_reload_cache(reload_cache_address)
    pid_swagger_result = T3_01_SingleCode.get_pid_data(swagger_result)
    execute_get_address = T3_01_SingleCode.execute_get_code_address(pid_swagger_result, reload_cache_address)
    execute_get_content = T3_01_SingleCode.get_code_content(execute_get_address)
    final_single_result = T3_01_SingleCode.single_data_handle(execute_get_content)
    # 从这往下是为了写入文件做的特殊处理,需要在这里加上 自定义的csv字段  比如ywlx jbfy chr
    custom_data_list = list(dict_config_content["custom_data_list"])
    final_single_result.extend(custom_data_list)
    #   获取 字段与${字段}作为写入文件作为参考
    json_data = T3_01_WriteResult.get_json_data(final_single_result)
    csv_data_num = T3_01_CsvHandle.get_csv_data_num(final_single_result)
    supple_data = T3_01_CsvHandle.supple_code_data(final_single_result, csv_data_num)
    change_trans_data = T3_01_CsvHandle.get_translate_field(supple_data)
    csv_write_data = T3_01_CsvHandle.get_csv_title(change_trans_data)
    csv_write_content = T3_01_CsvHandle.get_csv_content(csv_write_data, change_trans_data, csv_data_num)
    csv_write_type = T3_01_CsvHandle.change_data_list(csv_write_content)
    result_dir_address = T3_01_WriteResult.get_result_dir_path()
    save_dir_address = T3_01_WriteResult.get_save_dir(ApiDescription, result_dir_address)
    flags = dict_config_content["FileFlags"]
    write_result = T3_01_WriteResult.write_csv_file(csv_write_type, save_dir_address,
                                                    ApiDescription, flags)
    print(write_result)
    json_write_result = T3_01_WriteResult.write_json_data(json_data, save_dir_address,
                                                          ApiDescription, flags)
    print(json_write_result)
