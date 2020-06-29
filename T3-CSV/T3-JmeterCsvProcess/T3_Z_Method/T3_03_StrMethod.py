# 这个是Python
import re
class StringMethod:
    pass


def replace_string(content, old, new, count):
    result = str(content).replace(old, new, count)
    return result


def spilt_string(value_description):
    spilt = re.split(",|，",value_description)
    if len(spilt) >= 2:
        ZWM = spilt[0]
        qt = spilt[1]
    else:
        ZWM = spilt[0]
        qt = ""
    return ZWM,qt
