"""  处理 swagger define key 下的数据"""
import re

from AT_02_Constant import Constants
from AT_04_Mongodb import Mongodb_client
from AT_05_Util import StrUtil


class GetDefineData(object):
    DefineKey = None  # 储存 define 的数据的key
    ResultData = Constants.EmptyDict  # 存储存入 数据库的最终数据 每次写入数据时候 要先删后插
    RequireList = None
    DVName = None  # 储存模板名称
    ModelProValue = None
    Pid = None
    Model = None # 存入模板名称（动态）

    def __getattr__(self, item):
        return "调用的属性异常"

    def __init__(self, data, model, api, common):
        self.data = data
        self.model = model
        self.api = api
        self.common = common
        # if isinstance(self.data, dict):
            # self.DefineKey =

    def get_define_data_main(self):
        """
        调用获取模板的方法
        根据传过来的模板数据获取该模板字段
        通过传过来的接口名关联接口 如果找不到 抛出异常
        """
        One_data = None
        if self.data.keys():
            if self.model:
                try:
                    ModelValue = self.data[self.model]
                    one_model_keys = ModelValue.keys()
                    if Constants.Require in one_model_keys:
                        self.RequireList = ModelValue[Constants.Require]
                    if Constants.Properties in one_model_keys:
                        self.ModelProValue = ModelValue[Constants.Properties]
                        if self.ModelProValue:
                            # 获取字段信息
                            One_data = self.get_properties_data()

                except KeyError as e:
                    print(e)
                    print(Constants.ErrorMessage)

            else:
                print()
        return One_data
    def get_properties_data(self) -> list:
        """
            格式化 DTO/VO 获取结果(使用模板...)
            使用循环
            :rtype list
        :return: 格式化结果[{}]
        """
        ResultDataList = Constants.EmptyList
        for one in self.ModelProValue:
            self.ResultData[Constants.Field] = one
            data = self.ModelProValue[one]
            try:
                # self.ResultData[Constants.DVName] = self.DVName
               #  self.ResultData[Constants.In] = Constants.Body
                if Constants.DataType in data.keys():
                    self.ResultData[Constants.DataType] = data[Constants.DataType]
                    self.ResultData[Constants.RRef] = self.model
                else:
                    if Constants.Ref in data.keys():
                        self.ResultData[Constants.DataType] = Constants.EmptyString
                        self.ResultData[Constants.RRef] = data[Constants.Ref]

                if Constants.Description in data.keys():
                    DescriptionList = re.split(Constants.DescriptionRule, data[Constants.Description])
                    self.ResultData[Constants.FieldName] = DescriptionList[Constants.Zero]
                    if len(DescriptionList) > Constants.One:
                        self.num_list = re.findall(Constants.NumRule, DescriptionList[Constants.One])
                        self.get_abbr_len()
                        self.num_list = Constants.EmptyString   # 赋值后情况该变量 每次循环赋值

                    else:
                        self.ResultData[Constants.Single] = Constants.EmptyString
                        self.ResultData[Constants.CD] = Constants.EmptyString
                    # self.ResultData[Constants.Pid] = self.Pid
                if self.RequireList:
                    if one not in self.RequireList:
                        self.ResultData[Constants.Require] = False
                    else:
                        self.ResultData[Constants.Require] = True
                self.ResultData[Constants.Summary] = self.api
                self.ResultData.update(self.common)
                # 存入list
                ResultDataList.append(self.ResultData)

                # MongoCon = Mongodb_client.CommonMongo(Constants.MongoAddress,Constants.MongoDB,
                #                                       Constants.CollectionNameDefine,Constants.Insert,self.ResultData)
                # MongoCon.client()
            except KeyError as e:
                print(one)
                print(data)
        return ResultDataList # 以模板为单位 --> 接口为单位  返回结果

    def get_abbr_len(self):
        """
        获取字段长度属性的方法
        如果 第一个元素 匹配1140 认为是 单值代码 直接长度赋值100  single为码值
        如果 第一个元素 是100 则直接赋值100 非码值
        如果 第一个元素 是600 则长度 600 非码值
        如果 第一个元素 是32 则长度 32 非码值

        :return:
        """
        if self.num_list:
            if re.search(Constants.SingleValueRule, self.num_list[Constants.Zero]):
                self.ResultData[Constants.Single] = self.num_list[Constants.Zero]
                self.ResultData[Constants.CD] = Constants.CD100
            elif re.search(Constants.CD100, self.num_list[Constants.Zero]):
                self.ResultData[Constants.CD] = Constants.CD100
                self.ResultData[Constants.Single] = Constants.EmptyString
            elif re.search(Constants.CD600, self.num_list[Constants.Zero]):
                self.ResultData[Constants.CD] = Constants.CD600
                self.ResultData[Constants.Single] = Constants.EmptyString
            elif re.search(Constants.CD32, self.num_list[Constants.Zero]):
                self.ResultData[Constants.CD] = Constants.CD32
                self.ResultData[Constants.Single] = Constants.EmptyString
            else:
                self.ResultData[Constants.CD] = Constants.EmptyString
                self.ResultData[Constants.Single] = Constants.EmptyString
        else:
            self.ResultData[Constants.Single] = Constants.EmptyString
            self.ResultData[Constants.CD] = Constants.EmptyString