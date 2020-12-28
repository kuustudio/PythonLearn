# -*- coding: utf-8 -*-

# @Project  : 数据迁移_单值代码相关
# @File     : SqlServerConstant.py
# @Date     : 2020-11-30
# @Author   : Administrator
# @Info     :
# @Introduce:


class SqlConstant(object):

    flags = ' '
    equal_flags = '='
    point_flags = '.'
    quotes_flags = "'"
    left_braces = "{"
    right_braces = "}"
    TargetSchemaField = 'c_ms'
    TargetTableNameField = 'c_target_bm'
    CountSqlCommon = 'select count(*) as data_count from'
    bh_sql_common = 'select ywb.C_BH as data from'
    bhAj_sql_common = 'select aj.C_BH as data from'
    CommonConditions = 'where'
    TargetFieldName = 'c_target_zdm'
    TargetSingleName = 'c_target_jtmz'
    SourceTableNameField = 'c_source_bm'
    SourceFieldName = 'c_source_zdm'
    SourceSingleName = 'c_source_jtmz'
    Target = 'target'
    Source = 'source'
    SourceLB = 'c_source_ywlx'
    TargetLB = 'c_target_ywlx'
    TargetLX = 'c_target_sjlx'
    ALL = 'all'
    AND = 'AND'
    SheetMC = 'c_sheet_mc'
    SystemMC = 'c_system_type'
    GetScopeMark = "获取范围"
    LX = 'lx'
    Single = 'Single'

    # select count(*) from msaj.t_ms_aj_bg where c_ywlx = '0304'
