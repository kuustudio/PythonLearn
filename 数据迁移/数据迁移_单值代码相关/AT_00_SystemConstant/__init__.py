import time


class SystemConstant(object):
    ClassErrorMessage = '调用属性异常'
    FatherDirFlag = ".."
    DirSpiltFlag = "\\"
    Flag = '.'
    Semicolon = ':'
    Slash = '/'
    PreSource = 'jdbc:sybase:Tds:'
    IP = 'ip'
    Port = 'port'
    User = 'userid'
    Password = 'password'
    DataBase = 'database'
    targetDB = 'targetDB'
    sourceDB = 'sourceDB'
    SourceDBSchema = 'dbo'
    SourceDBName = 'YWST'
    Zero = 0
    One = 1
    Tow = 2
    ExceptErrorList= {
        'JsonError': '初始化配置失败，请检查配置格式是否正确'
    }
    JsonError = 'JsonError'
    MoreValueFieldFormatError = "多值代码字段格式转Map失败 请检查上方数据"
    SingleOrMoreError = "判断单值/多值代码类型失败 请检查上方数据"
    YwlxRelationError = "多值代码业务类型对应关系报错,可能存在对应的业务类型没有迁移 请检查上方数据"
    JsonFormatError = "Json格式化失败，请检查上方数据报错位置是否存在多余空格或其他非法字符"
    GetSQLError = "拼接Sql失败 请检查上方数据"
    ExecuteSqlError = "执行Sql失败 请检查上方数据"
    StrLocalTime = str(time.strftime("_%Y_%m_%d", time.localtime() ))
    location = time.strftime("%Y-%m-%d", time.localtime())
    LogPath = 'Log'
    ProgramError = "ProgramError"
    DataError = 'DataError'
    SUCCESS = 'Success'
    GroupData = 'c_group'
    Debug = '1'
    Info = '2'
    Error = '3'

    def __init__(self):
        pass



