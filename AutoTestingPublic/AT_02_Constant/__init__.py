"""
常量类
"""


class Constants(object):
    def __int__(self):
        pass

    # 分析 Env 用到的常量
    EnvSheetName = '环境信息'
    EnvFileName = '../AT_00_ENV/ENV.xlsx'
    EnvTitleRow = 0
    EnvStartRow = 1
    #  获取 Swagger 数据使用环境 因为要全量 需要所有服务启动 所以环境配置为稳定
    EvnAddress = "场景层稳定环境"
    EnvSwaggerStart = '以下是中台服务'
    EnvSwaggerEnd = '数据库信息'
    # 获取swagger 服务地址
    EnvInfoName = '名称'
    One = 1
    a = '../AT_00_ENV/04_正向长度边界-民事案件赔偿责任限制基金设立.xlsx'
    b = 'caselist'