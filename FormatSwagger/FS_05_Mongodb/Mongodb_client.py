import pymongo
import traceback


class MongoCLient(object):
    def __init__(self, DBName, CollectionName, Method, ListData):
        self.DB_name = DBName
        self.CollectionName = CollectionName
        self.Method = Method
        self.ListData = ListData
        pass

    def delete_data(self, collection):
        course_detail = collection.find({"_id":0})
        for detail in course_detail:
            print(detail)
            exit()
            if detail not in self.ListData:
                collection.delete_one(detail)

    def db_method(self, collection, Method):
        if Method == "insert":
            for i, item in enumerate(self.ListData, 1):
                if item:
                    server = item.get('swagger_name')
                    ZD = item.get("api_name")
                    controller = item.get('controller')
                    collection.insert({'server':server,'api':ZD,'controller':controller})
        if Method == "patch":
            for i, item in enumerate(self.ListData, 1):
                if item:
                    server = item.get('swagger_name')
                    ZD = item.get("api_name")
                    controller = item.get('controller')
                    collection.update({"api_name": str(ZD)}, {"$set": {"server":str(ZD),'api':server,'controller':controller}})
        if Method == "select":
            course_detail = collection.find({})

            for num, item in enumerate(course_detail, 1):
                table = item.get("swagger_name")
                ZD = item.get("api_name")
                # mark = item.get("mark")
                if table and ZD:
                    print(table + "\t" + ZD)

    def MongoCLient(self):
        try:
            mogoclient = pymongo.MongoClient("localhost", port=27017)
            db = mogoclient[self.DB_name]
            collection = db[self.CollectionName]
            # 删除 数据库多余字段
            self.delete_data(collection)
            for i, item in enumerate(self.ListData, 0):
                # 判断数据库中是否存在 如果存在 则更新 如果不存在就插入
                if item:
                    table = item.get("swagger_name")
                    ZD = item.get("api_name")
                    db_content = collection.find_one({"swagger_name": table}, {"api_name": ZD})
                    if not db_content:
                        self.db_method(collection, "insert")
                    else:
                        self.db_method(collection, "patch")
            self.db_method(collection,"select")

        except Exception as e:
            log = traceback.print_exc()
            print(log)
