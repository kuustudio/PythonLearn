class SmdData:
    pass


def get_need_data_list(data_list):
    need_list = []
    for item in data_list:
        need_dict = {}
        if item["字段中文名"] != "":
            table = item["表名"]
            name_s = item["字段"]
            single_s = item['代码类型']
            field_type = item['数据类型']
            single = str(str(single_s).split(".", 1)[0])

            name_list = name_s.split("_", 1)
            if len(name_list) >= 2:
                name = str(name_list[1]).lower()
            else:
                name = str(name_list[0]).lower()

            vcs = item.get("数据长度")
            vc = str(str(vcs).split(".", 1)[0])
            sm = item.get("说明")
            need_dict["ZWM"] = item["字段中文名"]
            need_dict["name"] = name
            need_dict["vc"] = vc
            need_dict["table"] = table
            need_dict["sm"] = sm
            need_dict['single'] = single
            need_dict['field_type'] = field_type
            need_list.append(need_dict)
    return need_list


def get_more_value_single(content, rule):
    for i in content:
        data = i[rule]


def get_compare_data(need_list, DB_table):
    compare_data = []
    for i in need_list:
        j = i["table"]
        if j == DB_table:
            compare_data.append(i)
    return compare_data


def get_comment_data(swagger, ZDM, ft):
    for item in swagger:
        ZWM = item["ZWM"]
        if ZWM == ZDM:
            item['ft'] = ft
            return item
        else:
            pass
    if ZDM:
        return ZDM


def write_error_file(error):
    error_address = "C:\\Users\\Administrator\\Desktop\\Error.txt"
    file = open(error_address, "a+", encoding="UTF-8")
    file.write(error)
    file.write("\n")
    file.close()


def Compare_data(smd_data, swagger_data):
    for item in smd_data:
        ZDM = item["ZWM"]
        table = item["table"]
        Smd_vc = item["vc"]
        Smd_name = item['name']
        Smd_single = item['single']
        Smd_field_type = item['field_type']
        swagger = get_comment_data(swagger_data, ZDM, Smd_field_type)
        if swagger == ZDM:
            error = table + "\t" + ZDM + "\t" + "没有找到相同字段名的字段"
            write_error_file(error)
        else:
            Swagger_vc = swagger['vc']
            if Swagger_vc == Smd_vc:
                pass
            else:
                error = table + "\t" + ZDM + "\t" + "字段长度不同" + "\t" + Smd_vc + "\t" + Swagger_vc
                write_error_file(error)
            Swagger_name = swagger['name']
            if Swagger_name == Smd_name:
                pass
            else:
                error = table + "\t" + ZDM + "\t" + "字段名不同" + "\t" + Smd_name + "\t" + Swagger_name
                write_error_file(error)
            if Smd_single != '':
                swagger_single = swagger['single']
                if swagger_single == Smd_single:
                    pass
                else:
                    error = table + "\t" + ZDM + "\t" + "单值代码注释问题" + "\t" + Smd_single + "\t" + swagger_single
                    write_error_file(error)
    return swagger_data
