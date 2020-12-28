import time

import pymongo

from AT_02_Constant import Constants
from AT_05_Util import StrUtil


class CommonMongo(object):
    def __getattr__(self, item):
        return Constants.InsertError

    def __init__(self, Address, DBName, CollectionName, method, *args):
        self.MongoAddress = Address
        self.DBName = DBName
        self.CollectionName = CollectionName
        if len(args) > Constants.Zero:
            self.DataOne = args[Constants.Zero]
        self.method = method

    def client(self):
        try:
            mogoclient = pymongo.MongoClient(self.MongoAddress, port=27017)
            db = mogoclient[self.DBName]
            collection = db[self.CollectionName]
            if self.method == Constants.DeleteCon:
                collection.delete_many({})
            if self.method == Constants.Insert:
                if self.DataOne:
                    self.DataOne[Constants.ID] = StrUtil.get_uuid()
                    # JsonData = StrUtil.get_json_to_str(self.DataOne)
                    collection.insert(self.DataOne)
            if self.method == Constants.Patch:
                pass
            if self.method == Constants.Search:
                pass

        except Exception as e:
            print(e)
            pass


class DBDataCL(object):
    def __init__(self, Address, DBName, CollectionName1, CollectionName2):
        self.MongoAddress = Address
        self.DBName = DBName
        self.CollectionName1 = CollectionName1
        self.CollectionName2 = CollectionName2

    def update(self, key):
        mogoclient = pymongo.MongoClient(self.MongoAddress, port=27017)
        db1 = mogoclient[self.DBName]
        collection_1 = db1[self.CollectionName1]
        collection_2 = db1[self.CollectionName2]
        course = collection_1.find()
        for i, item in enumerate(course, 1):
            value = item.get(key)
            items = collection_2.find_one({key: value})
            if items:  # 找到了common 库中的数据
                collection_1.update({key: value}, {"$set": item})
                collection_1.update({key: value}, {"$set": {Constants.UpdateTime: time.time()}})
            else:
                print(Constants.ErrorMessage + item.get(Constants.FieldName))

    def extend(self, CollectionName3):
        mogoclient = pymongo.MongoClient(self.MongoAddress, port=27017)
        db1 = mogoclient[self.DBName]
        collection_1 = db1[self.CollectionName1]
        collection_2 = db1[self.CollectionName2]
        collection_3 = db1[CollectionName3]
        course = collection_1.find()
        course2 = collection_2.find()
        for i, item in enumerate(course, 1):
            collection_3.insert(item)
        for i, items in enumerate(course2, 1):
            collection_3.insert(items)