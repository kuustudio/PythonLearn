from T3_Z_Method import T3_01_FileMethod, T3_02_JsonMethod,T3_05_DictMethod


class ConfigControl(object):
    # 定义类属性
    configfile = None

    # 定义初始化属性
    def __init__(self, path, filename, key):
        #   path  与该程序处于同一级目录的 文件夹名称
        self.path = path
        #   filename path 文件夹需要取得配置文件名
        self.filename = filename
        #   key 根据key 获取希望的配置信息
        self.key = key
        print("从[%s]中获取配置文件[%s]中的配置项[%s]" % (self.path,self.filename,self.key))

    # 拼接 类属性 configfile
    def get_configfile(self):
        #  获取当前项目路径
        current_path = T3_01_FileMethod.get_file_path()
        #   拼接配置文件path
        config_path = current_path + "\\" + self.path + "\\" + self.filename
        ConfigControl.configfile = config_path

    # 文件内容转化为字典
    def get_file_content(self):
        try:
            file = open(self.configfile, 'r', encoding="UTF-8")
            file_content = file.read()
            # eval  将字典字符串转字典。
            dict_config_content = eval(file_content)
            value = T3_05_DictMethod.get_value(dict_config_content,self.key)
            if value:
                return value
            else:
                return "这个配置不存在"
        except Exception as e:
            return "打开文件[%s]失败" % ConfigControl.configfile





