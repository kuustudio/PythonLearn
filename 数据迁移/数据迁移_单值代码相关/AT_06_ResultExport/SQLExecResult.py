# -*- coding: utf-8 -*-

# @Project  : 数据迁移_单值代码相关
# @File     : SQLExecResult.py
# @Date     : 2020-12-06
# @Author   : Administrator
# @Info     :
# @Introduce:

from AT_06_ResultExport import SqlConstant

ConstantClass = SqlConstant.SqlConstant()


class Sql(object):
    result = None

    def __init__(self, opera, data):
        self.opera = opera
        self.data = data

    def main(self):
        if self.opera == ConstantClass.GetScopeOpera:
            self.result = self.get_scope_sql()
        return self.result

    def get_scope_sql(self):
        sheetMC = self.data[ConstantClass.SheetMC]
        SystemMC = self.data[ConstantClass.SystemMC]
        GetScopeSql = "select c_sql ,c_where from sjqy.t_sjqy_sql where c_ofsheet_mc = '%s'" \
                      " and c_sql_type = 'MAINSQL' and c_system_type = '%s'" % (sheetMC, SystemMC)
        return GetScopeSql