# -*- coding: utf-8 -*-

# @Project      : 数据迁移_单值代码相关
# @File         : FilterRulesServer.py
# @Date         : 2020-11-25
# @Author       : Administrator
# @Introduce    : 该 Server 主要是用来过滤不需要进行测试的数据
# @Info         : 通过传入的 字段列表 和 码值列表 过滤所有需要过滤的数据
#               : 目前主要是案由(code) 文书 转换类（字段）

from AT_07_FilteringRules import FilterRulesConstant


class FilterDataServer(object):

    def __init__(self, data):
        self.data = data
        self.FC = FilterRulesConstant.RuleConstant()
        self.rule = self.FC.field_list_filter_map

    def main(self):
        for i in self.rule.keys():
            key = i
            value = self.rule[i]
            self.filter_data(key,value)
        return self.data

    def filter_data(self, key, value):
        """
        根据传入的key和value 过滤list数据
        :param key:
        :param value:
        """
        for i in self.data[:]:
            if value == self.FC.NotNull:
                if i[key]:
                    self.data.remove(i)
            else:
                if i[key] == value:
                    self.data.remove(i)


if __name__ == '__main__':

    pass