from AT_00_SystemConstant import SystemConstant
from AT_04_DBDataProcess import ProcessConstant
from AT_08_Logging import LoggingServer
from AT_09_CommonMethod import CommonMethodServer
import re, copy, json, traceback, sys


class ProcessDataServer(object):
    ProcessConstantsMark = ProcessConstant.ProcessConstantServer
    SingleValueList = []
    MoreSingleValueList = []
    table_name = None
    target_code_type = None
    source_code_type = None
    code_data = None
    table_mark_dict = {}
    SingleValueAssembleSource = []
    case_type_list = []
    ErrorData = None

    def __init__(self, field_value_list, code_value_list):
        self.field_value_list = field_value_list
        self.code_value_list = code_value_list
        self.get_case_type_list()

    def __getattr__(self, item):
        return SystemConstant.ClassErrorMessage

    def code_classification(self):
        """
          之前已经排除掉是空的情况
          对 code码值进行分类 如果 Target 和 Source都是以数字开头的 或者是 单值代码
          否则是多值代码
        """

        for i in self.field_value_list:
            try:
                Target = i[self.ProcessConstantsMark.TargetCodeField]
                Source = i[self.ProcessConstantsMark.SourceCodeField]
                if re.search(r'^\d+', Target) and re.search(r'^\d+', Source):
                    self.SingleValueList.append(i)
                elif Source in ProcessConstant.ProcessConstantServer.special_target_single_list:
                    self.SingleValueList.append(i)
                else:
                    self.MoreSingleValueList.append(i)
            except TypeError as e:
                exc_type, exc_value, exc_tb = sys.exc_info()
                if SystemConstant.GroupData in self.ErrorData.keys():
                    Group = self.ErrorData[SystemConstant.GroupData]
                else:
                    Group = 'Common'
                file = LoggingServer.get_log_file(SystemConstant.ProgramError, Group)
                LoggingServer.program_error(exc_value, exc_type, file, SystemConstant.One, self.ErrorData,
                                            SystemConstant.SingleOrMoreError)

    def get_case_type_list(self):
        self.case_type_list = {}
        for i in self.code_value_list:
            if i[self.ProcessConstantsMark.SourceCodeType] == self.ProcessConstantsMark.SourceYwlxCodeType:
                self.case_type_list.update({i[self.ProcessConstantsMark.TargetCode]:
                                                i[self.ProcessConstantsMark.SourceCode]})


class HandleSingleValue(ProcessDataServer):
    # 处理单值代码
    def main(self):
        self.code_classification()
        self.handle_single_value()


        return self.SingleValueAssembleSource

    def handle_single_value(self):
        mark = "Single"
        a = []
        data = copy.deepcopy(self.SingleValueList)
        for i in data:
            if i['c_group'] == 'tj':
                a.append(i)
            self.ErrorData = i  # 如果报错则 log 打印这个 报错的数据信息和 报错原因
            self.table_name = i[self.ProcessConstantsMark.TargetSchemaField]
            self.target_code_type = i[self.ProcessConstantsMark.TargetCodeField]
            self.source_code_type = i[self.ProcessConstantsMark.SourceCodeField]
            TargetField = i[self.ProcessConstantsMark.TargetField]
            self.get_code_data(TargetField)
            common = CommonMethodServer.get_common(i)
            common.update({"lx":mark})
            handle_result = CommonMethodServer.add_comment_element(self.code_data, common)

            self.SingleValueAssembleSource.append(handle_result)

    def get_code_data(self, target_field):
        """
            根据 T3c(target)的模式名(c_ms) 和 T3c的码值code_type以及Np的code_type生成一套规则查找数据
            迁移的单值代码迁移规则
            可能存在 多个字段用一套码值 所以 需要加上字段名称 一起判断
        """

        self.code_data = None
        self.code_data = [i for i in self.code_value_list if
                          i[self.ProcessConstantsMark.TargetCodeType] == self.target_code_type
                          and i[self.ProcessConstantsMark.SourceCodeType] == self.source_code_type
                          and i["c_target_zdm"] == target_field]


