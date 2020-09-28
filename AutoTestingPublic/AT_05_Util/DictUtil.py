from AT_02_Constant import Constants


class DictUtilMethod(object):
    SwaggerAddressList = None
    SwaggerAddressMap = {}

    def __init__(self, data, index_start, index_end):
        self.data = data
        self.Index = index_start
        self.IndexEnd = index_end

    def get_target_index_dict(self) -> dict:
        """
        根据 data 以及 配置元素 Constants Start End 获取 一个list data中子列表
        :return: Swagger 地址Map {}
        """
        for i in self.data:
            if i[Constants.EnvInfoName] == Constants.EnvSwaggerStart:
                self.Index = self.data.index(i)
            if i[Constants.EnvInfoName] == Constants.EnvSwaggerEnd:
                self.IndexEnd = self.data.index(i)
        self.SwaggerAddressList = self.data[self.Index + Constants.One:self.IndexEnd]
        res = self.get_target_map()
        return res

    def get_target_map(self) -> dict:
        for i in self.SwaggerAddressList:
            if Constants.EvnAddress in list(i.keys()):
                key = i[Constants.EnvInfoName]
                value = i[Constants.EvnAddress]
                self.SwaggerAddressMap.update({key: value})
        return self.SwaggerAddressMap
