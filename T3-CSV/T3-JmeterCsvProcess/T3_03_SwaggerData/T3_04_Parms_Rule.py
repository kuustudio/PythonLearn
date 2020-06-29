import re
from T3_Z_Method import RandomData
import uuid
import time


class ParmRule:
    pass


def patch_shu_x(SwaggerData):
    for item in SwaggerData:
        ZWM = item.get("ZWM")
        CD = item.get("vc")
        DM = item.get("single")
        LX = item.get("ft")
        ZD = item.get("name")
        if item.get("LX") == "ARRAY VC":
            item.update({"RCLX": "ARRAYVC"})
        elif re.search(r'案由', str(ZWM)) or re.search(r'罪名', str(ZWM)):
            item.update({"RCLX": "AY"})
        elif re.search(r'名称$', str(ZWM)) and CD == "600":
            item.update({"RCLX": "VC600"})
        elif re.search(r'1140', str(DM)):
            item.update({"RCLX": "单值代码"})
        elif LX == "DT":
            item.update({"RCLX": "时间戳"})
        elif re.search(r'日期$', str(ZWM)):
            item.update({"RCLX": "日期"})
        elif LX == "NUM":
            item.update({"RCLX": "NUM"})
        elif LX == "N":
            item.update({"RCLX": "N"})
        elif re.search(r'人', str(ZWM)) and not re.search(r'^bh', str(ZD)):
            item.update({"RCLX": "人员"})
        elif re.search(r'人', str(ZWM)) and re.search(r'^bh', str(ZD)):
            item.update({"RCLX": "UUID"})
        else:
            item.update({"RCLX": "VC100"})
    return SwaggerData


def DefaultValue(swagger_dict):
    ft = swagger_dict['f_type']
    if ft == 'VC100':
        value = RandomData.RandomData().RandomData(10)
        return value
    elif ft == "单值代码":
        value = str(1)
        return value
    elif ft == "ARRAYVC":
        value = [1, 2]
        return value
    elif ft == 'VC100':
        uid = str(uuid.uuid4())
        value = ''.join(uid.split('-'))
        return value
    elif ft == '日期' or ft == '时间戳':
        t = time.time()
        value = int(round(t * 1000))
        return value
    elif ft == 'VC600':
        value = RandomData.RandomData().RandomData(10)
        return value
    elif ft == 'AY':
        value = "AY"
        return value
    elif ft == 'N':
        value = 20
        return value
    else:
        uid = str(uuid.uuid4())
        value = ''.join(uid.split('-'))
        return value



