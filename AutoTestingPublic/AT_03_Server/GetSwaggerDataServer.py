""" 获取 SwaggerData Server
    ： 获取 ENV的信息
"""

from AT_02_Constant import Constants, GroupConstant
from AT_05_Util import ExeclOperaUtil, DictUtil, RequestsUtil, ListUtil


class GetSwaggerDataServer(object):
    """获取Swagger信息的类"""
    SwaggerDocsAddress = None  # 用于接收 所有ApiDocs的变量
    SwaggerDocsData = None  # 用于接收SwaggerData
    SwaggerDocsKey = []  # 用于 接收 SwaggerDocsKey
    SwaggerFormatResult = []  # 用于接收 SwaggerData 处理的最终结果

    def __getattr__(self, item):
        return "调用的属性异常"

    def __int__(self):
        pass

    def util_main(self):
        # 实例化 execl 的操作方法
        TargetEnvInfo = None
        ExeclOperaMethod = ExeclOperaUtil.ExeclOpera(Constants.EnvFileName, Constants.EnvSheetName,
                                                     Constants.EnvTitleRow,
                                                     Constants.EnvStartRow
                                                     )
        # 调用get 方法 分析 env 数据 获取环境光信息]
        EvnInfo = ExeclOperaMethod.get_excel_info()
        # 实例化字典方法
        DictEvnInfo = DictUtil.DictUtilMethod(EvnInfo, Constants.EnvSwaggerStart, Constants.EnvSwaggerEnd)
        # 从Env 地址中获取 Swagger地址信息
        self.SwaggerDocsAddress = DictEvnInfo.get_target_index_dict()
        self.get_swagger_data()

    def get_swagger_data(self):
        for i in self.SwaggerDocsAddress:
            key = list(i.keys())[Constants.Zero]
            value = i[key]
            RequestMethod = RequestsUtil.RunMain(value, Constants.Post, key, data=None)
            self.SwaggerDocsData = RequestMethod.run_main()
            if isinstance(self.SwaggerDocsData, dict):
                self.SwaggerDocsKey = self.SwaggerDocsData.keys()
            if self.SwaggerDocsKey:
                self.format_swagger_main()
        print(self.SwaggerFormatResult)

    def format_swagger_main(self):
        """
        处理 swagger data 的 总方法
        """
        if self.SwaggerDocsKey:
            if Constants.Tags in self.SwaggerDocsKey:
                self.format_swagger_tags()
            if Constants.Host in self.SwaggerDocsKey:
                self.format_swagger_host()
            if Constants.BasePath in self.SwaggerDocsKey:
                self.format_swagger_basepath()

            pass

    def format_swagger_tags(self):
        print(self.SwaggerDocsData)
        Tags = self.SwaggerDocsData[Constants.Tags]
        for OneTag in Tags:
            self.SwaggerFormatResult.append(OneTag)

    def format_swagger_host(self):
        """
        处理swagger host
        host : ip + port
        :return: str
        :rtype str

        """
        Host = self.SwaggerDocsData[Constants.Host]
        element = {Constants.Host: Host}
        ListUtil.add_element(self.SwaggerFormatResult, element)

    def format_swagger_basepath(self):
        """
        处理 basepath
         basepath:/
        :return: str
        :rtype str

        """
        BasePath = self.SwaggerDocsData[Constants.BasePath]
        element = {Constants.BasePath: BasePath}
        ListUtil.add_element(self.SwaggerFormatResult, element)


if __name__ == '__main__':
    x = GetSwaggerDataServer()
    x.util_main()
