from AT_02_Constant import Constants
from AT_05_Util import RequestsUtil
import re


class DictUtilMethod(object):
    SwaggerAddressList = None
    ApiDocsAddress = []
    Host = None  # 记录每次请求的host
    PublicInfo = None  # 记录每个请求对应的版本

    def __init__(self, data, index_start, index_end):
        self.data = data
        self.Index = index_start
        self.IndexEnd = index_end

    def get_target_index_dict(self) -> list:
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
        res = self.get_target_list()
        return res

    def get_target_list(self) -> list:
        """
        目的是 获取Swagger Docs Address
        循环 swagger address list
        如果配置的环境地址在列表元素map的键值列表中
        以 该map的指定键对应的值 为键
        以 该map的指定键的对应值为值 如果需要转换 根据配置转换
        set 进指定的map 返回
        :rtype list
        :return: 服务地址object list
        """
        for i in self.SwaggerAddressList:
            if Constants.EvnAddress in list(i.keys()):
                key = i[Constants.EnvInfoName]
                self.Host = str(i[Constants.EvnAddress]).replace(Constants.ApiSwaggerFlags, Constants.NullStr)
                PublicInfo = self.Host + Constants.PublicAddress
                RequestMethod = RequestsUtil.RunMain(PublicInfo, Constants.Post, key, data=None).run_main()

                if isinstance(RequestMethod, list) is True:
                    for j in RequestMethod:
                        info = self.format_swagger_docs_address(j, key)
                        if info:
                            self.ApiDocsAddress.append(info)

        return self.ApiDocsAddress

    def format_swagger_docs_address(self, data, key):
        if Constants.ReV in data[Constants.Name]:
            if data[Constants.Name].index(Constants.ReV) == Constants.Zero:
                return
        if data[Constants.Name] == Constants.ReDefaultFlags :
            value = self.Host + data[Constants.Url]
            return {key: value}
        elif  data[Constants.Name] == Constants.ReAllFlags:
            value = self.Host + data[Constants.Url]
            return {key: value}
        else:
            return {data[Constants.Name]: self.Host + data[Constants.Url]}

    @staticmethod
    def get_value(data, key):
        if isinstance(data, dict):
            value = data[key]
            return value
        else:
            return
