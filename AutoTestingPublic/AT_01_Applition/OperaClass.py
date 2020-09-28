'''
操作类
'''
from AT_02_Constant import Constants
from AT_03_Server import GetSwaggerDataServer


class OperaClassApplication(object):
    def __int__(self):
        pass

    def main(self):
        GetSwaggerMethod = GetSwaggerDataServer.GetSwaggerDataServer()
        GetSwaggerMethod.util_main()
