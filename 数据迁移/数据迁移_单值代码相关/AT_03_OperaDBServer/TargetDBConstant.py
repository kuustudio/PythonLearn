class Constant(object):
    conditions_single = "sjqy.t_sjqy_dzdm"
    conditions_field = "sjqy.t_sjqy_zdgx"
    GetSingleAllSql = "select * from " + conditions_single
    GetFieldAllSql = "select * from " + conditions_field
    GetSingleAllSqlMC = "获取单值代码表所有数据"
    GetSingleFieldList = [
        "c_target_ywlx","c_source_ywlx","c_target_zdm","c_source_zdm","c_target_dzdm","c_source_dzdm",
        "c_target_jtmz","c_source_jtmz",
    ]
    GetFieldRelation = "获取字段关系表所有数据"
    GetFieldList = ['c_target_bm',"c_ms","c_target_zd", "c_source_bm", "c_source_zd","c_system_type",
                    "c_target_dmlx","c_source_dmlx","c_target_zhl","c_group","c_sheet_mc","c_system_type",
                    "c_target_sjlx"]
    filter_target_field = "c_target_dmlx"
    filter_source_field = "c_source_dmlx"
    SystemMark = 'np'
    ay_mark = 'ay'
    FieldSystemMark = 'c_system_type'
    ExecuteSqlMark = "执行sql"

