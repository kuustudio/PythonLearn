from T3_Z_Method import T3_01_FileMethod,T3_02_JsonMethod


class ReadConfig:
    pass


def spilt_config_path(path,filename):
    """
        获取config 文件的父级目录拼接config file path
    :return:
    """
    father_path = T3_01_FileMethod.get_file_path()
    config_path = father_path + "\\"+path+"\\" + filename
    return config_path


def get_config_content(config_path):

    file = open(config_path,'r',encoding="UTF-8")
    file_content = file.read()
    # eval  将字典字符串转字典。
    dict_config_content = eval(file_content)

    return dict_config_content




