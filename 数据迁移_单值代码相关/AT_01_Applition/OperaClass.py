'''
操作类
'''
from AT_02_Constant import Constants
from AT_03_Server import GetSwaggerDataServer
from AT_04_Mongodb import Mongodb_client


class OperaClassApplication(object):
    def __int__(self):
        pass

    def main(self):
        GetSwaggerMethod = GetSwaggerDataServer.GetSwaggerDataServer()
        # MongoCon = Mongodb_client.CommonMongo(Constants.MongoAddress, Constants.MongoDB,
        #                                       Constants.Collection, Constants.DeleteCon)
        # # 如果调用了这个方法  说明是要重新生成数据 需要将之前的数据清空
        # MongoCon.client()
        #
        # MongoConDefine = Mongodb_client.CommonMongo(Constants.MongoAddress, Constants.MongoDB,
        #                                             Constants.CollectionNameDefine, Constants.DeleteCon)
        # # 如果调用了这个方法  说明是要重新生成数据 需要将之前的数据清空
        # MongoConDefine.client()
        # MongoCommon = Mongodb_client.CommonMongo(Constants.MongoAddress, Constants.MongoDB,
        #                                          Constants.CollectionNameCommon, Constants.DeleteCon)
        # # 如果调用了这个方法  说明是要重新生成数据 需要将之前的数据清空
        # MongoCommon.client()
        #
        # MongoParm = Mongodb_client.CommonMongo(Constants.MongoAddress, Constants.MongoDB,
        #                                        Constants.CollectionNameParm, Constants.DeleteCon)
        # # 如果调用了这个方法  说明是要重新生成数据 需要将之前的数据清空
        # MongoCommon.client()
        GetSwaggerMethod.util_main()
        #
        # DBFormatCollectionNameParm = Mongodb_client.DBDataCL(Constants.MongoAddress, Constants.MongoDB,
        #                                                      Constants.CollectionNameParm,
        #                                                      Constants.CollectionNameCommon)
        # DBFormatCollectionNameParm.update(Constants.Summary)

        # DBFormatCollectionNameParm = Mongodb_client.DBDataCL(Constants.MongoAddress, Constants.MongoDB,
        #                                                      Constants.CollectionNameDefine,
        #                                                      Constants.CollectionNameCommon)
        # DBFormatCollectionNameParm.update(Constants.R)

