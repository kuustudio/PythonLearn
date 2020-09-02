import re


def swagger_attribute_handle(data) -> dict:
    field_type = data['type']
    field_single = data['single']
    field_vc = data['vc']
    field_name = data['name']
    if field_type == 'array':
        if re.search(r'^1140', field_single):
            data["attribute"] = "多值代码"
            return data
        elif field_vc == '32':
            data["attribute"] = "多值编号"
            return data
        elif re.search(r'案由', field_name):
            data["attribute"] = "多值案由"
            return data

        else:
            data["attribute"] = "内嵌Json"
            return data
    if field_type == 'string':
        if re.search(r'^1140', field_single):
            data["attribute"] = "单值代码"
            return data
        if field_vc == "32":
            data["attribute"] = "UUID"
            return data
        if re.search(r'法院', field_name):
            data["attribute"] = "法院ID"
            return data
        if re.search(r'日期$', field_name):
            data["attribute"] = "Time"
            return data
        if field_vc == "600":
            data["attribute"] = "Text"
            return data

        if field_vc == "100" and re.search(r'人$', field_name):
            data["attribute"] = "组织机构人员"
            return data
        if field_vc == "100" and re.search('部门标识|庭室', field_name):
            data["attribute"] = "组织机构"
            return data
        elif re.search(r'案由', field_name):
            data["attribute"] = "多值案由"
            return data
        else:
            data["attribute"] = "其他"
            return data
    if field_type == "integer":
        data["attribute"] = "NUM"
        return data
    if field_type == "number":
        data["attribute"] = "float"
        return data
