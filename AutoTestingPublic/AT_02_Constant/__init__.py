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
    Zero = 0
    One = 1
    # api docs Constant
    ApiDocsFlags = 'v2/api-docs'
    ApiSwaggerFlags = '/swagger-ui.html'
    GroupFlags = '?group='
    PublicAddress = '/swagger-resources'
    ReAllFlags = 'all'
    ReDefaultFlags = 'default'
    ReV = "v"
    # docs keys
    Host = 'Host'
    BasePath = '/'
    Tags = 'tags'
    Paths = 'paths'
    Def = 'definitions'
    # Error Constant
    ErrorMessage = ':请求错误'
    # Request Constant
    Post = 'post'
    Headers = {"Content-Type": "application/json"}
    Get = 'get'
    Delete = 'delete'
    Patch = 'Patch'
    # DB Constant
    MongoClientIp = 'localhost'
    MongoClientPort = 27017
    DBName = "LMK_DB"
    CollectionName = 'swagger_data'
    Insert = 'insert'
    Update = 'Update'
    Search = 'Search'
    ZeroID = {"_id": 0}
    # Public Constant
    Name = 'name'
    NullStr = ''
    Url = 'url'
