from T3_08_ConfigController import T3_01_ConfigControl

if __name__ == '__main__':
    #   第一步 调用方法获取配置文件信息
    config_value = T3_01_ConfigControl.ConfigControl("Z-Config", "Config.txt","DzdmAddress")
    config_value.get_configfile()
    a = config_value.get_file_content()
    print(a)



