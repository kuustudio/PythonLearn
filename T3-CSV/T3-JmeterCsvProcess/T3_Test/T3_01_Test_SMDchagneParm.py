from T3_02_ReadConfig import T3_01_ReadConfig
from T3_Z_Method import Method
import re
import json


class SmdChangeParm:

    def __init__(self, address, name, sheetname, title_row, start_row):
        self.address = address
        self.name = name
        self.sheetname = sheetname
        self.title_row = title_row
        self.start_row = start_row
        print("开始转化文件:%s" % name)

    def get_smd_data(self):
        data = Method.get_one_smd_data(self.address, self.sheetname, self.title_row, self.start_row)

    def __str__(self):
        return "文件[%s]转化完成" % self.name


config_path = T3_01_ReadConfig.spilt_config_path("Z-Config", "ChangeSmdToJson.txt")
dict_config_content = T3_01_ReadConfig.get_config_content(config_path)
json_file = "C:\\Users\\Administrator\\Desktop\\json.txt"
file = open(json_file, "a+", encoding="UTF-8")
file.truncate()
smd_address = dict_config_content["address"]
smd_name = dict_config_content["name"]
result = Method.get_one_smd_data(smd_address, "COL", 0, 1)
data_list = []
for item in result:
    key = item["表名"]
    value = item["字段"]
    data_list.append(value)

patten_rule = r'[\u4e00-\u9fa5]+'
num_list = []
for item in data_list:
    if re.search(patten_rule, item):
        num_list.append(data_list.index(item))
num = len(num_list)
print(num)
c = []
for i in num_list:
    a = num_list.index(i)
    if a < num - 1:
        b = (data_list[i + 1:num_list[a + 1]])
        for j in b:
            d = str(j).split("_", 1)
            g = len(d)
            if g > 1:
                f = d[1].lower()
            else:
                f = d[0].lower()
            b[b.index(j)] = f
        c.append(b)
for m in c:
    dict_1 = {}
    for n in m:
        dict_1[n] = "${" + n + "}"
    json_data = json.dumps(dict_1, indent=4)
    json_file = "C:\\Users\\Administrator\\Desktop\\json.txt"
    file = open(json_file, "a+", encoding="UTF-8")
    file.truncate()
    file.write(json_data)
    file.close()

