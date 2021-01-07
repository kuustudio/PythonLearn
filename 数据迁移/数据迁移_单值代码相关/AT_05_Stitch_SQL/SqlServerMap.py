# -*- coding: utf-8 -*-

# @Project  : 数据迁移_单值代码相关
# @File     : SqlServerMap.py
# @Date     : 2021-01-06
# @Author   : Administrator
# @Info     :
# @Introduce:
#
#
#
# select ywb.C_BH as data from  T_GX_SPZZCYBG AS ywb JOIN T_GX_AJ AS aj ON ywb.C_BH_AJ = aj.C_BH
from AT_05_Stitch_SQL import SqlServerConstant


sql_c = SqlServerConstant.SqlConstant()


class Map(object):

    def __init__(self,mark, table, schema):
        self.mark = mark
        self.table = table
        self.schema = schema

    def get_sql(self):
        bh_aj = 'c_bh_aj'
        if self.table == 'T_SX_HZSJ':
            bh_aj = 'c_bh_zt'
        if self.mark == 'MS':
            sql = 'select count(*) as data_count from ' + sql_c.flags + self.schema + sql_c.point_flags + self.table \
                  + sql_c.flags + 'AS ywb JOIN msaj.t_ms_aj_jc as aj ON ywb.' + bh_aj + '= aj.c_bh'
        elif self.mark == 'XS':
            sql = 'select count(*) as data_count from ' + sql_c.flags + self.schema + sql_c.point_flags + self.table \
                  + sql_c.flags + 'AS ywb JOIN xsaj.t_xs_aj_jc as aj ON ywb.' + bh_aj + '= aj.c_bh'
        else:
            x = str(self.mark).lower()
            sql = 'select count(*) as data_count from ' + sql_c.flags + self.schema + sql_c.point_flags + self.table \
                  + sql_c.flags + 'AS ywb JOIN aj.t_' + x + '_aj_jc as aj ON ywb.' + bh_aj + '= aj.c_bh'
        return sql
