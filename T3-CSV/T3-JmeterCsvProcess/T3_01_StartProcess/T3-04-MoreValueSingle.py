from T3_Z_Method import T3_01_FileMethod
from T3_02_ReadConfig import T3_01_ReadConfig
from T3_03_SwaggerData import T3_01_SwaggerData, T3_02_SwaggerData, T3_04_Parms_Rule
from T3_04_SingleCode import T3_01_SingleCode
from T3_05_CsvHandle import T3_01_CsvHandle
from T3_06_WriteResult import T3_01_WriteResult
from T3_Z_Method import Method
from T3_07_SmdData import T3_01_init_smddata

if __name__ == '__main__':
    config_path = T3_01_ReadConfig.spilt_config_path("Z-Config", "ChangeSmdToJson.txt")
    dict_config_content = T3_01_ReadConfig.get_config_content(config_path)
    smd_address = dict_config_content['address']
    smd_content = Method.get_one_smd_data(smd_address,"COL",0,1)



