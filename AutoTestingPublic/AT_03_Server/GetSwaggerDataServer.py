""" 获取 SwaggerData Server
    ： 获取 ENV的信息
"""

from AT_02_Constant import Constants
from AT_05_Util import ExeclOperaUtil, DictUtil


class GetSwaggerDataServer(object):

    def util_main(self):
        # 实例化 execl 的操作方法
        TargetEnvInfo = None
        ExeclOperaMethod = ExeclOperaUtil.ExeclOpera(Constants.a, Constants.b,
                                                     Constants.EnvTitleRow,
                                                     Constants.EnvStartRow
                                                     )
        # 调用get 方法 分析 env 数据 获取环境光信息]
        EvnInfo = ExeclOperaMethod.get_excel_info()
        # 实例化字典方法
        DictEvnInfo = DictUtil.DictUtilMethod(EvnInfo,Constants.EnvSwaggerStart,Constants.EnvSwaggerEnd)
        # 从Env 地址中获取 Swagger地址信息
        SwaggerData = DictEvnInfo.get_target_index_dict()
        print(SwaggerData)


if __name__ == '__main__':
    x = GetSwaggerDataServer()
    x.util_main()