class HandleMoreValue(HandleSingleValue):

    def main(self):
        print(len(self.SingleValueAssembleSource))
        self.code_classification()
        self.handle_more_value()

        return self.SingleValueAssembleSource

    def handle_more_value(self):
        mark = 'more'
        data = copy.deepcopy(self.MoreSingleValueList)
        for i in data:
            self.ErrorData = i
            # 对 source 和 target 拆分
            value_type_result = self.handle_value_type(i)
            if value_type_result:
                value_correspond = self.confirm_source_code_type(value_type_result)
                self.format_to_single_value(i, value_correspond)

    def format_to_single_value(self, data, value_correspond):
        """
        静态方法 根据 多值代码所在的字段信息数据 以及多值代码对应关系 生成多条与单值代码相同格式的数据返回
        :param data: 字段信息
        :param value_correspond: 多值代码对应关系
        :return 返回格式化数据
        :rtype 返回格式为数组
        """
        mark = 'more'
        for i in value_correspond:
            self.target_code_type = list(i.values())[SystemConstant.Zero]
            self.source_code_type = list(i.values())[SystemConstant.One]
            # self.code_data 所有的码值
            target_feild = data[self.ProcessConstantsMark.TargetField]
            self.get_code_data(target_feild)

            key_list = [self.ProcessConstantsMark.SourceYwlxField, self.ProcessConstantsMark.TargetYwlxField]
            value_list = [list(i.keys())[SystemConstant.One], list(i.keys())[SystemConstant.Zero]]
            # 获取 公共字段
            common = CommonMethodServer.get_common(data)
            common.update({"lx":mark})
            handle_result = CommonMethodServer.add_comment_element(self.code_data, common)
            if handle_result:
                if handle_result[0]["c_source_zdm"]== "C_SSDW":
                    print(handle_result)
            result = CommonMethodServer.change_dict_value(handle_result, key_list, value_list)
            self.SingleValueAssembleSource.append(result)
        return self.SingleValueAssembleSource

    def handle_value_type(self, data):
        """
           处理 多值代码的 c_target_dmlx的type
        """
        try:
            target = json.loads(str(data[ProcessConstant.ProcessConstantServer.TargetCodeField]).replace("\n", ""))

            source = json.loads(str(data[ProcessConstant.ProcessConstantServer.SourceCodeField]).replace("\n", ""))
            return target, source
        except json.decoder.JSONDecodeError as e :
            if SystemConstant.GroupData in self.ErrorData.keys():
                Group = self.ErrorData[SystemConstant.GroupData]
            else:
                Group = 'Common'
            exc_type, exc_value, exc_tb = sys.exc_info()
            file = LoggingServer.get_log_file(SystemConstant.ProgramError,Group)
            LoggingServer.program_error(exc_value,exc_type, file, SystemConstant.One, self.ErrorData,
                                        SystemConstant.MoreValueFieldFormatError, SystemConstant.JsonFormatError,
                                        )
        except Exception as e:
            if SystemConstant.GroupData in self.ErrorData.keys():
                Group = self.ErrorData[SystemConstant.GroupData]
            else:
                Group = 'Common'
            exc_type, exc_value, exc_tb = sys.exc_info()
            file = LoggingServer.get_log_file(SystemConstant.ProgramError,Group)
            LoggingServer.program_error(exc_value,exc_type,file, SystemConstant.One, self.ErrorData,
                                        SystemConstant.MoreValueFieldFormatError)
            # 需要数据写在log 日志中

    def confirm_source_code_type(self, value_list) -> list:
        """
            通过 11401179 与 code 在码值表中确认 source 业务类型 生成多值代码对应关系的list
            [{'0102': '11400108','10101': '10125025}]
        """

        target = self.get_more_code_relation(SystemConstant.Zero, value_list)
        source = self.get_more_code_relation(SystemConstant.One, value_list)
        relation = CommonMethodServer.extend_list_set(source, target)
        result = self.get_more_value_result(value_list, relation)

        return result

    def get_more_code_relation(self, mark, value_list) -> list:
        """
            根据传值的标识 确定 该多值代码 业务类型对应关系 返回 map
        :param mark: 标识 0 target 取 source ， 1 source 取 target
        :param value_list:  more code value
        :return
        :rtype list
        """
        code_relation_list = []
        if mark == SystemConstant.Zero:
            un_mark = SystemConstant.One
            data = value_list[mark]
            un_data = value_list[un_mark]
            for i in data:
                format_key = str(i)[1:2] + self.ProcessConstantsMark.SourceFormat
                un_key = self.get_one_code_relation(i, un_data, format_key, mark)
                if un_key:
                    except_map = {i: un_key}
                    if except_map not in code_relation_list:
                        code_relation_list.append(except_map)
        else:
            un_mark = SystemConstant.Zero
            data = value_list[mark]
            un_data = value_list[un_mark]
            for i in data:
                format_key = str(list(un_data.keys())[SystemConstant.Zero])[
                             0:2] + self.ProcessConstantsMark.TargetFormat
                un_key = self.get_one_code_relation(i, un_data, format_key, mark)
                if un_key:
                    except_map = {un_key: i}
                    if except_map not in code_relation_list:
                        code_relation_list.append(except_map)
        return code_relation_list

    def get_one_code_relation(self, key, un_data, format_key, mark) -> dict:
        """
        获取 单个 单值代码 业务类型关系的方法
        :param key:  针对于父方法传参 为多值代码字段格式化后的map的一个key
        :param un_data: 针对于父方法传参 多值代码 目标 map 例如 使用T3C 反推源库 则 传参为 源库所使用多值代码
        :param format_key:  目标map业务类型大类
        :param mark: 标记 0 为T3C 反推源库 1 为 源库推T3C
        :return: 返回为 dict  因为存在键值相同的情况
        :rtype dict
        """
        try:
            one_key = None
            if mark == SystemConstant.Zero:
                un_key = self.case_type_list[key]
            else:
                key_index = list(self.case_type_list.values()).index(key)
                un_key = list(self.case_type_list.keys())[key_index]
            if un_key:
                if un_key in un_data.keys():
                    one_key = un_key
                elif format_key in un_data.keys():
                    one_key = format_key
                else:
                    pass
            return one_key
        except ValueError as e:
            if SystemConstant.GroupData in self.ErrorData.keys():
                Group = self.ErrorData[SystemConstant.GroupData]
            else:
                Group = 'Common'
            exc_type, exc_value, exc_tb = sys.exc_info()
            file = LoggingServer.get_log_file(SystemConstant.ProgramError,Group)
            LoggingServer.program_error(exc_value, exc_type, file, SystemConstant.One, self.ErrorData,
                                        SystemConstant.YwlxRelationError)

    def get_more_value_result(self, value_list, code_relation):
        """
            根据code对应关系以及 value_list 获取多值代码的最终处理结果
        :param value_list:  字段的多值代码关系
        :param code_relation: 字段维度 业务类型对应关系
        """
        result = []
        for i in code_relation:
            try:
                one = {}
                target_ywlx = list(i.keys())[SystemConstant.Zero]
                source_ywlx = i[target_ywlx]
                one.update({target_ywlx: value_list[SystemConstant.Zero][target_ywlx]})
                one.update({source_ywlx: value_list[SystemConstant.One][source_ywlx]})
                result.append(one)
            except Exception as e:
                exc_type, exc_value, exc_tb = sys.exc_info()
                if SystemConstant.GroupData in self.ErrorData.keys():
                    Group = self.ErrorData[SystemConstant.GroupData]
                else:
                    Group = 'Common'
                file = LoggingServer.get_log_file(SystemConstant.ProgramError, Group)
                LoggingServer.program_error(exc_value, exc_type, file, SystemConstant.One, self.ErrorData,
                                            SystemConstant.YwlxRelationError,exc_type)

        return result
if __name__ == '__main__':
    data = {
    'c_sheet_mc': '民事当事人-sscyr',
    'c_ms': 'sscyr',
    'c_target_bm': 'T_MS_DSR',
    'c_target_zd': 'C_ESSSDW',
    'c_target_sjlx': '_varchar',
    'c_target_dmlx': '11400379',
    'c_target_zhl': None,
    'c_source_bm': 'T_MS_DSR',
    'c_source_zd': 'N_ESSSDW',
    'c_source_dmlx': '10103313',
    'c_system_type': 'np',
    'c_group': 'sscyr-民事'
}
