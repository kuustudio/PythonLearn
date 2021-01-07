# -*- coding: utf-8 -*-

# @Project  : 数据迁移_单值代码相关
# @File     : SQLServer.py
# @Date     : 2020-11-29
# @Author   : Administrator
# @Info     : 根据 ProcessServer处理后的数据 循环生成SQL List 结果为 [x{{T3C,NP},{T3C,NP}}]
# @Introduce:
import copy, sys, traceback, re, psycopg2
from AT_00_SystemConstant import SystemConstant
from AT_05_Stitch_SQL import SqlServerConstant, SqlServerMap
from AT_03_OperaDBServer import TargetDBServer, TargetDBConstant
from AT_06_ResultExport import SQLExecResult
from AT_08_Logging import LoggingServer
from AT_04_DBDataProcess import ProcessConstant
from AT_02_ExportOutInputData import ExportOutDataServer, ExportOutDataConstant

sql_constant = SqlServerConstant.SqlConstant()

ProcessConstantClass = ProcessConstant.ProcessConstantServer()


class GetSql(object):
    OneData = None
    TargetData = None
    SourceData = None
    target_count_sql = None
    source_count_sql = None
    ErrorData = None
    target_sql = None
    source_sql = None
    one_data = None
    source_conditions = []
    target_conditions = []
    search_bh = False
    ConfigData = None
    my_table = None
    count_result = None
    target_count_result = None
    source_count_result = None
    OnceTarget = None
    OnceSource = None
    Already = None
    data_mark_list = []

    def __init__(self, format_data, db_info, mark):
        self.format_data = format_data
        self.db_info = db_info
        self.mark = mark
        self.TargetDB = TargetDBServer.TargetDB(self.db_info[SystemConstant.targetDB], self.mark)
        self.SourceDB = TargetDBServer.SourceDB(self.db_info[SystemConstant.sourceDB])

    def main(self):
        """
            主方法
            1 循环 得到的数据 取得第一条数据 获取公共拼接字段
            2 循环得到码值的对应关系
            3 生成对应的数据
        """
        data = copy.deepcopy(self.format_data)
        for one_data in data:
            if one_data:
                self.one_data = one_data
                # 判断是不是已经比较过
                mark_result = self.get_data_mark()
                if mark_result:
                    for target_data in one_data:
                        self.OneData = target_data
                        # 获取T3C公共部分
                        self.get_target_common_data()
                        # 获取NP 公共部分
                        self.get_source_common_data()
                        #  获取T3C 以及 NP where 条件
                        conditions_list = self.get_target_conditions()
                        # 区分一对多和 一对一
                        self.between_more_single(conditions_list)
                        # 生成 count sql
                        self.get_count_sql(conditions_list)
                        # 执行 count SQL 获取数量

                        # 因为内部是获取了所有的 条件 所以 这个方法执行后需要跳出循环
                        self.source_conditions = []
                        break
                    self.source_count_sql = None

    def get_data_mark(self):
        """
            @info: 获取跑过数据的标识 如果用来判断 如果已经跑过 则不需要再次执行
        """
        if isinstance(self.one_data[SystemConstant.Zero], dict):
            data_json = copy.deepcopy(self.one_data[SystemConstant.Zero])
            target_single = data_json.pop(sql_constant.TargetSingleName)
            source_single = data_json.pop(sql_constant.SourceSingleName)
            if data_json not in self.data_mark_list:
                self.data_mark_list.append(data_json)
                return self.data_mark_list
            else:
                return None

    def between_more_single(self, conditions_list):
        """
            区分条件 将所有需要累加的条件放在一起 后期请求出的数据会累加
        """
        # for i in conditions_list:
        pass

    def get_count_sql(self, conditions_list):

        for one_conditions in conditions_list:
            # 获取每次执行SQL 使用的码值 赋值后返回 作为logger打印的必要元素
            try:
                self.OnceTarget = (str(one_conditions[sql_constant.Target]).split("="))[1]
                self.OnceSource = (str(one_conditions[sql_constant.Source]).split("="))[1]
            except Exception:
                pass
            target = sql_constant.flags + sql_constant.AND + sql_constant.flags + one_conditions[sql_constant.Target]
            source = sql_constant.flags + sql_constant.AND + sql_constant.flags + self.my_table \
                     + sql_constant.point_flags + one_conditions[sql_constant.Source]
            self.target_count_sql = copy.deepcopy(self.target_sql)
            self.source_count_sql = copy.deepcopy(self.source_sql)
            self.target_count_sql += target
            self.source_count_sql += source
            self.count_result = self.perform_sql('count')
            # 根据情况执行 编号SQL
            self.get_bh_sql()

    def get_target_common_data(self):
        """
        @info: 获取 T3C 公共SQL 赋值给 target sql
        select * from .schema table name .
        """
        self.target_sql = sql_constant.CountSqlCommon + sql_constant.flags \
                          + self.OneData[sql_constant.TargetSchemaField] + sql_constant.point_flags \
                          + self.OneData[sql_constant.TargetTableNameField] \
                          + sql_constant.flags

    def get_source_common_data(self):
        """
            @info: 获取 NP 的公共部分
        """
        self.get_source_data_scope()

        # select count(*) as  source_count from YWST.dbo.T_XZ_TZZXXZXW where 'N_TZZXQDFS' = '10102499'"

    def get_source_data_scope(self):
        """
            @info  根据 sheet 名称 去SQL 表中查询 迁移数据的范围
        """
        GetSqlClass = SQLExecResult.Sql(sql_constant.GetScopeMark, self.OneData)
        self.TargetDB.opera = sql_constant.GetScopeMark
        self.TargetDB.sql = GetSqlClass.main()
        self.TargetDB.main()
        sql_result = copy.deepcopy(self.TargetDB.cur.fetchall())
        if sql_result:
            if len(sql_result[SystemConstant.Zero]) > SystemConstant.One:
                if sql_result[SystemConstant.Zero][SystemConstant.One]:
                    if sql_result[SystemConstant.Zero][SystemConstant.One] != 'NULL':
                        self.source_conditions.append(sql_result[SystemConstant.Zero][SystemConstant.One])
            # 如果长度大于1 则代表着 where条件存在数据 NP SQL的 where 条件直接 使用 数据库中的数据拼接 将得到的where条件
            # 直接放到 要拼接的条件中

        # 原始的迁移SQL
        self.source_sql = sql_result[SystemConstant.Zero][SystemConstant.Zero]
        # 如果原始的迁移SQL 不存在 则使用新拼接的SQL
        if not self.source_sql:
            self.source_sql = sql_constant.CountSqlCommon + sql_constant.flags + SystemConstant.SourceDBName \
                              + sql_constant.point_flags + \
                              SystemConstant.SourceDBSchema + sql_constant.point_flags \
                              + self.OneData[sql_constant.SourceTableNameField] + sql_constant.flags + \
                              sql_constant.CommonConditions

        self.deal_source_sql()

    def deal_source_sql(self):
        """
        处理从数据迁移库中得到的SQL
        拼接 where条件
        1 获取 配置的公共 where 条件列表
        2  拼接 where 条件
        """
        Config = ExportOutDataServer.ExportOutData(ExportOutDataConstant.Constant.DirName,
                                                   ExportOutDataConstant.Constant.FileName)
        self.ConfigData = Config.export_main()
        SourceCommonConditions = self.ConfigData[SystemConstant.sourceDB]['CommonWhere']
        TargetCommonConditions = self.ConfigData[SystemConstant.targetDB]['CommonWhere']
        self.target_conditions.extend(TargetCommonConditions)
        self.source_conditions.extend(SourceCommonConditions)
        self.deal_more_single()
        sql_list = None
        # 处理 单值多值代码拼接SQL
        # 业务类型 多值代码  不是all 和 案件类别标志结尾的
        # 放到 target 和 source 中
        source_finally_conditions = ""
        for one in set(self.source_conditions):
            conn = copy.deepcopy(one)
            # 如果其他或者请示答复类案件 需要将收案时间转化为aj.DT_DJSJ
            if ("T_QT_" in self.OneData[sql_constant.SourceTableNameField]
            ) or ("T_QSDF_" in self.OneData[sql_constant.SourceTableNameField]):
                conn = str(one).replace("SASJ", "DJSJ")
            if self.source_conditions.index(one) == SystemConstant.Zero:
                source_finally_conditions += "Where "
                source_finally_conditions += str(conn)
            else:
                source_finally_conditions += "AND "
                source_finally_conditions += str(conn)
        if self.source_sql:
            # 兼容 from From 之前没有兼容 这个
            sql_list = re.split("FROM|from", self.source_sql)
        if self.search_bh is False and sql_list:
            self.source_sql = sql_constant.CountSqlCommon + " " + sql_list[SystemConstant.One] + " " + \
                              source_finally_conditions

        target_finally_conditions = ""

        for one in set(self.target_conditions):
            if self.target_conditions.index(one) == SystemConstant.Zero:
                target_finally_conditions += "Where "
                target_finally_conditions += str(one)
            else:
                target_finally_conditions += "AND "
                target_finally_conditions += str(one)
        self.target_sql += target_finally_conditions
        if self.search_bh is False:
            self.source_sql = sql_constant.CountSqlCommon + " " + sql_list[SystemConstant.One] + " " + \
                              source_finally_conditions


        else:
            pass

    def get_target_conditions(self):
        conditions_list = []
        for one in self.one_data:
            # 排除码值是空的情况
            if one[sql_constant.TargetSingleName] and one[sql_constant.SourceSingleName]:
                self.ErrorData = one
                self.deal_my_conditions()
                target_conditions_value = None
                target_conditions = None
                try:
                    target_conditions_key = one[sql_constant.TargetFieldName] \
                                            + sql_constant.flags + sql_constant.equal_flags \
                                            + sql_constant.flags
                    if one[sql_constant.TargetLX] == '_varchar':
                        # 数组 target 码值全是 varchar, 只验证 单个码值的 不验证多个 技术原因 后期优化 sybase
                        # target_conditions = one[sql_constant.TargetFieldName]\
                        #                      + "@> ARRAY[" + sql_constant.quotes_flags+one[sql_constant.TargetSingleName]\
                        #                      + sql_constant.quotes_flags + "] :: VARCHAR []"
                        target_conditions_value = sql_constant.quotes_flags + sql_constant.left_braces + one[
                            sql_constant.TargetSingleName] + sql_constant.right_braces + sql_constant.quotes_flags
                    else:
                        target_conditions_value = sql_constant.quotes_flags + one[
                            sql_constant.TargetSingleName] + sql_constant.quotes_flags
                    if target_conditions_key and target_conditions_value:
                        target_conditions = target_conditions_key + target_conditions_value
                    source_conditions_key = one[sql_constant.SourceFieldName] \
                                            + sql_constant.flags + sql_constant.equal_flags \
                                            + sql_constant.flags
                    if "N_" in one[sql_constant.SourceFieldName]:
                        source_conditions_value = str(one[sql_constant.SourceSingleName])
                    else:
                        source_conditions_value = sql_constant.quotes_flags + one[
                            sql_constant.SourceSingleName] + sql_constant.quotes_flags
                    source_conditions = source_conditions_key + source_conditions_value
                    if target_conditions and source_conditions:
                        conditions_list.append({'target': target_conditions, 'source': source_conditions})
                except TypeError as e:
                    if SystemConstant.GroupData in self.ErrorData.keys():
                        Group = self.ErrorData[SystemConstant.GroupData]
                    else:
                        Group = 'Common'
                    exc_type, exc_value, exc_tb = sys.exc_info()
                    file = LoggingServer.get_log_file(SystemConstant.DataError, Group)
                    LoggingServer.program_error(exc_value, exc_type, file, SystemConstant.One, self.ErrorData,
                                                SystemConstant.GetSQLError
                                                )
                except Exception as e:
                    if SystemConstant.GroupData in self.ErrorData.keys():
                        Group = self.ErrorData[SystemConstant.GroupData]
                    else:
                        Group = 'Common'
                    exc_type, exc_value, exc_tb = sys.exc_info()
                    file = LoggingServer.get_log_file(SystemConstant.DataError, Group)
                    LoggingServer.program_error(exc_value, exc_type, file, SystemConstant.One, self.ErrorData,
                                                SystemConstant.GetSQLError)

        return conditions_list

    def deal_more_single(self):
        """
            处理多值代码的 条件拼接
        """
        target_conditions = None
        source_conditions = None
        if self.OneData[sql_constant.TargetLB] != sql_constant.ALL:
            if not str(self.OneData[sql_constant.TargetLB]).endswith(ProcessConstantClass.TargetFormat):
                target_conditions = "C_YWLX = " + "'" + self.OneData[sql_constant.TargetLB] + "'"
            if self.OneData[sql_constant.SourceLB] != sql_constant.ALL:
                if not str(self.OneData[sql_constant.TargetLB]).endswith(ProcessConstantClass.SourceFormat):
                    source_conditions = "aj.N_YWLX = " + str(self.OneData[sql_constant.SourceLB])
        if target_conditions:
            self.target_conditions.append(target_conditions)
        if source_conditions:
            self.source_conditions.append(source_conditions)

    def deal_my_conditions(self):
        """
            处理 自己拼接的where条件
            1 如果是业务类型 则 source 为 int
            2 区分 接 aj 还是 业务表
        """
        if str(self.OneData[sql_constant.SourceTableNameField]).endswith("_AJ"):
            self.my_table = "aj"
        else:
            self.my_table = "ywb"

    def perform_sql(self, mark):
        # 在执行SQL前 最后处理一遍 生成的SQL 保证没有任何问题
        if mark == 'count':
            self.deal_finally_sql()
        target_result = None
        try:
            if mark == 'count':
                self.TargetDB.sql = copy.deepcopy(self.target_count_sql)
                self.TargetDB.main()
                target_row = self.TargetDB.cur.fetchall()
                target_result = target_row[SystemConstant.Zero][SystemConstant.Zero]
                # int 0  也代表不存在

            self.SourceDB.sql = copy.deepcopy(self.source_count_sql)
            self.SourceDB.main()
            source_row = self.SourceDB.cur.fetchall()
            if mark == 'count':
                source_result = source_row[SystemConstant.Zero][SystemConstant.Zero]
            else:
                source_result = source_row[SystemConstant.Zero]
            if mark == 'bh':
                self.TargetDB.sql = copy.deepcopy(self.target_count_sql)
                self.TargetDB.main()
                target_row = self.TargetDB.cur.fetchall()
                target_result = target_row[SystemConstant.Zero][SystemConstant.Zero]
            if target_result or target_result == SystemConstant.Zero:
                return target_result, source_result
            else:
                return source_result

        except Exception as e:
            sql = {SystemConstant.targetDB: self.target_count_sql, SystemConstant.sourceDB: self.source_count_sql}
            if SystemConstant.GroupData in self.ErrorData.keys():
                Group = self.ErrorData[SystemConstant.GroupData]
            else:
                Group = 'Common'
            exc_type, exc_value, exc_tb = sys.exc_info()
            file = LoggingServer.get_log_file(SystemConstant.DataError, Group)
            LoggingServer.program_error(exc_value, exc_type, file, SystemConstant.One, self.ErrorData,
                                        SystemConstant.ExecuteSqlError, sql)
            self.TargetDB.conn.rollback()

    def get_bh_sql(self):

        self.ErrorData[sql_constant.TargetSingleName] = self.OnceTarget
        self.ErrorData[sql_constant.SourceSingleName] = self.OnceSource
        sql = {SystemConstant.targetDB: self.target_count_sql, SystemConstant.sourceDB: self.source_count_sql}
        if self.count_result:
            self.target_count_result = self.count_result[SystemConstant.Zero]
            self.source_count_result = self.count_result[SystemConstant.One]
        if self.target_count_result and self.source_count_result:
            if self.target_count_result < self.source_count_result:  # 数量不等 且小于等于 拼接 编号sql
                if self.count_result:
                    if self.target_count_result == SystemConstant.Zero:
                        Error = "T3C.%s.%s数量为%s,NP.%s.%s数量为%s,请检查生成Sql确定是否迁移问题" % (
                            self.OneData[sql_constant.TargetTableNameField],
                            self.OneData[sql_constant.TargetFieldName],
                            self.count_result[SystemConstant.Zero],
                            self.OneData[sql_constant.SourceTableNameField],
                            self.OneData[sql_constant.SourceFieldName],
                            self.count_result[SystemConstant.One])

                        try:
                            raise ValueError(Error)
                        except ValueError as e:
                            if SystemConstant.GroupData in self.ErrorData.keys():
                                Group = self.ErrorData[SystemConstant.GroupData]
                            else:
                                Group = 'Common'
                            exc_type, exc_value, exc_tb = sys.exc_info()
                            file = LoggingServer.get_log_file(SystemConstant.DataError, Group)
                            LoggingServer.program_error(exc_value, exc_type, file, SystemConstant.One, self.ErrorData,
                                                        Error, sql
                                                        )
                    elif self.source_count_result == SystemConstant.Zero:
                        Error = "T3C.%s.%s数量为%s,NP.%s.%s数量为%s,请检查生成Sql确定是否迁移问题" % (
                            self.OneData[sql_constant.TargetTableNameField],
                            self.OneData[sql_constant.TargetFieldName],
                            self.count_result[SystemConstant.Zero],
                            self.OneData[sql_constant.SourceTableNameField],
                            self.OneData[sql_constant.SourceFieldName],
                            self.count_result[SystemConstant.One])
                        try:
                            raise ValueError(Error)
                        except ValueError as e:
                            if SystemConstant.GroupData in self.ErrorData.keys():
                                Group = self.ErrorData[SystemConstant.GroupData]
                            else:
                                Group = 'Common'
                            exc_type, exc_value, exc_tb = sys.exc_info()
                            file = LoggingServer.get_log_file(SystemConstant.DataError, Group)
                            LoggingServer.program_error(exc_value, exc_type, file, SystemConstant.One, self.ErrorData,
                                                        Error, sql
                                                        )
                        except TypeError as e:
                            print(e)
                    else:
                        # 如果没有是0的 则 需要验证source 数据库中在 target 库中
                        source_bh_sql = ""
                        if isinstance(self.source_count_sql, str):
                            # 不能使用 这个判断 用表名
                            if "_AJ" in self.ErrorData[sql_constant.SourceTableNameField]:
                                source_bh_sql = str(self.source_count_sql).replace(sql_constant.CountSqlCommon,
                                                                                   sql_constant.bhAj_sql_common)
                            else:
                                source_bh_sql = str(self.source_count_sql).replace(sql_constant.CountSqlCommon,
                                                                                   sql_constant.bh_sql_common)
                            self.source_count_sql = copy.deepcopy(source_bh_sql)

                            bh_source_list = self.perform_sql('qt')
                            if bh_source_list:
                                for one_bh in bh_source_list:
                                    if "_AJ" in self.ErrorData[sql_constant.SourceTableNameField] and "_AJ_JC" not in \
                                            self.ErrorData[sql_constant.TargetTableNameField]:
                                        self.target_count_sql += " and 'C_BH_AJ' =" + \
                                                                 sql_constant.quotes_flags + one_bh + \
                                                                 sql_constant.quotes_flags
                                    else:
                                        self.target_count_sql += " and 'C_BH' =" + \
                                                                 sql_constant.quotes_flags + one_bh + \
                                                                 sql_constant.quotes_flags
                                    target_count = self.perform_sql('bh')
                                    if target_count[SystemConstant.Zero] == SystemConstant.Zero:
                                        sql = {SystemConstant.targetDB: self.target_count_sql,
                                               SystemConstant.sourceDB: source_bh_sql}
                                        bh_error = "T3C.%s表中没有找到与NP.%s表中编号为%s的数据 请检查上方SQL是否正确" % (
                                            self.OneData[sql_constant.TargetTableNameField],
                                            self.OneData[sql_constant.SourceTableNameField],
                                            target_count[SystemConstant.One][SystemConstant.Zero]
                                        )
                                        try:
                                            raise ValueError(bh_error)
                                        except ValueError as e:
                                            if SystemConstant.GroupData in self.ErrorData.keys():
                                                Group = self.ErrorData[SystemConstant.GroupData]
                                            else:
                                                Group = 'Common'
                                            exc_type, exc_value, exc_tb = sys.exc_info()
                                            file = LoggingServer.get_log_file(SystemConstant.DataError, Group)
                                            LoggingServer.program_error(exc_value, exc_type, file, SystemConstant.One,
                                                                        self.ErrorData,
                                                                        bh_error, sql
                                                                        )


            else:

                SUCCESS = "执行成功！！！！！"
                a = "T3C表名%s,字段名%s,码值%s,NP表名%s,字段名%s,码值%s," % (self.OneData[sql_constant.TargetTableNameField],
                                                               self.OneData[sql_constant.TargetFieldName],
                                                               str(self.OnceTarget),
                                                               self.OneData[sql_constant.SourceTableNameField],
                                                               self.OneData[sql_constant.SourceFieldName],
                                                               str(self.OnceSource)

                                                               )
                try:
                    raise ValueError(a)
                except ValueError as e:
                    if SystemConstant.GroupData in self.ErrorData.keys():
                        Group = self.ErrorData[SystemConstant.GroupData]
                    else:
                        Group = 'Common'
                    exc_type, exc_value, exc_tb = sys.exc_info()
                    file = LoggingServer.get_log_file(SystemConstant.SUCCESS, Group)
                    LoggingServer.program_error(exc_value, exc_type, file, SystemConstant.One, SUCCESS,
                                                )

    def deal_ywlx_conditions(self, sql_source_list):
        """
        @INFO: 根据 source SQL 中 业务类型的限制情况 获取 target SQL 的业务类型限制情况
        :param sql_source_list:
        """
        result = None
        finally_result = []
        if sql_source_list:
            for condition in sql_source_list:
                if 'N_YWLX' in condition:
                    deal_data = copy.deepcopy(condition)
                    target_data = deal_data.replace('N_YWLX', 'C_YWLX')
                    source_ywlx = re.findall(r'\d+', deal_data)
                    if SystemConstant.ywlx_map:
                        ywlx_map = SystemConstant.ywlx_map
                    else:
                        ywlx_map = sql_constant.ywlx_map
                    if source_ywlx:
                        for one_ywlx in source_ywlx:
                            if one_ywlx in ywlx_map.keys():
                                if ywlx_map[one_ywlx]:
                                    # 获取T3C码值
                                    target_one_ywlx = sql_constant.quotes_flags + ywlx_map[one_ywlx] + \
                                                      sql_constant.quotes_flags
                                    if target_one_ywlx:
                                        if one_ywlx in target_data:
                                            target_data = target_data.replace(one_ywlx, target_one_ywlx)
                                else:
                                    target_data = target_data.replace(one_ywlx, '')
                    result_list = target_data.split(',')

                    if result_list:
                        result = ','.join([x for x in result_list if x != ''])
                        result = result.replace(",)", ")")
                    del_aj_res = result.split('aj.')

                    finally_result.append(del_aj_res[SystemConstant.One])
        return finally_result

    def deal_finally_sql(self):

        """
        执行SQL前最后处理一遍SQL 保证SQL准确性
        """
        # 如果 source SQL 中存在存在 其他案件的 直接把 收案时间改掉
        ywlx_conditions = None
        if "T_QSDF_" in self.source_count_sql or "T_QT_" in self.source_count_sql:
            self.source_count_sql = self.source_count_sql.replace("SASJ", "DJSJ")
        # 不能用长度判断 可能存在 NULL
        sql_source_list = re.split("Where|AND|and", self.source_count_sql)
        ajlb = re.findall('JOIN T_(.*?)_AJ', str(sql_source_list[SystemConstant.Zero]))
        if ajlb and ajlb in sql_constant.LB:
            ywlx_conditions = self.deal_ywlx_conditions(sql_source_list)
        sql_target_list = re.split("Where|where|AND|and", self.target_count_sql)
        # 如果元素中存在 业务类型= 且为单值代码 直接删掉该数据
        if self.OneData[sql_constant.LX] == sql_constant.Single:
            for x in sql_target_list[:]:
                # 存在 边长 null  这种情况暂不处理
                # 存在 业务类型的且不是测试业务类型字段的单值代码数据 删除
                # 存在 业务类型 需要 转换该条件 放到 target 中
                if 'C_YWLX' in x and len(sql_target_list) > 3:
                    sql_target_list.remove(x)
                # 格式化 源库SQL 替换 \n
                if "\n  " in x:
                    y = x.replace("\n   ", " ")
                    sql_target_list[sql_target_list.index(x)] = y
                if len(x.split("=")) == 2:
                    if x.split('=')[SystemConstant.One].count("'") > 2:
                        z = x.split('=')[SystemConstant.One].replace("'", "")
                        if z:
                            y = x.split('=')[SystemConstant.Zero] + "=" + "'" + str(z).replace(" ", "") + "'"
                            sql_target_list[sql_target_list.index(x)] = y
        if ywlx_conditions:
            sql_target_list.extend(ywlx_conditions)
        target_list = None
        # 根据 source 获取 target 连表查询SQL
        if 'aj.' in self.source_count_sql and '_jc' not in self.OneData[sql_constant.TargetTableNameField]:
            target_list = self.deal_target_sql(sql_target_list, sql_source_list[SystemConstant.Zero])
        if 'JOIN' not in sql_source_list[SystemConstant.Zero]:
            copy_data = None
            for source in sql_source_list[:]:
                if 'ywb.' in source:
                    copy_data = copy.deepcopy(source)
                if 'aj.' in source or 'ywb.' in source:
                    sql_source_list.remove(source)
                if copy_data:
                    sql_source_list.append(copy_data.split('.')[SystemConstant.One])
        self.source_count_sql = self.get_finally_sql(sql_source_list)
        self.target_count_sql = self.get_finally_sql(target_list)
        print(self.target_count_sql)
        print(self.source_count_sql)
        exit()

    def deal_target_sql(self, target, source):
        """
            @INFO: 根据 source 第一个元素 修改 target的第一个元素 （案件表联查）
                    然后 target  子表为ywb aj 表 为aj ；
                    除了业务类型外 其他字段 前加ywb 业务类型为aj表
        :param source: 第一个元素
        :param target:
        :return:
        """
        target_index_one = None
        schema = self.OneData[sql_constant.TargetSchemaField]
        table = self.OneData[sql_constant.TargetTableNameField]
        for i, item in enumerate(target):
            if i == SystemConstant.Zero:
                table_list = re.findall('JOIN T_(.*?)_AJ', str(source))
                if table_list and table_list[SystemConstant.Zero] in sql_constant.LB:
                    source_aj_table = table_list[SystemConstant.Zero]
                    Map = SqlServerMap.Map(source_aj_table, table, schema)
                    if source_aj_table in sql_constant.LB:
                        target_index_one = Map.get_sql()
                        target[i] = target_index_one
            elif 'C_YWLX' in item:
                if target_index_one:
                    target[i] = ' aj.' + str(item)
            else:
                if target_index_one:
                    target[i] = ' ywb.' + str(item)
        return target

    @staticmethod
    def get_finally_sql(sql_source_list):
        if sql_source_list:
            first = sql_source_list[SystemConstant.Zero] + sql_constant.flags + \
                    sql_constant.CommonConditions + sql_constant.flags+ \
                    sql_source_list[SystemConstant.One] + sql_constant.flags

            if len(sql_source_list)>=3:
                first += sql_constant.AND
            second = ' AND '.join(sql_source_list[2:])
            result = first + second
            if result:
                return result


if __name__ == '__main__':
    d = [[{'c_target_ywlx': 'all', 'c_source_ywlx': 'all', 'c_target_zdm': 'C_XB', 'c_source_zdm': 'N_XB',
           'c_target_dzdm': '11400000', 'c_source_dzdm': '10100003', 'c_target_jtmz': '1', 'c_source_jtmz': '1',
           'c_sheet_mc': '审判组织成员人民陪审员-spzzcy', 'c_ms': 'spzzcy', 'c_target_bm': 'T_SPZZCY_RMPSY',
           'c_target_sjlx': 'varchar', 'c_source_bm': 'T_YWGY_RMPSY', 'c_system_type': 'np', 'c_group': 'spzzcy',
           'lx': 'Single'},
          {'c_target_ywlx': 'all', 'c_source_ywlx': 'all', 'c_target_zdm': 'C_XB', 'c_source_zdm': 'N_XB',
           'c_target_dzdm': '11400000', 'c_source_dzdm': '10100003', 'c_target_jtmz': '2', 'c_source_jtmz': '2',
           'c_sheet_mc': '审判组织成员人民陪审员-spzzcy', 'c_ms': 'spzzcy', 'c_target_bm': 'T_SPZZCY_RMPSY',
           'c_target_sjlx': 'varchar', 'c_source_bm': 'T_YWGY_RMPSY', 'c_system_type': 'np', 'c_group': 'spzzcy',
           'lx': 'Single'},
          {'c_target_ywlx': 'all', 'c_source_ywlx': 'all', 'c_target_zdm': 'C_XB', 'c_source_zdm': 'N_XB',
           'c_target_dzdm': '11400000', 'c_source_dzdm': '10100003', 'c_target_jtmz': '9', 'c_source_jtmz': None,
           'c_sheet_mc': '审判组织成员人民陪审员-spzzcy', 'c_ms': 'spzzcy', 'c_target_bm': 'T_SPZZCY_RMPSY',
           'c_target_sjlx': 'varchar', 'c_source_bm': 'T_YWGY_RMPSY', 'c_system_type': 'np', 'c_group': 'spzzcy',
           'lx': 'Single'},
          {'c_target_ywlx': 'all', 'c_source_ywlx': 'all', 'c_target_zdm': 'C_XB', 'c_source_zdm': 'N_XB',
           'c_target_dzdm': '11400000', 'c_source_dzdm': '10100003', 'c_target_jtmz': '0', 'c_source_jtmz': '255',
           'c_sheet_mc': '审判组织成员人民陪审员-spzzcy', 'c_ms': 'spzzcy', 'c_target_bm': 'T_SPZZCY_RMPSY',
           'c_target_sjlx': 'varchar', 'c_source_bm': 'T_YWGY_RMPSY', 'c_system_type': 'np', 'c_group': 'spzzcy',
           'lx': 'Single'},
          {'c_target_ywlx': 'all', 'c_source_ywlx': 'all', 'c_target_zdm': 'C_XB', 'c_source_zdm': 'N_XB',
           'c_target_dzdm': '11400000', 'c_source_dzdm': '10100003', 'c_target_jtmz': '0', 'c_source_jtmz': '0',
           'c_sheet_mc': '审判组织成员人民陪审员-spzzcy', 'c_ms': 'spzzcy', 'c_target_bm': 'T_SPZZCY_RMPSY',
           'c_target_sjlx': 'varchar', 'c_source_bm': 'T_YWGY_RMPSY', 'c_system_type': 'np', 'c_group': 'spzzcy',
           'lx': 'Single'}], [
             {'c_target_ywlx': 'all', 'c_source_ywlx': 'all', 'c_target_zdm': 'C_XB', 'c_source_zdm': 'N_XB',
              'c_target_dzdm': '11400000', 'c_source_dzdm': '10100003', 'c_target_jtmz': '1', 'c_source_jtmz': '1',
              'c_sheet_mc': '审判组织成员人民陪审员-spzzcy', 'c_ms': 'spzzcy', 'c_target_bm': 'T_SPZZCY_RMPSY',
              'c_target_sjlx': 'varchar', 'c_source_bm': 'T_YWGY_RMPSY', 'c_system_type': 'np', 'c_group': 'spzzcy',
              'lx': 'Single'},
             {'c_target_ywlx': 'all', 'c_source_ywlx': 'all', 'c_target_zdm': 'C_XB', 'c_source_zdm': 'N_XB',
              'c_target_dzdm': '11400000', 'c_source_dzdm': '10100003', 'c_target_jtmz': '2', 'c_source_jtmz': '2',
              'c_sheet_mc': '审判组织成员人民陪审员-spzzcy', 'c_ms': 'spzzcy', 'c_target_bm': 'T_SPZZCY_RMPSY',
              'c_target_sjlx': 'varchar', 'c_source_bm': 'T_YWGY_RMPSY', 'c_system_type': 'np', 'c_group': 'spzzcy',
              'lx': 'Single'},
             {'c_target_ywlx': 'all', 'c_source_ywlx': 'all', 'c_target_zdm': 'C_XB', 'c_source_zdm': 'N_XB',
              'c_target_dzdm': '11400000', 'c_source_dzdm': '10100003', 'c_target_jtmz': '9', 'c_source_jtmz': None,
              'c_sheet_mc': '审判组织成员人民陪审员-spzzcy', 'c_ms': 'spzzcy', 'c_target_bm': 'T_SPZZCY_RMPSY',
              'c_target_sjlx': 'varchar', 'c_source_bm': 'T_YWGY_RMPSY', 'c_system_type': 'np', 'c_group': 'spzzcy',
              'lx': 'Single'},
             {'c_target_ywlx': 'all', 'c_source_ywlx': 'all', 'c_target_zdm': 'C_XB', 'c_source_zdm': 'N_XB',
              'c_target_dzdm': '11400000', 'c_source_dzdm': '10100003', 'c_target_jtmz': '0', 'c_source_jtmz': '255',
              'c_sheet_mc': '审判组织成员人民陪审员-spzzcy', 'c_ms': 'spzzcy', 'c_target_bm': 'T_SPZZCY_RMPSY',
              'c_target_sjlx': 'varchar', 'c_source_bm': 'T_YWGY_RMPSY', 'c_system_type': 'np', 'c_group': 'spzzcy',
              'lx': 'Single'},
             {'c_target_ywlx': 'all', 'c_source_ywlx': 'all', 'c_target_zdm': 'C_XB', 'c_source_zdm': 'N_XB',
              'c_target_dzdm': '11400000', 'c_source_dzdm': '10100003', 'c_target_jtmz': '0', 'c_source_jtmz': '0',
              'c_sheet_mc': '审判组织成员人民陪审员-spzzcy', 'c_ms': 'spzzcy', 'c_target_bm': 'T_SPZZCY_RMPSY',
              'c_target_sjlx': 'varchar', 'c_source_bm': 'T_YWGY_RMPSY', 'c_system_type': 'np', 'c_group': 'spzzcy',
              'lx': 'Single'}], [
             {'c_target_ywlx': 'all', 'c_source_ywlx': 'all', 'c_target_zdm': 'C_XB', 'c_source_zdm': 'N_XB',
              'c_target_dzdm': '11400000', 'c_source_dzdm': '10100003', 'c_target_jtmz': '1', 'c_source_jtmz': '1',
              'c_sheet_mc': '审判组织成员人民陪审员-spzzcy', 'c_ms': 'spzzcy', 'c_target_bm': 'T_SPZZCY_RMPSY',
              'c_target_sjlx': 'varchar', 'c_source_bm': 'T_YWGY_RMPSY', 'c_system_type': 'np', 'c_group': 'spzzcy',
              'lx': 'Single'},
             {'c_target_ywlx': 'all', 'c_source_ywlx': 'all', 'c_target_zdm': 'C_XB', 'c_source_zdm': 'N_XB',
              'c_target_dzdm': '11400000', 'c_source_dzdm': '10100003', 'c_target_jtmz': '2', 'c_source_jtmz': '2',
              'c_sheet_mc': '审判组织成员人民陪审员-spzzcy', 'c_ms': 'spzzcy', 'c_target_bm': 'T_SPZZCY_RMPSY',
              'c_target_sjlx': 'varchar', 'c_source_bm': 'T_YWGY_RMPSY', 'c_system_type': 'np', 'c_group': 'spzzcy',
              'lx': 'Single'},
             {'c_target_ywlx': 'all', 'c_source_ywlx': 'all', 'c_target_zdm': 'C_XB', 'c_source_zdm': 'N_XB',
              'c_target_dzdm': '11400000', 'c_source_dzdm': '10100003', 'c_target_jtmz': '9', 'c_source_jtmz': None,
              'c_sheet_mc': '审判组织成员人民陪审员-spzzcy', 'c_ms': 'spzzcy', 'c_target_bm': 'T_SPZZCY_RMPSY',
              'c_target_sjlx': 'varchar', 'c_source_bm': 'T_YWGY_RMPSY', 'c_system_type': 'np', 'c_group': 'spzzcy',
              'lx': 'Single'},
             {'c_target_ywlx': 'all', 'c_source_ywlx': 'all', 'c_target_zdm': 'C_XB', 'c_source_zdm': 'N_XB',
              'c_target_dzdm': '11400000', 'c_source_dzdm': '10100003', 'c_target_jtmz': '0', 'c_source_jtmz': '255',
              'c_sheet_mc': '审判组织成员人民陪审员-spzzcy', 'c_ms': 'spzzcy', 'c_target_bm': 'T_SPZZCY_RMPSY',
              'c_target_sjlx': 'varchar', 'c_source_bm': 'T_YWGY_RMPSY', 'c_system_type': 'np', 'c_group': 'spzzcy',
              'lx': 'Single'},
             {'c_target_ywlx': 'all', 'c_source_ywlx': 'all', 'c_target_zdm': 'C_XB', 'c_source_zdm': 'N_XB',
              'c_target_dzdm': '11400000', 'c_source_dzdm': '10100003', 'c_target_jtmz': '0', 'c_source_jtmz': '0',
              'c_sheet_mc': '审判组织成员人民陪审员-spzzcy', 'c_ms': 'spzzcy', 'c_target_bm': 'T_SPZZCY_RMPSY',
              'c_target_sjlx': 'varchar', 'c_source_bm': 'T_YWGY_RMPSY', 'c_system_type': 'np', 'c_group': 'spzzcy',
              'lx': 'Single'}], [
             {'c_target_ywlx': 'all', 'c_source_ywlx': 'all', 'c_target_zdm': 'C_XB', 'c_source_zdm': 'N_XB',
              'c_target_dzdm': '11400000', 'c_source_dzdm': '10100003', 'c_target_jtmz': '1', 'c_source_jtmz': '1',
              'c_sheet_mc': '审判组织成员人民陪审员-spzzcy', 'c_ms': 'spzzcy', 'c_target_bm': 'T_SPZZCY_RMPSY',
              'c_target_sjlx': 'varchar', 'c_source_bm': 'T_YWGY_RMPSY', 'c_system_type': 'np', 'c_group': 'spzzcy',
              'lx': 'Single'},
             {'c_target_ywlx': 'all', 'c_source_ywlx': 'all', 'c_target_zdm': 'C_XB', 'c_source_zdm': 'N_XB',
              'c_target_dzdm': '11400000', 'c_source_dzdm': '10100003', 'c_target_jtmz': '2', 'c_source_jtmz': '2',
              'c_sheet_mc': '审判组织成员人民陪审员-spzzcy', 'c_ms': 'spzzcy', 'c_target_bm': 'T_SPZZCY_RMPSY',
              'c_target_sjlx': 'varchar', 'c_source_bm': 'T_YWGY_RMPSY', 'c_system_type': 'np', 'c_group': 'spzzcy',
              'lx': 'Single'},
             {'c_target_ywlx': 'all', 'c_source_ywlx': 'all', 'c_target_zdm': 'C_XB', 'c_source_zdm': 'N_XB',
              'c_target_dzdm': '11400000', 'c_source_dzdm': '10100003', 'c_target_jtmz': '9', 'c_source_jtmz': None,
              'c_sheet_mc': '审判组织成员人民陪审员-spzzcy', 'c_ms': 'spzzcy', 'c_target_bm': 'T_SPZZCY_RMPSY',
              'c_target_sjlx': 'varchar', 'c_source_bm': 'T_YWGY_RMPSY', 'c_system_type': 'np', 'c_group': 'spzzcy',
              'lx': 'Single'},
             {'c_target_ywlx': 'all', 'c_source_ywlx': 'all', 'c_target_zdm': 'C_XB', 'c_source_zdm': 'N_XB',
              'c_target_dzdm': '11400000', 'c_source_dzdm': '10100003', 'c_target_jtmz': '0', 'c_source_jtmz': '255',
              'c_sheet_mc': '审判组织成员人民陪审员-spzzcy', 'c_ms': 'spzzcy', 'c_target_bm': 'T_SPZZCY_RMPSY',
              'c_target_sjlx': 'varchar', 'c_source_bm': 'T_YWGY_RMPSY', 'c_system_type': 'np', 'c_group': 'spzzcy',
              'lx': 'Single'},
             {'c_target_ywlx': 'all', 'c_source_ywlx': 'all', 'c_target_zdm': 'C_XB', 'c_source_zdm': 'N_XB',
              'c_target_dzdm': '11400000', 'c_source_dzdm': '10100003', 'c_target_jtmz': '0', 'c_source_jtmz': '0',
              'c_sheet_mc': '审判组织成员人民陪审员-spzzcy', 'c_ms': 'spzzcy', 'c_target_bm': 'T_SPZZCY_RMPSY',
              'c_target_sjlx': 'varchar', 'c_source_bm': 'T_YWGY_RMPSY', 'c_system_type': 'np', 'c_group': 'spzzcy',
              'lx': 'Single'}], [
             {'c_target_ywlx': 'all', 'c_source_ywlx': 'all', 'c_target_zdm': 'C_XB', 'c_source_zdm': 'N_XB',
              'c_target_dzdm': '11400000', 'c_source_dzdm': '10100003', 'c_target_jtmz': '1', 'c_source_jtmz': '1',
              'c_sheet_mc': '审判组织成员人民陪审员-spzzcy', 'c_ms': 'spzzcy', 'c_target_bm': 'T_SPZZCY_RMPSY',
              'c_target_sjlx': 'varchar', 'c_source_bm': 'T_YWGY_RMPSY', 'c_system_type': 'np', 'c_group': 'spzzcy',
              'lx': 'Single'},
             {'c_target_ywlx': 'all', 'c_source_ywlx': 'all', 'c_target_zdm': 'C_XB', 'c_source_zdm': 'N_XB',
              'c_target_dzdm': '11400000', 'c_source_dzdm': '10100003', 'c_target_jtmz': '2', 'c_source_jtmz': '2',
              'c_sheet_mc': '审判组织成员人民陪审员-spzzcy', 'c_ms': 'spzzcy', 'c_target_bm': 'T_SPZZCY_RMPSY',
              'c_target_sjlx': 'varchar', 'c_source_bm': 'T_YWGY_RMPSY', 'c_system_type': 'np', 'c_group': 'spzzcy',
              'lx': 'Single'},
             {'c_target_ywlx': 'all', 'c_source_ywlx': 'all', 'c_target_zdm': 'C_XB', 'c_source_zdm': 'N_XB',
              'c_target_dzdm': '11400000', 'c_source_dzdm': '10100003', 'c_target_jtmz': '9', 'c_source_jtmz': None,
              'c_sheet_mc': '审判组织成员人民陪审员-spzzcy', 'c_ms': 'spzzcy', 'c_target_bm': 'T_SPZZCY_RMPSY',
              'c_target_sjlx': 'varchar', 'c_source_bm': 'T_YWGY_RMPSY', 'c_system_type': 'np', 'c_group': 'spzzcy',
              'lx': 'Single'},
             {'c_target_ywlx': 'all', 'c_source_ywlx': 'all', 'c_target_zdm': 'C_XB', 'c_source_zdm': 'N_XB',
              'c_target_dzdm': '11400000', 'c_source_dzdm': '10100003', 'c_target_jtmz': '0', 'c_source_jtmz': '255',
              'c_sheet_mc': '审判组织成员人民陪审员-spzzcy', 'c_ms': 'spzzcy', 'c_target_bm': 'T_SPZZCY_RMPSY',
              'c_target_sjlx': 'varchar', 'c_source_bm': 'T_YWGY_RMPSY', 'c_system_type': 'np', 'c_group': 'spzzcy',
              'lx': 'Single'},
             {'c_target_ywlx': 'all', 'c_source_ywlx': 'all', 'c_target_zdm': 'C_XB', 'c_source_zdm': 'N_XB',
              'c_target_dzdm': '11400000', 'c_source_dzdm': '10100003', 'c_target_jtmz': '0', 'c_source_jtmz': '0',
              'c_sheet_mc': '审判组织成员人民陪审员-spzzcy', 'c_ms': 'spzzcy', 'c_target_bm': 'T_SPZZCY_RMPSY',
              'c_target_sjlx': 'varchar', 'c_source_bm': 'T_YWGY_RMPSY', 'c_system_type': 'np', 'c_group': 'spzzcy',
              'lx': 'Single'}], [
             {'c_target_ywlx': 'all', 'c_source_ywlx': 'all', 'c_target_zdm': 'C_XB', 'c_source_zdm': 'N_XB',
              'c_target_dzdm': '11400000', 'c_source_dzdm': '10100003', 'c_target_jtmz': '1', 'c_source_jtmz': '1',
              'c_sheet_mc': '审判组织成员人民陪审员-spzzcy', 'c_ms': 'spzzcy', 'c_target_bm': 'T_SPZZCY_RMPSY',
              'c_target_sjlx': 'varchar', 'c_source_bm': 'T_YWGY_RMPSY', 'c_system_type': 'np', 'c_group': 'spzzcy',
              'lx': 'Single'},
             {'c_target_ywlx': 'all', 'c_source_ywlx': 'all', 'c_target_zdm': 'C_XB', 'c_source_zdm': 'N_XB',
              'c_target_dzdm': '11400000', 'c_source_dzdm': '10100003', 'c_target_jtmz': '2', 'c_source_jtmz': '2',
              'c_sheet_mc': '审判组织成员人民陪审员-spzzcy', 'c_ms': 'spzzcy', 'c_target_bm': 'T_SPZZCY_RMPSY',
              'c_target_sjlx': 'varchar', 'c_source_bm': 'T_YWGY_RMPSY', 'c_system_type': 'np', 'c_group': 'spzzcy',
              'lx': 'Single'},
             {'c_target_ywlx': 'all', 'c_source_ywlx': 'all', 'c_target_zdm': 'C_XB', 'c_source_zdm': 'N_XB',
              'c_target_dzdm': '11400000', 'c_source_dzdm': '10100003', 'c_target_jtmz': '9', 'c_source_jtmz': None,
              'c_sheet_mc': '审判组织成员人民陪审员-spzzcy', 'c_ms': 'spzzcy', 'c_target_bm': 'T_SPZZCY_RMPSY',
              'c_target_sjlx': 'varchar', 'c_source_bm': 'T_YWGY_RMPSY', 'c_system_type': 'np', 'c_group': 'spzzcy',
              'lx': 'Single'},
             {'c_target_ywlx': 'all', 'c_source_ywlx': 'all', 'c_target_zdm': 'C_XB', 'c_source_zdm': 'N_XB',
              'c_target_dzdm': '11400000', 'c_source_dzdm': '10100003', 'c_target_jtmz': '0', 'c_source_jtmz': '255',
              'c_sheet_mc': '审判组织成员人民陪审员-spzzcy', 'c_ms': 'spzzcy', 'c_target_bm': 'T_SPZZCY_RMPSY',
              'c_target_sjlx': 'varchar', 'c_source_bm': 'T_YWGY_RMPSY', 'c_system_type': 'np', 'c_group': 'spzzcy',
              'lx': 'Single'},
             {'c_target_ywlx': 'all', 'c_source_ywlx': 'all', 'c_target_zdm': 'C_XB', 'c_source_zdm': 'N_XB',
              'c_target_dzdm': '11400000', 'c_source_dzdm': '10100003', 'c_target_jtmz': '0', 'c_source_jtmz': '0',
              'c_sheet_mc': '审判组织成员人民陪审员-spzzcy', 'c_ms': 'spzzcy', 'c_target_bm': 'T_SPZZCY_RMPSY',
              'c_target_sjlx': 'varchar', 'c_source_bm': 'T_YWGY_RMPSY', 'c_system_type': 'np', 'c_group': 'spzzcy',
              'lx': 'Single'}], [
             {'c_target_ywlx': 'all', 'c_source_ywlx': 'all', 'c_target_zdm': 'C_XB', 'c_source_zdm': 'N_XB',
              'c_target_dzdm': '11400000', 'c_source_dzdm': '10100003', 'c_target_jtmz': '1', 'c_source_jtmz': '1',
              'c_sheet_mc': '审判组织成员人民陪审员-spzzcy', 'c_ms': 'spzzcy', 'c_target_bm': 'T_SPZZCY_RMPSY',
              'c_target_sjlx': 'varchar', 'c_source_bm': 'T_YWGY_RMPSY', 'c_system_type': 'np', 'c_group': 'spzzcy',
              'lx': 'Single'},
             {'c_target_ywlx': 'all', 'c_source_ywlx': 'all', 'c_target_zdm': 'C_XB', 'c_source_zdm': 'N_XB',
              'c_target_dzdm': '11400000', 'c_source_dzdm': '10100003', 'c_target_jtmz': '2', 'c_source_jtmz': '2',
              'c_sheet_mc': '审判组织成员人民陪审员-spzzcy', 'c_ms': 'spzzcy', 'c_target_bm': 'T_SPZZCY_RMPSY',
              'c_target_sjlx': 'varchar', 'c_source_bm': 'T_YWGY_RMPSY', 'c_system_type': 'np', 'c_group': 'spzzcy',
              'lx': 'Single'},
             {'c_target_ywlx': 'all', 'c_source_ywlx': 'all', 'c_target_zdm': 'C_XB', 'c_source_zdm': 'N_XB',
              'c_target_dzdm': '11400000', 'c_source_dzdm': '10100003', 'c_target_jtmz': '9', 'c_source_jtmz': None,
              'c_sheet_mc': '审判组织成员人民陪审员-spzzcy', 'c_ms': 'spzzcy', 'c_target_bm': 'T_SPZZCY_RMPSY',
              'c_target_sjlx': 'varchar', 'c_source_bm': 'T_YWGY_RMPSY', 'c_system_type': 'np', 'c_group': 'spzzcy',
              'lx': 'Single'},
             {'c_target_ywlx': 'all', 'c_source_ywlx': 'all', 'c_target_zdm': 'C_XB', 'c_source_zdm': 'N_XB',
              'c_target_dzdm': '11400000', 'c_source_dzdm': '10100003', 'c_target_jtmz': '0', 'c_source_jtmz': '255',
              'c_sheet_mc': '审判组织成员人民陪审员-spzzcy', 'c_ms': 'spzzcy', 'c_target_bm': 'T_SPZZCY_RMPSY',
              'c_target_sjlx': 'varchar', 'c_source_bm': 'T_YWGY_RMPSY', 'c_system_type': 'np', 'c_group': 'spzzcy',
              'lx': 'Single'},
             {'c_target_ywlx': 'all', 'c_source_ywlx': 'all', 'c_target_zdm': 'C_XB', 'c_source_zdm': 'N_XB',
              'c_target_dzdm': '11400000', 'c_source_dzdm': '10100003', 'c_target_jtmz': '0', 'c_source_jtmz': '0',
              'c_sheet_mc': '审判组织成员人民陪审员-spzzcy', 'c_ms': 'spzzcy', 'c_target_bm': 'T_SPZZCY_RMPSY',
              'c_target_sjlx': 'varchar', 'c_source_bm': 'T_YWGY_RMPSY', 'c_system_type': 'np', 'c_group': 'spzzcy',
              'lx': 'Single'}], [
             {'c_target_ywlx': 'all', 'c_source_ywlx': 'all', 'c_target_zdm': 'C_XB', 'c_source_zdm': 'N_XB',
              'c_target_dzdm': '11400000', 'c_source_dzdm': '10100003', 'c_target_jtmz': '1', 'c_source_jtmz': '1',
              'c_sheet_mc': '审判组织成员人民陪审员-spzzcy', 'c_ms': 'spzzcy', 'c_target_bm': 'T_SPZZCY_RMPSY',
              'c_target_sjlx': 'varchar', 'c_source_bm': 'T_YWGY_RMPSY', 'c_system_type': 'np', 'c_group': 'spzzcy',
              'lx': 'Single'},
             {'c_target_ywlx': 'all', 'c_source_ywlx': 'all', 'c_target_zdm': 'C_XB', 'c_source_zdm': 'N_XB',
              'c_target_dzdm': '11400000', 'c_source_dzdm': '10100003', 'c_target_jtmz': '2', 'c_source_jtmz': '2',
              'c_sheet_mc': '审判组织成员人民陪审员-spzzcy', 'c_ms': 'spzzcy', 'c_target_bm': 'T_SPZZCY_RMPSY',
              'c_target_sjlx': 'varchar', 'c_source_bm': 'T_YWGY_RMPSY', 'c_system_type': 'np', 'c_group': 'spzzcy',
              'lx': 'Single'},
             {'c_target_ywlx': 'all', 'c_source_ywlx': 'all', 'c_target_zdm': 'C_XB', 'c_source_zdm': 'N_XB',
              'c_target_dzdm': '11400000', 'c_source_dzdm': '10100003', 'c_target_jtmz': '9', 'c_source_jtmz': None,
              'c_sheet_mc': '审判组织成员人民陪审员-spzzcy', 'c_ms': 'spzzcy', 'c_target_bm': 'T_SPZZCY_RMPSY',
              'c_target_sjlx': 'varchar', 'c_source_bm': 'T_YWGY_RMPSY', 'c_system_type': 'np', 'c_group': 'spzzcy',
              'lx': 'Single'},
             {'c_target_ywlx': 'all', 'c_source_ywlx': 'all', 'c_target_zdm': 'C_XB', 'c_source_zdm': 'N_XB',
              'c_target_dzdm': '11400000', 'c_source_dzdm': '10100003', 'c_target_jtmz': '0', 'c_source_jtmz': '255',
              'c_sheet_mc': '审判组织成员人民陪审员-spzzcy', 'c_ms': 'spzzcy', 'c_target_bm': 'T_SPZZCY_RMPSY',
              'c_target_sjlx': 'varchar', 'c_source_bm': 'T_YWGY_RMPSY', 'c_system_type': 'np', 'c_group': 'spzzcy',
              'lx': 'Single'},
             {'c_target_ywlx': 'all', 'c_source_ywlx': 'all', 'c_target_zdm': 'C_XB', 'c_source_zdm': 'N_XB',
              'c_target_dzdm': '11400000', 'c_source_dzdm': '10100003', 'c_target_jtmz': '0', 'c_source_jtmz': '0',
              'c_sheet_mc': '审判组织成员人民陪审员-spzzcy', 'c_ms': 'spzzcy', 'c_target_bm': 'T_SPZZCY_RMPSY',
              'c_target_sjlx': 'varchar', 'c_source_bm': 'T_YWGY_RMPSY', 'c_system_type': 'np', 'c_group': 'spzzcy',
              'lx': 'Single'}], [
             {'c_target_ywlx': 'all', 'c_source_ywlx': 'all', 'c_target_zdm': 'C_XB', 'c_source_zdm': 'N_XB',
              'c_target_dzdm': '11400000', 'c_source_dzdm': '10100003', 'c_target_jtmz': '1', 'c_source_jtmz': '1',
              'c_sheet_mc': '审判组织成员人民陪审员-spzzcy', 'c_ms': 'spzzcy', 'c_target_bm': 'T_SPZZCY_RMPSY',
              'c_target_sjlx': 'varchar', 'c_source_bm': 'T_YWGY_RMPSY', 'c_system_type': 'np', 'c_group': 'spzzcy',
              'lx': 'Single'},
             {'c_target_ywlx': 'all', 'c_source_ywlx': 'all', 'c_target_zdm': 'C_XB', 'c_source_zdm': 'N_XB',
              'c_target_dzdm': '11400000', 'c_source_dzdm': '10100003', 'c_target_jtmz': '2', 'c_source_jtmz': '2',
              'c_sheet_mc': '审判组织成员人民陪审员-spzzcy', 'c_ms': 'spzzcy', 'c_target_bm': 'T_SPZZCY_RMPSY',
              'c_target_sjlx': 'varchar', 'c_source_bm': 'T_YWGY_RMPSY', 'c_system_type': 'np', 'c_group': 'spzzcy',
              'lx': 'Single'},
             {'c_target_ywlx': 'all', 'c_source_ywlx': 'all', 'c_target_zdm': 'C_XB', 'c_source_zdm': 'N_XB',
              'c_target_dzdm': '11400000', 'c_source_dzdm': '10100003', 'c_target_jtmz': '9', 'c_source_jtmz': None,
              'c_sheet_mc': '审判组织成员人民陪审员-spzzcy', 'c_ms': 'spzzcy', 'c_target_bm': 'T_SPZZCY_RMPSY',
              'c_target_sjlx': 'varchar', 'c_source_bm': 'T_YWGY_RMPSY', 'c_system_type': 'np', 'c_group': 'spzzcy',
              'lx': 'Single'},
             {'c_target_ywlx': 'all', 'c_source_ywlx': 'all', 'c_target_zdm': 'C_XB', 'c_source_zdm': 'N_XB',
              'c_target_dzdm': '11400000', 'c_source_dzdm': '10100003', 'c_target_jtmz': '0', 'c_source_jtmz': '255',
              'c_sheet_mc': '审判组织成员人民陪审员-spzzcy', 'c_ms': 'spzzcy', 'c_target_bm': 'T_SPZZCY_RMPSY',
              'c_target_sjlx': 'varchar', 'c_source_bm': 'T_YWGY_RMPSY', 'c_system_type': 'np', 'c_group': 'spzzcy',
              'lx': 'Single'},
             {'c_target_ywlx': 'all', 'c_source_ywlx': 'all', 'c_target_zdm': 'C_XB', 'c_source_zdm': 'N_XB',
              'c_target_dzdm': '11400000', 'c_source_dzdm': '10100003', 'c_target_jtmz': '0', 'c_source_jtmz': '0',
              'c_sheet_mc': '审判组织成员人民陪审员-spzzcy', 'c_ms': 'spzzcy', 'c_target_bm': 'T_SPZZCY_RMPSY',
              'c_target_sjlx': 'varchar', 'c_source_bm': 'T_YWGY_RMPSY', 'c_system_type': 'np', 'c_group': 'spzzcy',
              'lx': 'Single'}], [
             {'c_target_ywlx': 'all', 'c_source_ywlx': 'all', 'c_target_zdm': 'C_XB', 'c_source_zdm': 'N_XB',
              'c_target_dzdm': '11400000', 'c_source_dzdm': '10100003', 'c_target_jtmz': '1', 'c_source_jtmz': '1',
              'c_sheet_mc': '审判组织成员人民陪审员-spzzcy', 'c_ms': 'spzzcy', 'c_target_bm': 'T_SPZZCY_RMPSY',
              'c_target_sjlx': 'varchar', 'c_source_bm': 'T_YWGY_RMPSY', 'c_system_type': 'np', 'c_group': 'spzzcy',
              'lx': 'Single'},
             {'c_target_ywlx': 'all', 'c_source_ywlx': 'all', 'c_target_zdm': 'C_XB', 'c_source_zdm': 'N_XB',
              'c_target_dzdm': '11400000', 'c_source_dzdm': '10100003', 'c_target_jtmz': '2', 'c_source_jtmz': '2',
              'c_sheet_mc': '审判组织成员人民陪审员-spzzcy', 'c_ms': 'spzzcy', 'c_target_bm': 'T_SPZZCY_RMPSY',
              'c_target_sjlx': 'varchar', 'c_source_bm': 'T_YWGY_RMPSY', 'c_system_type': 'np', 'c_group': 'spzzcy',
              'lx': 'Single'},
             {'c_target_ywlx': 'all', 'c_source_ywlx': 'all', 'c_target_zdm': 'C_XB', 'c_source_zdm': 'N_XB',
              'c_target_dzdm': '11400000', 'c_source_dzdm': '10100003', 'c_target_jtmz': '9', 'c_source_jtmz': None,
              'c_sheet_mc': '审判组织成员人民陪审员-spzzcy', 'c_ms': 'spzzcy', 'c_target_bm': 'T_SPZZCY_RMPSY',
              'c_target_sjlx': 'varchar', 'c_source_bm': 'T_YWGY_RMPSY', 'c_system_type': 'np', 'c_group': 'spzzcy',
              'lx': 'Single'},
             {'c_target_ywlx': 'all', 'c_source_ywlx': 'all', 'c_target_zdm': 'C_XB', 'c_source_zdm': 'N_XB',
              'c_target_dzdm': '11400000', 'c_source_dzdm': '10100003', 'c_target_jtmz': '0', 'c_source_jtmz': '255',
              'c_sheet_mc': '审判组织成员人民陪审员-spzzcy', 'c_ms': 'spzzcy', 'c_target_bm': 'T_SPZZCY_RMPSY',
              'c_target_sjlx': 'varchar', 'c_source_bm': 'T_YWGY_RMPSY', 'c_system_type': 'np', 'c_group': 'spzzcy',
              'lx': 'Single'},
             {'c_target_ywlx': 'all', 'c_source_ywlx': 'all', 'c_target_zdm': 'C_XB', 'c_source_zdm': 'N_XB',
              'c_target_dzdm': '11400000', 'c_source_dzdm': '10100003', 'c_target_jtmz': '0', 'c_source_jtmz': '0',
              'c_sheet_mc': '审判组织成员人民陪审员-spzzcy', 'c_ms': 'spzzcy', 'c_target_bm': 'T_SPZZCY_RMPSY',
              'c_target_sjlx': 'varchar', 'c_source_bm': 'T_YWGY_RMPSY', 'c_system_type': 'np', 'c_group': 'spzzcy',
              'lx': 'Single'}], [
             {'c_target_ywlx': 'all', 'c_source_ywlx': 'all', 'c_target_zdm': 'C_XB', 'c_source_zdm': 'N_XB',
              'c_target_dzdm': '11400000', 'c_source_dzdm': '10100003', 'c_target_jtmz': '1', 'c_source_jtmz': '1',
              'c_sheet_mc': '审判组织成员人民陪审员-spzzcy', 'c_ms': 'spzzcy', 'c_target_bm': 'T_SPZZCY_RMPSY',
              'c_target_sjlx': 'varchar', 'c_source_bm': 'T_YWGY_RMPSY', 'c_system_type': 'np', 'c_group': 'spzzcy',
              'lx': 'Single'},
             {'c_target_ywlx': 'all', 'c_source_ywlx': 'all', 'c_target_zdm': 'C_XB', 'c_source_zdm': 'N_XB',
              'c_target_dzdm': '11400000', 'c_source_dzdm': '10100003', 'c_target_jtmz': '2', 'c_source_jtmz': '2',
              'c_sheet_mc': '审判组织成员人民陪审员-spzzcy', 'c_ms': 'spzzcy', 'c_target_bm': 'T_SPZZCY_RMPSY',
              'c_target_sjlx': 'varchar', 'c_source_bm': 'T_YWGY_RMPSY', 'c_system_type': 'np', 'c_group': 'spzzcy',
              'lx': 'Single'},
             {'c_target_ywlx': 'all', 'c_source_ywlx': 'all', 'c_target_zdm': 'C_XB', 'c_source_zdm': 'N_XB',
              'c_target_dzdm': '11400000', 'c_source_dzdm': '10100003', 'c_target_jtmz': '9', 'c_source_jtmz': None,
              'c_sheet_mc': '审判组织成员人民陪审员-spzzcy', 'c_ms': 'spzzcy', 'c_target_bm': 'T_SPZZCY_RMPSY',
              'c_target_sjlx': 'varchar', 'c_source_bm': 'T_YWGY_RMPSY', 'c_system_type': 'np', 'c_group': 'spzzcy',
              'lx': 'Single'},
             {'c_target_ywlx': 'all', 'c_source_ywlx': 'all', 'c_target_zdm': 'C_XB', 'c_source_zdm': 'N_XB',
              'c_target_dzdm': '11400000', 'c_source_dzdm': '10100003', 'c_target_jtmz': '0', 'c_source_jtmz': '255',
              'c_sheet_mc': '审判组织成员人民陪审员-spzzcy', 'c_ms': 'spzzcy', 'c_target_bm': 'T_SPZZCY_RMPSY',
              'c_target_sjlx': 'varchar', 'c_source_bm': 'T_YWGY_RMPSY', 'c_system_type': 'np', 'c_group': 'spzzcy',
              'lx': 'Single'},
             {'c_target_ywlx': 'all', 'c_source_ywlx': 'all', 'c_target_zdm': 'C_XB', 'c_source_zdm': 'N_XB',
              'c_target_dzdm': '11400000', 'c_source_dzdm': '10100003', 'c_target_jtmz': '0', 'c_source_jtmz': '0',
              'c_sheet_mc': '审判组织成员人民陪审员-spzzcy', 'c_ms': 'spzzcy', 'c_target_bm': 'T_SPZZCY_RMPSY',
              'c_target_sjlx': 'varchar', 'c_source_bm': 'T_YWGY_RMPSY', 'c_system_type': 'np', 'c_group': 'spzzcy',
              'lx': 'Single'}], [
             {'c_target_ywlx': 'all', 'c_source_ywlx': 'all', 'c_target_zdm': 'C_XB', 'c_source_zdm': 'N_XB',
              'c_target_dzdm': '11400000', 'c_source_dzdm': '10100003', 'c_target_jtmz': '1', 'c_source_jtmz': '1',
              'c_sheet_mc': '审判组织成员人民陪审员-spzzcy', 'c_ms': 'spzzcy', 'c_target_bm': 'T_SPZZCY_RMPSY',
              'c_target_sjlx': 'varchar', 'c_source_bm': 'T_YWGY_RMPSY', 'c_system_type': 'np', 'c_group': 'spzzcy',
              'lx': 'Single'},
             {'c_target_ywlx': 'all', 'c_source_ywlx': 'all', 'c_target_zdm': 'C_XB', 'c_source_zdm': 'N_XB',
              'c_target_dzdm': '11400000', 'c_source_dzdm': '10100003', 'c_target_jtmz': '2', 'c_source_jtmz': '2',
              'c_sheet_mc': '审判组织成员人民陪审员-spzzcy', 'c_ms': 'spzzcy', 'c_target_bm': 'T_SPZZCY_RMPSY',
              'c_target_sjlx': 'varchar', 'c_source_bm': 'T_YWGY_RMPSY', 'c_system_type': 'np', 'c_group': 'spzzcy',
              'lx': 'Single'},
             {'c_target_ywlx': 'all', 'c_source_ywlx': 'all', 'c_target_zdm': 'C_XB', 'c_source_zdm': 'N_XB',
              'c_target_dzdm': '11400000', 'c_source_dzdm': '10100003', 'c_target_jtmz': '9', 'c_source_jtmz': None,
              'c_sheet_mc': '审判组织成员人民陪审员-spzzcy', 'c_ms': 'spzzcy', 'c_target_bm': 'T_SPZZCY_RMPSY',
              'c_target_sjlx': 'varchar', 'c_source_bm': 'T_YWGY_RMPSY', 'c_system_type': 'np', 'c_group': 'spzzcy',
              'lx': 'Single'},
             {'c_target_ywlx': 'all', 'c_source_ywlx': 'all', 'c_target_zdm': 'C_XB', 'c_source_zdm': 'N_XB',
              'c_target_dzdm': '11400000', 'c_source_dzdm': '10100003', 'c_target_jtmz': '0', 'c_source_jtmz': '255',
              'c_sheet_mc': '审判组织成员人民陪审员-spzzcy', 'c_ms': 'spzzcy', 'c_target_bm': 'T_SPZZCY_RMPSY',
              'c_target_sjlx': 'varchar', 'c_source_bm': 'T_YWGY_RMPSY', 'c_system_type': 'np', 'c_group': 'spzzcy',
              'lx': 'Single'},
             {'c_target_ywlx': 'all', 'c_source_ywlx': 'all', 'c_target_zdm': 'C_XB', 'c_source_zdm': 'N_XB',
              'c_target_dzdm': '11400000', 'c_source_dzdm': '10100003', 'c_target_jtmz': '0', 'c_source_jtmz': '0',
              'c_sheet_mc': '审判组织成员人民陪审员-spzzcy', 'c_ms': 'spzzcy', 'c_target_bm': 'T_SPZZCY_RMPSY',
              'c_target_sjlx': 'varchar', 'c_source_bm': 'T_YWGY_RMPSY', 'c_system_type': 'np', 'c_group': 'spzzcy',
              'lx': 'Single'}], [
             {'c_target_ywlx': 'all', 'c_source_ywlx': 'all', 'c_target_zdm': 'C_XB', 'c_source_zdm': 'N_XB',
              'c_target_dzdm': '11400000', 'c_source_dzdm': '10100003', 'c_target_jtmz': '1', 'c_source_jtmz': '1',
              'c_sheet_mc': '审判组织成员人民陪审员-spzzcy', 'c_ms': 'spzzcy', 'c_target_bm': 'T_SPZZCY_RMPSY',
              'c_target_sjlx': 'varchar', 'c_source_bm': 'T_YWGY_RMPSY', 'c_system_type': 'np', 'c_group': 'spzzcy',
              'lx': 'Single'},
             {'c_target_ywlx': 'all', 'c_source_ywlx': 'all', 'c_target_zdm': 'C_XB', 'c_source_zdm': 'N_XB',
              'c_target_dzdm': '11400000', 'c_source_dzdm': '10100003', 'c_target_jtmz': '2', 'c_source_jtmz': '2',
              'c_sheet_mc': '审判组织成员人民陪审员-spzzcy', 'c_ms': 'spzzcy', 'c_target_bm': 'T_SPZZCY_RMPSY',
              'c_target_sjlx': 'varchar', 'c_source_bm': 'T_YWGY_RMPSY', 'c_system_type': 'np', 'c_group': 'spzzcy',
              'lx': 'Single'},
             {'c_target_ywlx': 'all', 'c_source_ywlx': 'all', 'c_target_zdm': 'C_XB', 'c_source_zdm': 'N_XB',
              'c_target_dzdm': '11400000', 'c_source_dzdm': '10100003', 'c_target_jtmz': '9', 'c_source_jtmz': None,
              'c_sheet_mc': '审判组织成员人民陪审员-spzzcy', 'c_ms': 'spzzcy', 'c_target_bm': 'T_SPZZCY_RMPSY',
              'c_target_sjlx': 'varchar', 'c_source_bm': 'T_YWGY_RMPSY', 'c_system_type': 'np', 'c_group': 'spzzcy',
              'lx': 'Single'},
             {'c_target_ywlx': 'all', 'c_source_ywlx': 'all', 'c_target_zdm': 'C_XB', 'c_source_zdm': 'N_XB',
              'c_target_dzdm': '11400000', 'c_source_dzdm': '10100003', 'c_target_jtmz': '0', 'c_source_jtmz': '255',
              'c_sheet_mc': '审判组织成员人民陪审员-spzzcy', 'c_ms': 'spzzcy', 'c_target_bm': 'T_SPZZCY_RMPSY',
              'c_target_sjlx': 'varchar', 'c_source_bm': 'T_YWGY_RMPSY', 'c_system_type': 'np', 'c_group': 'spzzcy',
              'lx': 'Single'},
             {'c_target_ywlx': 'all', 'c_source_ywlx': 'all', 'c_target_zdm': 'C_XB', 'c_source_zdm': 'N_XB',
              'c_target_dzdm': '11400000', 'c_source_dzdm': '10100003', 'c_target_jtmz': '0', 'c_source_jtmz': '0',
              'c_sheet_mc': '审判组织成员人民陪审员-spzzcy', 'c_ms': 'spzzcy', 'c_target_bm': 'T_SPZZCY_RMPSY',
              'c_target_sjlx': 'varchar', 'c_source_bm': 'T_YWGY_RMPSY', 'c_system_type': 'np', 'c_group': 'spzzcy',
              'lx': 'Single'}], [
             {'c_target_ywlx': 'all', 'c_source_ywlx': 'all', 'c_target_zdm': 'C_XB', 'c_source_zdm': 'N_XB',
              'c_target_dzdm': '11400000', 'c_source_dzdm': '10100003', 'c_target_jtmz': '1', 'c_source_jtmz': '1',
              'c_sheet_mc': '审判组织成员人民陪审员-spzzcy', 'c_ms': 'spzzcy', 'c_target_bm': 'T_SPZZCY_RMPSY',
              'c_target_sjlx': 'varchar', 'c_source_bm': 'T_YWGY_RMPSY', 'c_system_type': 'np', 'c_group': 'spzzcy',
              'lx': 'Single'},
             {'c_target_ywlx': 'all', 'c_source_ywlx': 'all', 'c_target_zdm': 'C_XB', 'c_source_zdm': 'N_XB',
              'c_target_dzdm': '11400000', 'c_source_dzdm': '10100003', 'c_target_jtmz': '2', 'c_source_jtmz': '2',
              'c_sheet_mc': '审判组织成员人民陪审员-spzzcy', 'c_ms': 'spzzcy', 'c_target_bm': 'T_SPZZCY_RMPSY',
              'c_target_sjlx': 'varchar', 'c_source_bm': 'T_YWGY_RMPSY', 'c_system_type': 'np', 'c_group': 'spzzcy',
              'lx': 'Single'},
             {'c_target_ywlx': 'all', 'c_source_ywlx': 'all', 'c_target_zdm': 'C_XB', 'c_source_zdm': 'N_XB',
              'c_target_dzdm': '11400000', 'c_source_dzdm': '10100003', 'c_target_jtmz': '9', 'c_source_jtmz': None,
              'c_sheet_mc': '审判组织成员人民陪审员-spzzcy', 'c_ms': 'spzzcy', 'c_target_bm': 'T_SPZZCY_RMPSY',
              'c_target_sjlx': 'varchar', 'c_source_bm': 'T_YWGY_RMPSY', 'c_system_type': 'np', 'c_group': 'spzzcy',
              'lx': 'Single'},
             {'c_target_ywlx': 'all', 'c_source_ywlx': 'all', 'c_target_zdm': 'C_XB', 'c_source_zdm': 'N_XB',
              'c_target_dzdm': '11400000', 'c_source_dzdm': '10100003', 'c_target_jtmz': '0', 'c_source_jtmz': '255',
              'c_sheet_mc': '审判组织成员人民陪审员-spzzcy', 'c_ms': 'spzzcy', 'c_target_bm': 'T_SPZZCY_RMPSY',
              'c_target_sjlx': 'varchar', 'c_source_bm': 'T_YWGY_RMPSY', 'c_system_type': 'np', 'c_group': 'spzzcy',
              'lx': 'Single'},
             {'c_target_ywlx': 'all', 'c_source_ywlx': 'all', 'c_target_zdm': 'C_XB', 'c_source_zdm': 'N_XB',
              'c_target_dzdm': '11400000', 'c_source_dzdm': '10100003', 'c_target_jtmz': '0', 'c_source_jtmz': '0',
              'c_sheet_mc': '审判组织成员人民陪审员-spzzcy', 'c_ms': 'spzzcy', 'c_target_bm': 'T_SPZZCY_RMPSY',
              'c_target_sjlx': 'varchar', 'c_source_bm': 'T_YWGY_RMPSY', 'c_system_type': 'np', 'c_group': 'spzzcy',
              'lx': 'Single'}], [
             {'c_target_ywlx': 'all', 'c_source_ywlx': 'all', 'c_target_zdm': 'C_XB', 'c_source_zdm': 'N_XB',
              'c_target_dzdm': '11400000', 'c_source_dzdm': '10100003', 'c_target_jtmz': '1', 'c_source_jtmz': '1',
              'c_sheet_mc': '审判组织成员人民陪审员-spzzcy', 'c_ms': 'spzzcy', 'c_target_bm': 'T_SPZZCY_RMPSY',
              'c_target_sjlx': 'varchar', 'c_source_bm': 'T_YWGY_RMPSY', 'c_system_type': 'np', 'c_group': 'spzzcy',
              'lx': 'Single'},
             {'c_target_ywlx': 'all', 'c_source_ywlx': 'all', 'c_target_zdm': 'C_XB', 'c_source_zdm': 'N_XB',
              'c_target_dzdm': '11400000', 'c_source_dzdm': '10100003', 'c_target_jtmz': '2', 'c_source_jtmz': '2',
              'c_sheet_mc': '审判组织成员人民陪审员-spzzcy', 'c_ms': 'spzzcy', 'c_target_bm': 'T_SPZZCY_RMPSY',
              'c_target_sjlx': 'varchar', 'c_source_bm': 'T_YWGY_RMPSY', 'c_system_type': 'np', 'c_group': 'spzzcy',
              'lx': 'Single'},
             {'c_target_ywlx': 'all', 'c_source_ywlx': 'all', 'c_target_zdm': 'C_XB', 'c_source_zdm': 'N_XB',
              'c_target_dzdm': '11400000', 'c_source_dzdm': '10100003', 'c_target_jtmz': '9', 'c_source_jtmz': None,
              'c_sheet_mc': '审判组织成员人民陪审员-spzzcy', 'c_ms': 'spzzcy', 'c_target_bm': 'T_SPZZCY_RMPSY',
              'c_target_sjlx': 'varchar', 'c_source_bm': 'T_YWGY_RMPSY', 'c_system_type': 'np', 'c_group': 'spzzcy',
              'lx': 'Single'},
             {'c_target_ywlx': 'all', 'c_source_ywlx': 'all', 'c_target_zdm': 'C_XB', 'c_source_zdm': 'N_XB',
              'c_target_dzdm': '11400000', 'c_source_dzdm': '10100003', 'c_target_jtmz': '0', 'c_source_jtmz': '255',
              'c_sheet_mc': '审判组织成员人民陪审员-spzzcy', 'c_ms': 'spzzcy', 'c_target_bm': 'T_SPZZCY_RMPSY',
              'c_target_sjlx': 'varchar', 'c_source_bm': 'T_YWGY_RMPSY', 'c_system_type': 'np', 'c_group': 'spzzcy',
              'lx': 'Single'},
             {'c_target_ywlx': 'all', 'c_source_ywlx': 'all', 'c_target_zdm': 'C_XB', 'c_source_zdm': 'N_XB',
              'c_target_dzdm': '11400000', 'c_source_dzdm': '10100003', 'c_target_jtmz': '0', 'c_source_jtmz': '0',
              'c_sheet_mc': '审判组织成员人民陪审员-spzzcy', 'c_ms': 'spzzcy', 'c_target_bm': 'T_SPZZCY_RMPSY',
              'c_target_sjlx': 'varchar', 'c_source_bm': 'T_YWGY_RMPSY', 'c_system_type': 'np', 'c_group': 'spzzcy',
              'lx': 'Single'}], [
             {'c_target_ywlx': 'all', 'c_source_ywlx': 'all', 'c_target_zdm': 'C_XB', 'c_source_zdm': 'N_XB',
              'c_target_dzdm': '11400000', 'c_source_dzdm': '10100003', 'c_target_jtmz': '1', 'c_source_jtmz': '1',
              'c_sheet_mc': '审判组织成员人民陪审员-spzzcy', 'c_ms': 'spzzcy', 'c_target_bm': 'T_SPZZCY_RMPSY',
              'c_target_sjlx': 'varchar', 'c_source_bm': 'T_YWGY_RMPSY', 'c_system_type': 'np', 'c_group': 'spzzcy',
              'lx': 'Single'},
             {'c_target_ywlx': 'all', 'c_source_ywlx': 'all', 'c_target_zdm': 'C_XB', 'c_source_zdm': 'N_XB',
              'c_target_dzdm': '11400000', 'c_source_dzdm': '10100003', 'c_target_jtmz': '2', 'c_source_jtmz': '2',
              'c_sheet_mc': '审判组织成员人民陪审员-spzzcy', 'c_ms': 'spzzcy', 'c_target_bm': 'T_SPZZCY_RMPSY',
              'c_target_sjlx': 'varchar', 'c_source_bm': 'T_YWGY_RMPSY', 'c_system_type': 'np', 'c_group': 'spzzcy',
              'lx': 'Single'},
             {'c_target_ywlx': 'all', 'c_source_ywlx': 'all', 'c_target_zdm': 'C_XB', 'c_source_zdm': 'N_XB',
              'c_target_dzdm': '11400000', 'c_source_dzdm': '10100003', 'c_target_jtmz': '9', 'c_source_jtmz': None,
              'c_sheet_mc': '审判组织成员人民陪审员-spzzcy', 'c_ms': 'spzzcy', 'c_target_bm': 'T_SPZZCY_RMPSY',
              'c_target_sjlx': 'varchar', 'c_source_bm': 'T_YWGY_RMPSY', 'c_system_type': 'np', 'c_group': 'spzzcy',
              'lx': 'Single'},
             {'c_target_ywlx': 'all', 'c_source_ywlx': 'all', 'c_target_zdm': 'C_XB', 'c_source_zdm': 'N_XB',
              'c_target_dzdm': '11400000', 'c_source_dzdm': '10100003', 'c_target_jtmz': '0', 'c_source_jtmz': '255',
              'c_sheet_mc': '审判组织成员人民陪审员-spzzcy', 'c_ms': 'spzzcy', 'c_target_bm': 'T_SPZZCY_RMPSY',
              'c_target_sjlx': 'varchar', 'c_source_bm': 'T_YWGY_RMPSY', 'c_system_type': 'np', 'c_group': 'spzzcy',
              'lx': 'Single'},
             {'c_target_ywlx': 'all', 'c_source_ywlx': 'all', 'c_target_zdm': 'C_XB', 'c_source_zdm': 'N_XB',
              'c_target_dzdm': '11400000', 'c_source_dzdm': '10100003', 'c_target_jtmz': '0', 'c_source_jtmz': '0',
              'c_sheet_mc': '审判组织成员人民陪审员-spzzcy', 'c_ms': 'spzzcy', 'c_target_bm': 'T_SPZZCY_RMPSY',
              'c_target_sjlx': 'varchar', 'c_source_bm': 'T_YWGY_RMPSY', 'c_system_type': 'np', 'c_group': 'spzzcy',
              'lx': 'Single'}], [
             {'c_target_ywlx': 'all', 'c_source_ywlx': 'all', 'c_target_zdm': 'C_XB', 'c_source_zdm': 'N_XB',
              'c_target_dzdm': '11400000', 'c_source_dzdm': '10100003', 'c_target_jtmz': '1', 'c_source_jtmz': '1',
              'c_sheet_mc': '审判组织成员人民陪审员-spzzcy', 'c_ms': 'spzzcy', 'c_target_bm': 'T_SPZZCY_RMPSY',
              'c_target_sjlx': 'varchar', 'c_source_bm': 'T_YWGY_RMPSY', 'c_system_type': 'np', 'c_group': 'spzzcy',
              'lx': 'Single'},
             {'c_target_ywlx': 'all', 'c_source_ywlx': 'all', 'c_target_zdm': 'C_XB', 'c_source_zdm': 'N_XB',
              'c_target_dzdm': '11400000', 'c_source_dzdm': '10100003', 'c_target_jtmz': '2', 'c_source_jtmz': '2',
              'c_sheet_mc': '审判组织成员人民陪审员-spzzcy', 'c_ms': 'spzzcy', 'c_target_bm': 'T_SPZZCY_RMPSY',
              'c_target_sjlx': 'varchar', 'c_source_bm': 'T_YWGY_RMPSY', 'c_system_type': 'np', 'c_group': 'spzzcy',
              'lx': 'Single'},
             {'c_target_ywlx': 'all', 'c_source_ywlx': 'all', 'c_target_zdm': 'C_XB', 'c_source_zdm': 'N_XB',
              'c_target_dzdm': '11400000', 'c_source_dzdm': '10100003', 'c_target_jtmz': '9', 'c_source_jtmz': None,
              'c_sheet_mc': '审判组织成员人民陪审员-spzzcy', 'c_ms': 'spzzcy', 'c_target_bm': 'T_SPZZCY_RMPSY',
              'c_target_sjlx': 'varchar', 'c_source_bm': 'T_YWGY_RMPSY', 'c_system_type': 'np', 'c_group': 'spzzcy',
              'lx': 'Single'},
             {'c_target_ywlx': 'all', 'c_source_ywlx': 'all', 'c_target_zdm': 'C_XB', 'c_source_zdm': 'N_XB',
              'c_target_dzdm': '11400000', 'c_source_dzdm': '10100003', 'c_target_jtmz': '0', 'c_source_jtmz': '255',
              'c_sheet_mc': '审判组织成员人民陪审员-spzzcy', 'c_ms': 'spzzcy', 'c_target_bm': 'T_SPZZCY_RMPSY',
              'c_target_sjlx': 'varchar', 'c_source_bm': 'T_YWGY_RMPSY', 'c_system_type': 'np', 'c_group': 'spzzcy',
              'lx': 'Single'},
             {'c_target_ywlx': 'all', 'c_source_ywlx': 'all', 'c_target_zdm': 'C_XB', 'c_source_zdm': 'N_XB',
              'c_target_dzdm': '11400000', 'c_source_dzdm': '10100003', 'c_target_jtmz': '0', 'c_source_jtmz': '0',
              'c_sheet_mc': '审判组织成员人民陪审员-spzzcy', 'c_ms': 'spzzcy', 'c_target_bm': 'T_SPZZCY_RMPSY',
              'c_target_sjlx': 'varchar', 'c_source_bm': 'T_YWGY_RMPSY', 'c_system_type': 'np', 'c_group': 'spzzcy',
              'lx': 'Single'}], [
             {'c_target_ywlx': 'all', 'c_source_ywlx': 'all', 'c_target_zdm': 'C_XB', 'c_source_zdm': 'N_XB',
              'c_target_dzdm': '11400000', 'c_source_dzdm': '10100003', 'c_target_jtmz': '1', 'c_source_jtmz': '1',
              'c_sheet_mc': '审判组织成员人民陪审员-spzzcy', 'c_ms': 'spzzcy', 'c_target_bm': 'T_SPZZCY_RMPSY',
              'c_target_sjlx': 'varchar', 'c_source_bm': 'T_YWGY_RMPSY', 'c_system_type': 'np', 'c_group': 'spzzcy',
              'lx': 'Single'},
             {'c_target_ywlx': 'all', 'c_source_ywlx': 'all', 'c_target_zdm': 'C_XB', 'c_source_zdm': 'N_XB',
              'c_target_dzdm': '11400000', 'c_source_dzdm': '10100003', 'c_target_jtmz': '2', 'c_source_jtmz': '2',
              'c_sheet_mc': '审判组织成员人民陪审员-spzzcy', 'c_ms': 'spzzcy', 'c_target_bm': 'T_SPZZCY_RMPSY',
              'c_target_sjlx': 'varchar', 'c_source_bm': 'T_YWGY_RMPSY', 'c_system_type': 'np', 'c_group': 'spzzcy',
              'lx': 'Single'},
             {'c_target_ywlx': 'all', 'c_source_ywlx': 'all', 'c_target_zdm': 'C_XB', 'c_source_zdm': 'N_XB',
              'c_target_dzdm': '11400000', 'c_source_dzdm': '10100003', 'c_target_jtmz': '9', 'c_source_jtmz': None,
              'c_sheet_mc': '审判组织成员人民陪审员-spzzcy', 'c_ms': 'spzzcy', 'c_target_bm': 'T_SPZZCY_RMPSY',
              'c_target_sjlx': 'varchar', 'c_source_bm': 'T_YWGY_RMPSY', 'c_system_type': 'np', 'c_group': 'spzzcy',
              'lx': 'Single'},
             {'c_target_ywlx': 'all', 'c_source_ywlx': 'all', 'c_target_zdm': 'C_XB', 'c_source_zdm': 'N_XB',
              'c_target_dzdm': '11400000', 'c_source_dzdm': '10100003', 'c_target_jtmz': '0', 'c_source_jtmz': '255',
              'c_sheet_mc': '审判组织成员人民陪审员-spzzcy', 'c_ms': 'spzzcy', 'c_target_bm': 'T_SPZZCY_RMPSY',
              'c_target_sjlx': 'varchar', 'c_source_bm': 'T_YWGY_RMPSY', 'c_system_type': 'np', 'c_group': 'spzzcy',
              'lx': 'Single'},
             {'c_target_ywlx': 'all', 'c_source_ywlx': 'all', 'c_target_zdm': 'C_XB', 'c_source_zdm': 'N_XB',
              'c_target_dzdm': '11400000', 'c_source_dzdm': '10100003', 'c_target_jtmz': '0', 'c_source_jtmz': '0',
              'c_sheet_mc': '审判组织成员人民陪审员-spzzcy', 'c_ms': 'spzzcy', 'c_target_bm': 'T_SPZZCY_RMPSY',
              'c_target_sjlx': 'varchar', 'c_source_bm': 'T_YWGY_RMPSY', 'c_system_type': 'np', 'c_group': 'spzzcy',
              'lx': 'Single'}], [
             {'c_target_ywlx': 'all', 'c_source_ywlx': 'all', 'c_target_zdm': 'C_XB', 'c_source_zdm': 'N_XB',
              'c_target_dzdm': '11400000', 'c_source_dzdm': '10100003', 'c_target_jtmz': '1', 'c_source_jtmz': '1',
              'c_sheet_mc': '审判组织成员人民陪审员-spzzcy', 'c_ms': 'spzzcy', 'c_target_bm': 'T_SPZZCY_RMPSY',
              'c_target_sjlx': 'varchar', 'c_source_bm': 'T_YWGY_RMPSY', 'c_system_type': 'np', 'c_group': 'spzzcy',
              'lx': 'Single'},
             {'c_target_ywlx': 'all', 'c_source_ywlx': 'all', 'c_target_zdm': 'C_XB', 'c_source_zdm': 'N_XB',
              'c_target_dzdm': '11400000', 'c_source_dzdm': '10100003', 'c_target_jtmz': '2', 'c_source_jtmz': '2',
              'c_sheet_mc': '审判组织成员人民陪审员-spzzcy', 'c_ms': 'spzzcy', 'c_target_bm': 'T_SPZZCY_RMPSY',
              'c_target_sjlx': 'varchar', 'c_source_bm': 'T_YWGY_RMPSY', 'c_system_type': 'np', 'c_group': 'spzzcy',
              'lx': 'Single'},
             {'c_target_ywlx': 'all', 'c_source_ywlx': 'all', 'c_target_zdm': 'C_XB', 'c_source_zdm': 'N_XB',
              'c_target_dzdm': '11400000', 'c_source_dzdm': '10100003', 'c_target_jtmz': '9', 'c_source_jtmz': None,
              'c_sheet_mc': '审判组织成员人民陪审员-spzzcy', 'c_ms': 'spzzcy', 'c_target_bm': 'T_SPZZCY_RMPSY',
              'c_target_sjlx': 'varchar', 'c_source_bm': 'T_YWGY_RMPSY', 'c_system_type': 'np', 'c_group': 'spzzcy',
              'lx': 'Single'},
             {'c_target_ywlx': 'all', 'c_source_ywlx': 'all', 'c_target_zdm': 'C_XB', 'c_source_zdm': 'N_XB',
              'c_target_dzdm': '11400000', 'c_source_dzdm': '10100003', 'c_target_jtmz': '0', 'c_source_jtmz': '255',
              'c_sheet_mc': '审判组织成员人民陪审员-spzzcy', 'c_ms': 'spzzcy', 'c_target_bm': 'T_SPZZCY_RMPSY',
              'c_target_sjlx': 'varchar', 'c_source_bm': 'T_YWGY_RMPSY', 'c_system_type': 'np', 'c_group': 'spzzcy',
              'lx': 'Single'},
             {'c_target_ywlx': 'all', 'c_source_ywlx': 'all', 'c_target_zdm': 'C_XB', 'c_source_zdm': 'N_XB',
              'c_target_dzdm': '11400000', 'c_source_dzdm': '10100003', 'c_target_jtmz': '0', 'c_source_jtmz': '0',
              'c_sheet_mc': '审判组织成员人民陪审员-spzzcy', 'c_ms': 'spzzcy', 'c_target_bm': 'T_SPZZCY_RMPSY',
              'c_target_sjlx': 'varchar', 'c_source_bm': 'T_YWGY_RMPSY', 'c_system_type': 'np', 'c_group': 'spzzcy',
              'lx': 'Single'}], [
             {'c_target_ywlx': 'all', 'c_source_ywlx': 'all', 'c_target_zdm': 'C_XB', 'c_source_zdm': 'N_XB',
              'c_target_dzdm': '11400000', 'c_source_dzdm': '10100003', 'c_target_jtmz': '1', 'c_source_jtmz': '1',
              'c_sheet_mc': '审判组织成员人民陪审员-spzzcy', 'c_ms': 'spzzcy', 'c_target_bm': 'T_SPZZCY_RMPSY',
              'c_target_sjlx': 'varchar', 'c_source_bm': 'T_YWGY_RMPSY', 'c_system_type': 'np', 'c_group': 'spzzcy',
              'lx': 'Single'},
             {'c_target_ywlx': 'all', 'c_source_ywlx': 'all', 'c_target_zdm': 'C_XB', 'c_source_zdm': 'N_XB',
              'c_target_dzdm': '11400000', 'c_source_dzdm': '10100003', 'c_target_jtmz': '2', 'c_source_jtmz': '2',
              'c_sheet_mc': '审判组织成员人民陪审员-spzzcy', 'c_ms': 'spzzcy', 'c_target_bm': 'T_SPZZCY_RMPSY',
              'c_target_sjlx': 'varchar', 'c_source_bm': 'T_YWGY_RMPSY', 'c_system_type': 'np', 'c_group': 'spzzcy',
              'lx': 'Single'},
             {'c_target_ywlx': 'all', 'c_source_ywlx': 'all', 'c_target_zdm': 'C_XB', 'c_source_zdm': 'N_XB',
              'c_target_dzdm': '11400000', 'c_source_dzdm': '10100003', 'c_target_jtmz': '9', 'c_source_jtmz': None,
              'c_sheet_mc': '审判组织成员人民陪审员-spzzcy', 'c_ms': 'spzzcy', 'c_target_bm': 'T_SPZZCY_RMPSY',
              'c_target_sjlx': 'varchar', 'c_source_bm': 'T_YWGY_RMPSY', 'c_system_type': 'np', 'c_group': 'spzzcy',
              'lx': 'Single'},
             {'c_target_ywlx': 'all', 'c_source_ywlx': 'all', 'c_target_zdm': 'C_XB', 'c_source_zdm': 'N_XB',
              'c_target_dzdm': '11400000', 'c_source_dzdm': '10100003', 'c_target_jtmz': '0', 'c_source_jtmz': '255',
              'c_sheet_mc': '审判组织成员人民陪审员-spzzcy', 'c_ms': 'spzzcy', 'c_target_bm': 'T_SPZZCY_RMPSY',
              'c_target_sjlx': 'varchar', 'c_source_bm': 'T_YWGY_RMPSY', 'c_system_type': 'np', 'c_group': 'spzzcy',
              'lx': 'Single'},
             {'c_target_ywlx': 'all', 'c_source_ywlx': 'all', 'c_target_zdm': 'C_XB', 'c_source_zdm': 'N_XB',
              'c_target_dzdm': '11400000', 'c_source_dzdm': '10100003', 'c_target_jtmz': '0', 'c_source_jtmz': '0',
              'c_sheet_mc': '审判组织成员人民陪审员-spzzcy', 'c_ms': 'spzzcy', 'c_target_bm': 'T_SPZZCY_RMPSY',
              'c_target_sjlx': 'varchar', 'c_source_bm': 'T_YWGY_RMPSY', 'c_system_type': 'np', 'c_group': 'spzzcy',
              'lx': 'Single'}], [
             {'c_target_ywlx': 'all', 'c_source_ywlx': 'all', 'c_target_zdm': 'C_XB', 'c_source_zdm': 'N_XB',
              'c_target_dzdm': '11400000', 'c_source_dzdm': '10100003', 'c_target_jtmz': '1', 'c_source_jtmz': '1',
              'c_sheet_mc': '审判组织成员人民陪审员-spzzcy', 'c_ms': 'spzzcy', 'c_target_bm': 'T_SPZZCY_RMPSY',
              'c_target_sjlx': 'varchar', 'c_source_bm': 'T_YWGY_RMPSY', 'c_system_type': 'np', 'c_group': 'spzzcy',
              'lx': 'Single'},
             {'c_target_ywlx': 'all', 'c_source_ywlx': 'all', 'c_target_zdm': 'C_XB', 'c_source_zdm': 'N_XB',
              'c_target_dzdm': '11400000', 'c_source_dzdm': '10100003', 'c_target_jtmz': '2', 'c_source_jtmz': '2',
              'c_sheet_mc': '审判组织成员人民陪审员-spzzcy', 'c_ms': 'spzzcy', 'c_target_bm': 'T_SPZZCY_RMPSY',
              'c_target_sjlx': 'varchar', 'c_source_bm': 'T_YWGY_RMPSY', 'c_system_type': 'np', 'c_group': 'spzzcy',
              'lx': 'Single'},
             {'c_target_ywlx': 'all', 'c_source_ywlx': 'all', 'c_target_zdm': 'C_XB', 'c_source_zdm': 'N_XB',
              'c_target_dzdm': '11400000', 'c_source_dzdm': '10100003', 'c_target_jtmz': '9', 'c_source_jtmz': None,
              'c_sheet_mc': '审判组织成员人民陪审员-spzzcy', 'c_ms': 'spzzcy', 'c_target_bm': 'T_SPZZCY_RMPSY',
              'c_target_sjlx': 'varchar', 'c_source_bm': 'T_YWGY_RMPSY', 'c_system_type': 'np', 'c_group': 'spzzcy',
              'lx': 'Single'},
             {'c_target_ywlx': 'all', 'c_source_ywlx': 'all', 'c_target_zdm': 'C_XB', 'c_source_zdm': 'N_XB',
              'c_target_dzdm': '11400000', 'c_source_dzdm': '10100003', 'c_target_jtmz': '0', 'c_source_jtmz': '255',
              'c_sheet_mc': '审判组织成员人民陪审员-spzzcy', 'c_ms': 'spzzcy', 'c_target_bm': 'T_SPZZCY_RMPSY',
              'c_target_sjlx': 'varchar', 'c_source_bm': 'T_YWGY_RMPSY', 'c_system_type': 'np', 'c_group': 'spzzcy',
              'lx': 'Single'},
             {'c_target_ywlx': 'all', 'c_source_ywlx': 'all', 'c_target_zdm': 'C_XB', 'c_source_zdm': 'N_XB',
              'c_target_dzdm': '11400000', 'c_source_dzdm': '10100003', 'c_target_jtmz': '0', 'c_source_jtmz': '0',
              'c_sheet_mc': '审判组织成员人民陪审员-spzzcy', 'c_ms': 'spzzcy', 'c_target_bm': 'T_SPZZCY_RMPSY',
              'c_target_sjlx': 'varchar', 'c_source_bm': 'T_YWGY_RMPSY', 'c_system_type': 'np', 'c_group': 'spzzcy',
              'lx': 'Single'}], [
             {'c_target_ywlx': 'all', 'c_source_ywlx': 'all', 'c_target_zdm': 'C_XB', 'c_source_zdm': 'N_XB',
              'c_target_dzdm': '11400000', 'c_source_dzdm': '10100003', 'c_target_jtmz': '1', 'c_source_jtmz': '1',
              'c_sheet_mc': '审判组织成员人民陪审员-spzzcy', 'c_ms': 'spzzcy', 'c_target_bm': 'T_SPZZCY_RMPSY',
              'c_target_sjlx': 'varchar', 'c_source_bm': 'T_YWGY_RMPSY', 'c_system_type': 'np', 'c_group': 'spzzcy',
              'lx': 'Single'},
             {'c_target_ywlx': 'all', 'c_source_ywlx': 'all', 'c_target_zdm': 'C_XB', 'c_source_zdm': 'N_XB',
              'c_target_dzdm': '11400000', 'c_source_dzdm': '10100003', 'c_target_jtmz': '2', 'c_source_jtmz': '2',
              'c_sheet_mc': '审判组织成员人民陪审员-spzzcy', 'c_ms': 'spzzcy', 'c_target_bm': 'T_SPZZCY_RMPSY',
              'c_target_sjlx': 'varchar', 'c_source_bm': 'T_YWGY_RMPSY', 'c_system_type': 'np', 'c_group': 'spzzcy',
              'lx': 'Single'},
             {'c_target_ywlx': 'all', 'c_source_ywlx': 'all', 'c_target_zdm': 'C_XB', 'c_source_zdm': 'N_XB',
              'c_target_dzdm': '11400000', 'c_source_dzdm': '10100003', 'c_target_jtmz': '9', 'c_source_jtmz': None,
              'c_sheet_mc': '审判组织成员人民陪审员-spzzcy', 'c_ms': 'spzzcy', 'c_target_bm': 'T_SPZZCY_RMPSY',
              'c_target_sjlx': 'varchar', 'c_source_bm': 'T_YWGY_RMPSY', 'c_system_type': 'np', 'c_group': 'spzzcy',
              'lx': 'Single'},
             {'c_target_ywlx': 'all', 'c_source_ywlx': 'all', 'c_target_zdm': 'C_XB', 'c_source_zdm': 'N_XB',
              'c_target_dzdm': '11400000', 'c_source_dzdm': '10100003', 'c_target_jtmz': '0', 'c_source_jtmz': '255',
              'c_sheet_mc': '审判组织成员人民陪审员-spzzcy', 'c_ms': 'spzzcy', 'c_target_bm': 'T_SPZZCY_RMPSY',
              'c_target_sjlx': 'varchar', 'c_source_bm': 'T_YWGY_RMPSY', 'c_system_type': 'np', 'c_group': 'spzzcy',
              'lx': 'Single'},
             {'c_target_ywlx': 'all', 'c_source_ywlx': 'all', 'c_target_zdm': 'C_XB', 'c_source_zdm': 'N_XB',
              'c_target_dzdm': '11400000', 'c_source_dzdm': '10100003', 'c_target_jtmz': '0', 'c_source_jtmz': '0',
              'c_sheet_mc': '审判组织成员人民陪审员-spzzcy', 'c_ms': 'spzzcy', 'c_target_bm': 'T_SPZZCY_RMPSY',
              'c_target_sjlx': 'varchar', 'c_source_bm': 'T_YWGY_RMPSY', 'c_system_type': 'np', 'c_group': 'spzzcy',
              'lx': 'Single'}], [
             {'c_target_ywlx': 'all', 'c_source_ywlx': 'all', 'c_target_zdm': 'C_XB', 'c_source_zdm': 'N_XB',
              'c_target_dzdm': '11400000', 'c_source_dzdm': '10100003', 'c_target_jtmz': '1', 'c_source_jtmz': '1',
              'c_sheet_mc': '审判组织成员人民陪审员-spzzcy', 'c_ms': 'spzzcy', 'c_target_bm': 'T_SPZZCY_RMPSY',
              'c_target_sjlx': 'varchar', 'c_source_bm': 'T_YWGY_RMPSY', 'c_system_type': 'np', 'c_group': 'spzzcy',
              'lx': 'Single'},
             {'c_target_ywlx': 'all', 'c_source_ywlx': 'all', 'c_target_zdm': 'C_XB', 'c_source_zdm': 'N_XB',
              'c_target_dzdm': '11400000', 'c_source_dzdm': '10100003', 'c_target_jtmz': '2', 'c_source_jtmz': '2',
              'c_sheet_mc': '审判组织成员人民陪审员-spzzcy', 'c_ms': 'spzzcy', 'c_target_bm': 'T_SPZZCY_RMPSY',
              'c_target_sjlx': 'varchar', 'c_source_bm': 'T_YWGY_RMPSY', 'c_system_type': 'np', 'c_group': 'spzzcy',
              'lx': 'Single'},
             {'c_target_ywlx': 'all', 'c_source_ywlx': 'all', 'c_target_zdm': 'C_XB', 'c_source_zdm': 'N_XB',
              'c_target_dzdm': '11400000', 'c_source_dzdm': '10100003', 'c_target_jtmz': '9', 'c_source_jtmz': None,
              'c_sheet_mc': '审判组织成员人民陪审员-spzzcy', 'c_ms': 'spzzcy', 'c_target_bm': 'T_SPZZCY_RMPSY',
              'c_target_sjlx': 'varchar', 'c_source_bm': 'T_YWGY_RMPSY', 'c_system_type': 'np', 'c_group': 'spzzcy',
              'lx': 'Single'},
             {'c_target_ywlx': 'all', 'c_source_ywlx': 'all', 'c_target_zdm': 'C_XB', 'c_source_zdm': 'N_XB',
              'c_target_dzdm': '11400000', 'c_source_dzdm': '10100003', 'c_target_jtmz': '0', 'c_source_jtmz': '255',
              'c_sheet_mc': '审判组织成员人民陪审员-spzzcy', 'c_ms': 'spzzcy', 'c_target_bm': 'T_SPZZCY_RMPSY',
              'c_target_sjlx': 'varchar', 'c_source_bm': 'T_YWGY_RMPSY', 'c_system_type': 'np', 'c_group': 'spzzcy',
              'lx': 'Single'},
             {'c_target_ywlx': 'all', 'c_source_ywlx': 'all', 'c_target_zdm': 'C_XB', 'c_source_zdm': 'N_XB',
              'c_target_dzdm': '11400000', 'c_source_dzdm': '10100003', 'c_target_jtmz': '0', 'c_source_jtmz': '0',
              'c_sheet_mc': '审判组织成员人民陪审员-spzzcy', 'c_ms': 'spzzcy', 'c_target_bm': 'T_SPZZCY_RMPSY',
              'c_target_sjlx': 'varchar', 'c_source_bm': 'T_YWGY_RMPSY', 'c_system_type': 'np', 'c_group': 'spzzcy',
              'lx': 'Single'}], [
             {'c_target_ywlx': 'all', 'c_source_ywlx': 'all', 'c_target_zdm': 'C_XB', 'c_source_zdm': 'N_XB',
              'c_target_dzdm': '11400000', 'c_source_dzdm': '10100003', 'c_target_jtmz': '1', 'c_source_jtmz': '1',
              'c_sheet_mc': '审判组织成员人民陪审员-spzzcy', 'c_ms': 'spzzcy', 'c_target_bm': 'T_SPZZCY_RMPSY',
              'c_target_sjlx': 'varchar', 'c_source_bm': 'T_YWGY_RMPSY', 'c_system_type': 'np', 'c_group': 'spzzcy',
              'lx': 'Single'},
             {'c_target_ywlx': 'all', 'c_source_ywlx': 'all', 'c_target_zdm': 'C_XB', 'c_source_zdm': 'N_XB',
              'c_target_dzdm': '11400000', 'c_source_dzdm': '10100003', 'c_target_jtmz': '2', 'c_source_jtmz': '2',
              'c_sheet_mc': '审判组织成员人民陪审员-spzzcy', 'c_ms': 'spzzcy', 'c_target_bm': 'T_SPZZCY_RMPSY',
              'c_target_sjlx': 'varchar', 'c_source_bm': 'T_YWGY_RMPSY', 'c_system_type': 'np', 'c_group': 'spzzcy',
              'lx': 'Single'},
             {'c_target_ywlx': 'all', 'c_source_ywlx': 'all', 'c_target_zdm': 'C_XB', 'c_source_zdm': 'N_XB',
              'c_target_dzdm': '11400000', 'c_source_dzdm': '10100003', 'c_target_jtmz': '9', 'c_source_jtmz': None,
              'c_sheet_mc': '审判组织成员人民陪审员-spzzcy', 'c_ms': 'spzzcy', 'c_target_bm': 'T_SPZZCY_RMPSY',
              'c_target_sjlx': 'varchar', 'c_source_bm': 'T_YWGY_RMPSY', 'c_system_type': 'np', 'c_group': 'spzzcy',
              'lx': 'Single'},
             {'c_target_ywlx': 'all', 'c_source_ywlx': 'all', 'c_target_zdm': 'C_XB', 'c_source_zdm': 'N_XB',
              'c_target_dzdm': '11400000', 'c_source_dzdm': '10100003', 'c_target_jtmz': '0', 'c_source_jtmz': '255',
              'c_sheet_mc': '审判组织成员人民陪审员-spzzcy', 'c_ms': 'spzzcy', 'c_target_bm': 'T_SPZZCY_RMPSY',
              'c_target_sjlx': 'varchar', 'c_source_bm': 'T_YWGY_RMPSY', 'c_system_type': 'np', 'c_group': 'spzzcy',
              'lx': 'Single'},
             {'c_target_ywlx': 'all', 'c_source_ywlx': 'all', 'c_target_zdm': 'C_XB', 'c_source_zdm': 'N_XB',
              'c_target_dzdm': '11400000', 'c_source_dzdm': '10100003', 'c_target_jtmz': '0', 'c_source_jtmz': '0',
              'c_sheet_mc': '审判组织成员人民陪审员-spzzcy', 'c_ms': 'spzzcy', 'c_target_bm': 'T_SPZZCY_RMPSY',
              'c_target_sjlx': 'varchar', 'c_source_bm': 'T_YWGY_RMPSY', 'c_system_type': 'np', 'c_group': 'spzzcy',
              'lx': 'Single'}], [
             {'c_target_ywlx': 'all', 'c_source_ywlx': 'all', 'c_target_zdm': 'C_XB', 'c_source_zdm': 'N_XB',
              'c_target_dzdm': '11400000', 'c_source_dzdm': '10100003', 'c_target_jtmz': '1', 'c_source_jtmz': '1',
              'c_sheet_mc': '审判组织成员人民陪审员-spzzcy', 'c_ms': 'spzzcy', 'c_target_bm': 'T_SPZZCY_RMPSY',
              'c_target_sjlx': 'varchar', 'c_source_bm': 'T_YWGY_RMPSY', 'c_system_type': 'np', 'c_group': 'spzzcy',
              'lx': 'Single'},
             {'c_target_ywlx': 'all', 'c_source_ywlx': 'all', 'c_target_zdm': 'C_XB', 'c_source_zdm': 'N_XB',
              'c_target_dzdm': '11400000', 'c_source_dzdm': '10100003', 'c_target_jtmz': '2', 'c_source_jtmz': '2',
              'c_sheet_mc': '审判组织成员人民陪审员-spzzcy', 'c_ms': 'spzzcy', 'c_target_bm': 'T_SPZZCY_RMPSY',
              'c_target_sjlx': 'varchar', 'c_source_bm': 'T_YWGY_RMPSY', 'c_system_type': 'np', 'c_group': 'spzzcy',
              'lx': 'Single'},
             {'c_target_ywlx': 'all', 'c_source_ywlx': 'all', 'c_target_zdm': 'C_XB', 'c_source_zdm': 'N_XB',
              'c_target_dzdm': '11400000', 'c_source_dzdm': '10100003', 'c_target_jtmz': '9', 'c_source_jtmz': None,
              'c_sheet_mc': '审判组织成员人民陪审员-spzzcy', 'c_ms': 'spzzcy', 'c_target_bm': 'T_SPZZCY_RMPSY',
              'c_target_sjlx': 'varchar', 'c_source_bm': 'T_YWGY_RMPSY', 'c_system_type': 'np', 'c_group': 'spzzcy',
              'lx': 'Single'},
             {'c_target_ywlx': 'all', 'c_source_ywlx': 'all', 'c_target_zdm': 'C_XB', 'c_source_zdm': 'N_XB',
              'c_target_dzdm': '11400000', 'c_source_dzdm': '10100003', 'c_target_jtmz': '0', 'c_source_jtmz': '255',
              'c_sheet_mc': '审判组织成员人民陪审员-spzzcy', 'c_ms': 'spzzcy', 'c_target_bm': 'T_SPZZCY_RMPSY',
              'c_target_sjlx': 'varchar', 'c_source_bm': 'T_YWGY_RMPSY', 'c_system_type': 'np', 'c_group': 'spzzcy',
              'lx': 'Single'},
             {'c_target_ywlx': 'all', 'c_source_ywlx': 'all', 'c_target_zdm': 'C_XB', 'c_source_zdm': 'N_XB',
              'c_target_dzdm': '11400000', 'c_source_dzdm': '10100003', 'c_target_jtmz': '0', 'c_source_jtmz': '0',
              'c_sheet_mc': '审判组织成员人民陪审员-spzzcy', 'c_ms': 'spzzcy', 'c_target_bm': 'T_SPZZCY_RMPSY',
              'c_target_sjlx': 'varchar', 'c_source_bm': 'T_YWGY_RMPSY', 'c_system_type': 'np', 'c_group': 'spzzcy',
              'lx': 'Single'}], [
             {'c_target_ywlx': 'all', 'c_source_ywlx': 'all', 'c_target_zdm': 'C_XB', 'c_source_zdm': 'N_XB',
              'c_target_dzdm': '11400000', 'c_source_dzdm': '10100003', 'c_target_jtmz': '1', 'c_source_jtmz': '1',
              'c_sheet_mc': '审判组织成员人民陪审员-spzzcy', 'c_ms': 'spzzcy', 'c_target_bm': 'T_SPZZCY_RMPSY',
              'c_target_sjlx': 'varchar', 'c_source_bm': 'T_YWGY_RMPSY', 'c_system_type': 'np', 'c_group': 'spzzcy',
              'lx': 'Single'},
             {'c_target_ywlx': 'all', 'c_source_ywlx': 'all', 'c_target_zdm': 'C_XB', 'c_source_zdm': 'N_XB',
              'c_target_dzdm': '11400000', 'c_source_dzdm': '10100003', 'c_target_jtmz': '2', 'c_source_jtmz': '2',
              'c_sheet_mc': '审判组织成员人民陪审员-spzzcy', 'c_ms': 'spzzcy', 'c_target_bm': 'T_SPZZCY_RMPSY',
              'c_target_sjlx': 'varchar', 'c_source_bm': 'T_YWGY_RMPSY', 'c_system_type': 'np', 'c_group': 'spzzcy',
              'lx': 'Single'},
             {'c_target_ywlx': 'all', 'c_source_ywlx': 'all', 'c_target_zdm': 'C_XB', 'c_source_zdm': 'N_XB',
              'c_target_dzdm': '11400000', 'c_source_dzdm': '10100003', 'c_target_jtmz': '9', 'c_source_jtmz': None,
              'c_sheet_mc': '审判组织成员人民陪审员-spzzcy', 'c_ms': 'spzzcy', 'c_target_bm': 'T_SPZZCY_RMPSY',
              'c_target_sjlx': 'varchar', 'c_source_bm': 'T_YWGY_RMPSY', 'c_system_type': 'np', 'c_group': 'spzzcy',
              'lx': 'Single'},
             {'c_target_ywlx': 'all', 'c_source_ywlx': 'all', 'c_target_zdm': 'C_XB', 'c_source_zdm': 'N_XB',
              'c_target_dzdm': '11400000', 'c_source_dzdm': '10100003', 'c_target_jtmz': '0', 'c_source_jtmz': '255',
              'c_sheet_mc': '审判组织成员人民陪审员-spzzcy', 'c_ms': 'spzzcy', 'c_target_bm': 'T_SPZZCY_RMPSY',
              'c_target_sjlx': 'varchar', 'c_source_bm': 'T_YWGY_RMPSY', 'c_system_type': 'np', 'c_group': 'spzzcy',
              'lx': 'Single'},
             {'c_target_ywlx': 'all', 'c_source_ywlx': 'all', 'c_target_zdm': 'C_XB', 'c_source_zdm': 'N_XB',
              'c_target_dzdm': '11400000', 'c_source_dzdm': '10100003', 'c_target_jtmz': '0', 'c_source_jtmz': '0',
              'c_sheet_mc': '审判组织成员人民陪审员-spzzcy', 'c_ms': 'spzzcy', 'c_target_bm': 'T_SPZZCY_RMPSY',
              'c_target_sjlx': 'varchar', 'c_source_bm': 'T_YWGY_RMPSY', 'c_system_type': 'np', 'c_group': 'spzzcy',
              'lx': 'Single'}], [
             {'c_target_ywlx': 'all', 'c_source_ywlx': 'all', 'c_target_zdm': 'C_XB', 'c_source_zdm': 'N_XB',
              'c_target_dzdm': '11400000', 'c_source_dzdm': '10100003', 'c_target_jtmz': '1', 'c_source_jtmz': '1',
              'c_sheet_mc': '审判组织成员人民陪审员-spzzcy', 'c_ms': 'spzzcy', 'c_target_bm': 'T_SPZZCY_RMPSY',
              'c_target_sjlx': 'varchar', 'c_source_bm': 'T_YWGY_RMPSY', 'c_system_type': 'np', 'c_group': 'spzzcy',
              'lx': 'Single'},
             {'c_target_ywlx': 'all', 'c_source_ywlx': 'all', 'c_target_zdm': 'C_XB', 'c_source_zdm': 'N_XB',
              'c_target_dzdm': '11400000', 'c_source_dzdm': '10100003', 'c_target_jtmz': '2', 'c_source_jtmz': '2',
              'c_sheet_mc': '审判组织成员人民陪审员-spzzcy', 'c_ms': 'spzzcy', 'c_target_bm': 'T_SPZZCY_RMPSY',
              'c_target_sjlx': 'varchar', 'c_source_bm': 'T_YWGY_RMPSY', 'c_system_type': 'np', 'c_group': 'spzzcy',
              'lx': 'Single'},
             {'c_target_ywlx': 'all', 'c_source_ywlx': 'all', 'c_target_zdm': 'C_XB', 'c_source_zdm': 'N_XB',
              'c_target_dzdm': '11400000', 'c_source_dzdm': '10100003', 'c_target_jtmz': '9', 'c_source_jtmz': None,
              'c_sheet_mc': '审判组织成员人民陪审员-spzzcy', 'c_ms': 'spzzcy', 'c_target_bm': 'T_SPZZCY_RMPSY',
              'c_target_sjlx': 'varchar', 'c_source_bm': 'T_YWGY_RMPSY', 'c_system_type': 'np', 'c_group': 'spzzcy',
              'lx': 'Single'},
             {'c_target_ywlx': 'all', 'c_source_ywlx': 'all', 'c_target_zdm': 'C_XB', 'c_source_zdm': 'N_XB',
              'c_target_dzdm': '11400000', 'c_source_dzdm': '10100003', 'c_target_jtmz': '0', 'c_source_jtmz': '255',
              'c_sheet_mc': '审判组织成员人民陪审员-spzzcy', 'c_ms': 'spzzcy', 'c_target_bm': 'T_SPZZCY_RMPSY',
              'c_target_sjlx': 'varchar', 'c_source_bm': 'T_YWGY_RMPSY', 'c_system_type': 'np', 'c_group': 'spzzcy',
              'lx': 'Single'},
             {'c_target_ywlx': 'all', 'c_source_ywlx': 'all', 'c_target_zdm': 'C_XB', 'c_source_zdm': 'N_XB',
              'c_target_dzdm': '11400000', 'c_source_dzdm': '10100003', 'c_target_jtmz': '0', 'c_source_jtmz': '0',
              'c_sheet_mc': '审判组织成员人民陪审员-spzzcy', 'c_ms': 'spzzcy', 'c_target_bm': 'T_SPZZCY_RMPSY',
              'c_target_sjlx': 'varchar', 'c_source_bm': 'T_YWGY_RMPSY', 'c_system_type': 'np', 'c_group': 'spzzcy',
              'lx': 'Single'}], [
             {'c_target_ywlx': 'all', 'c_source_ywlx': 'all', 'c_target_zdm': 'C_XB', 'c_source_zdm': 'N_XB',
              'c_target_dzdm': '11400000', 'c_source_dzdm': '10100003', 'c_target_jtmz': '1', 'c_source_jtmz': '1',
              'c_sheet_mc': '审判组织成员人民陪审员-spzzcy', 'c_ms': 'spzzcy', 'c_target_bm': 'T_SPZZCY_RMPSY',
              'c_target_sjlx': 'varchar', 'c_source_bm': 'T_YWGY_RMPSY', 'c_system_type': 'np', 'c_group': 'spzzcy',
              'lx': 'Single'},
             {'c_target_ywlx': 'all', 'c_source_ywlx': 'all', 'c_target_zdm': 'C_XB', 'c_source_zdm': 'N_XB',
              'c_target_dzdm': '11400000', 'c_source_dzdm': '10100003', 'c_target_jtmz': '2', 'c_source_jtmz': '2',
              'c_sheet_mc': '审判组织成员人民陪审员-spzzcy', 'c_ms': 'spzzcy', 'c_target_bm': 'T_SPZZCY_RMPSY',
              'c_target_sjlx': 'varchar', 'c_source_bm': 'T_YWGY_RMPSY', 'c_system_type': 'np', 'c_group': 'spzzcy',
              'lx': 'Single'},
             {'c_target_ywlx': 'all', 'c_source_ywlx': 'all', 'c_target_zdm': 'C_XB', 'c_source_zdm': 'N_XB',
              'c_target_dzdm': '11400000', 'c_source_dzdm': '10100003', 'c_target_jtmz': '9', 'c_source_jtmz': None,
              'c_sheet_mc': '审判组织成员人民陪审员-spzzcy', 'c_ms': 'spzzcy', 'c_target_bm': 'T_SPZZCY_RMPSY',
              'c_target_sjlx': 'varchar', 'c_source_bm': 'T_YWGY_RMPSY', 'c_system_type': 'np', 'c_group': 'spzzcy',
              'lx': 'Single'},
             {'c_target_ywlx': 'all', 'c_source_ywlx': 'all', 'c_target_zdm': 'C_XB', 'c_source_zdm': 'N_XB',
              'c_target_dzdm': '11400000', 'c_source_dzdm': '10100003', 'c_target_jtmz': '0', 'c_source_jtmz': '255',
              'c_sheet_mc': '审判组织成员人民陪审员-spzzcy', 'c_ms': 'spzzcy', 'c_target_bm': 'T_SPZZCY_RMPSY',
              'c_target_sjlx': 'varchar', 'c_source_bm': 'T_YWGY_RMPSY', 'c_system_type': 'np', 'c_group': 'spzzcy',
              'lx': 'Single'},
             {'c_target_ywlx': 'all', 'c_source_ywlx': 'all', 'c_target_zdm': 'C_XB', 'c_source_zdm': 'N_XB',
              'c_target_dzdm': '11400000', 'c_source_dzdm': '10100003', 'c_target_jtmz': '0', 'c_source_jtmz': '0',
              'c_sheet_mc': '审判组织成员人民陪审员-spzzcy', 'c_ms': 'spzzcy', 'c_target_bm': 'T_SPZZCY_RMPSY',
              'c_target_sjlx': 'varchar', 'c_source_bm': 'T_YWGY_RMPSY', 'c_system_type': 'np', 'c_group': 'spzzcy',
              'lx': 'Single'}], [
             {'c_target_ywlx': 'all', 'c_source_ywlx': 'all', 'c_target_zdm': 'C_XB', 'c_source_zdm': 'N_XB',
              'c_target_dzdm': '11400000', 'c_source_dzdm': '10100003', 'c_target_jtmz': '1', 'c_source_jtmz': '1',
              'c_sheet_mc': '审判组织成员人民陪审员-spzzcy', 'c_ms': 'spzzcy', 'c_target_bm': 'T_SPZZCY_RMPSY',
              'c_target_sjlx': 'varchar', 'c_source_bm': 'T_YWGY_RMPSY', 'c_system_type': 'np', 'c_group': 'spzzcy',
              'lx': 'Single'},
             {'c_target_ywlx': 'all', 'c_source_ywlx': 'all', 'c_target_zdm': 'C_XB', 'c_source_zdm': 'N_XB',
              'c_target_dzdm': '11400000', 'c_source_dzdm': '10100003', 'c_target_jtmz': '2', 'c_source_jtmz': '2',
              'c_sheet_mc': '审判组织成员人民陪审员-spzzcy', 'c_ms': 'spzzcy', 'c_target_bm': 'T_SPZZCY_RMPSY',
              'c_target_sjlx': 'varchar', 'c_source_bm': 'T_YWGY_RMPSY', 'c_system_type': 'np', 'c_group': 'spzzcy',
              'lx': 'Single'},
             {'c_target_ywlx': 'all', 'c_source_ywlx': 'all', 'c_target_zdm': 'C_XB', 'c_source_zdm': 'N_XB',
              'c_target_dzdm': '11400000', 'c_source_dzdm': '10100003', 'c_target_jtmz': '9', 'c_source_jtmz': None,
              'c_sheet_mc': '审判组织成员人民陪审员-spzzcy', 'c_ms': 'spzzcy', 'c_target_bm': 'T_SPZZCY_RMPSY',
              'c_target_sjlx': 'varchar', 'c_source_bm': 'T_YWGY_RMPSY', 'c_system_type': 'np', 'c_group': 'spzzcy',
              'lx': 'Single'},
             {'c_target_ywlx': 'all', 'c_source_ywlx': 'all', 'c_target_zdm': 'C_XB', 'c_source_zdm': 'N_XB',
              'c_target_dzdm': '11400000', 'c_source_dzdm': '10100003', 'c_target_jtmz': '0', 'c_source_jtmz': '255',
              'c_sheet_mc': '审判组织成员人民陪审员-spzzcy', 'c_ms': 'spzzcy', 'c_target_bm': 'T_SPZZCY_RMPSY',
              'c_target_sjlx': 'varchar', 'c_source_bm': 'T_YWGY_RMPSY', 'c_system_type': 'np', 'c_group': 'spzzcy',
              'lx': 'Single'},
             {'c_target_ywlx': 'all', 'c_source_ywlx': 'all', 'c_target_zdm': 'C_XB', 'c_source_zdm': 'N_XB',
              'c_target_dzdm': '11400000', 'c_source_dzdm': '10100003', 'c_target_jtmz': '0', 'c_source_jtmz': '0',
              'c_sheet_mc': '审判组织成员人民陪审员-spzzcy', 'c_ms': 'spzzcy', 'c_target_bm': 'T_SPZZCY_RMPSY',
              'c_target_sjlx': 'varchar', 'c_source_bm': 'T_YWGY_RMPSY', 'c_system_type': 'np', 'c_group': 'spzzcy',
              'lx': 'Single'}], [
             {'c_target_ywlx': 'all', 'c_source_ywlx': 'all', 'c_target_zdm': 'C_XB', 'c_source_zdm': 'N_XB',
              'c_target_dzdm': '11400000', 'c_source_dzdm': '10100003', 'c_target_jtmz': '1', 'c_source_jtmz': '1',
              'c_sheet_mc': '审判组织成员人民陪审员-spzzcy', 'c_ms': 'spzzcy', 'c_target_bm': 'T_SPZZCY_RMPSY',
              'c_target_sjlx': 'varchar', 'c_source_bm': 'T_YWGY_RMPSY', 'c_system_type': 'np', 'c_group': 'spzzcy',
              'lx': 'Single'},
             {'c_target_ywlx': 'all', 'c_source_ywlx': 'all', 'c_target_zdm': 'C_XB', 'c_source_zdm': 'N_XB',
              'c_target_dzdm': '11400000', 'c_source_dzdm': '10100003', 'c_target_jtmz': '2', 'c_source_jtmz': '2',
              'c_sheet_mc': '审判组织成员人民陪审员-spzzcy', 'c_ms': 'spzzcy', 'c_target_bm': 'T_SPZZCY_RMPSY',
              'c_target_sjlx': 'varchar', 'c_source_bm': 'T_YWGY_RMPSY', 'c_system_type': 'np', 'c_group': 'spzzcy',
              'lx': 'Single'},
             {'c_target_ywlx': 'all', 'c_source_ywlx': 'all', 'c_target_zdm': 'C_XB', 'c_source_zdm': 'N_XB',
              'c_target_dzdm': '11400000', 'c_source_dzdm': '10100003', 'c_target_jtmz': '9', 'c_source_jtmz': None,
              'c_sheet_mc': '审判组织成员人民陪审员-spzzcy', 'c_ms': 'spzzcy', 'c_target_bm': 'T_SPZZCY_RMPSY',
              'c_target_sjlx': 'varchar', 'c_source_bm': 'T_YWGY_RMPSY', 'c_system_type': 'np', 'c_group': 'spzzcy',
              'lx': 'Single'},
             {'c_target_ywlx': 'all', 'c_source_ywlx': 'all', 'c_target_zdm': 'C_XB', 'c_source_zdm': 'N_XB',
              'c_target_dzdm': '11400000', 'c_source_dzdm': '10100003', 'c_target_jtmz': '0', 'c_source_jtmz': '255',
              'c_sheet_mc': '审判组织成员人民陪审员-spzzcy', 'c_ms': 'spzzcy', 'c_target_bm': 'T_SPZZCY_RMPSY',
              'c_target_sjlx': 'varchar', 'c_source_bm': 'T_YWGY_RMPSY', 'c_system_type': 'np', 'c_group': 'spzzcy',
              'lx': 'Single'},
             {'c_target_ywlx': 'all', 'c_source_ywlx': 'all', 'c_target_zdm': 'C_XB', 'c_source_zdm': 'N_XB',
              'c_target_dzdm': '11400000', 'c_source_dzdm': '10100003', 'c_target_jtmz': '0', 'c_source_jtmz': '0',
              'c_sheet_mc': '审判组织成员人民陪审员-spzzcy', 'c_ms': 'spzzcy', 'c_target_bm': 'T_SPZZCY_RMPSY',
              'c_target_sjlx': 'varchar', 'c_source_bm': 'T_YWGY_RMPSY', 'c_system_type': 'np', 'c_group': 'spzzcy',
              'lx': 'Single'}], [
             {'c_target_ywlx': 'all', 'c_source_ywlx': 'all', 'c_target_zdm': 'C_XB', 'c_source_zdm': 'N_XB',
              'c_target_dzdm': '11400000', 'c_source_dzdm': '10100003', 'c_target_jtmz': '1', 'c_source_jtmz': '1',
              'c_sheet_mc': '审判组织成员人民陪审员-spzzcy', 'c_ms': 'spzzcy', 'c_target_bm': 'T_SPZZCY_RMPSY',
              'c_target_sjlx': 'varchar', 'c_source_bm': 'T_YWGY_RMPSY', 'c_system_type': 'np', 'c_group': 'spzzcy',
              'lx': 'Single'},
             {'c_target_ywlx': 'all', 'c_source_ywlx': 'all', 'c_target_zdm': 'C_XB', 'c_source_zdm': 'N_XB',
              'c_target_dzdm': '11400000', 'c_source_dzdm': '10100003', 'c_target_jtmz': '2', 'c_source_jtmz': '2',
              'c_sheet_mc': '审判组织成员人民陪审员-spzzcy', 'c_ms': 'spzzcy', 'c_target_bm': 'T_SPZZCY_RMPSY',
              'c_target_sjlx': 'varchar', 'c_source_bm': 'T_YWGY_RMPSY', 'c_system_type': 'np', 'c_group': 'spzzcy',
              'lx': 'Single'},
             {'c_target_ywlx': 'all', 'c_source_ywlx': 'all', 'c_target_zdm': 'C_XB', 'c_source_zdm': 'N_XB',
              'c_target_dzdm': '11400000', 'c_source_dzdm': '10100003', 'c_target_jtmz': '9', 'c_source_jtmz': None,
              'c_sheet_mc': '审判组织成员人民陪审员-spzzcy', 'c_ms': 'spzzcy', 'c_target_bm': 'T_SPZZCY_RMPSY',
              'c_target_sjlx': 'varchar', 'c_source_bm': 'T_YWGY_RMPSY', 'c_system_type': 'np', 'c_group': 'spzzcy',
              'lx': 'Single'},
             {'c_target_ywlx': 'all', 'c_source_ywlx': 'all', 'c_target_zdm': 'C_XB', 'c_source_zdm': 'N_XB',
              'c_target_dzdm': '11400000', 'c_source_dzdm': '10100003', 'c_target_jtmz': '0', 'c_source_jtmz': '255',
              'c_sheet_mc': '审判组织成员人民陪审员-spzzcy', 'c_ms': 'spzzcy', 'c_target_bm': 'T_SPZZCY_RMPSY',
              'c_target_sjlx': 'varchar', 'c_source_bm': 'T_YWGY_RMPSY', 'c_system_type': 'np', 'c_group': 'spzzcy',
              'lx': 'Single'},
             {'c_target_ywlx': 'all', 'c_source_ywlx': 'all', 'c_target_zdm': 'C_XB', 'c_source_zdm': 'N_XB',
              'c_target_dzdm': '11400000', 'c_source_dzdm': '10100003', 'c_target_jtmz': '0', 'c_source_jtmz': '0',
              'c_sheet_mc': '审判组织成员人民陪审员-spzzcy', 'c_ms': 'spzzcy', 'c_target_bm': 'T_SPZZCY_RMPSY',
              'c_target_sjlx': 'varchar', 'c_source_bm': 'T_YWGY_RMPSY', 'c_system_type': 'np', 'c_group': 'spzzcy',
              'lx': 'Single'}], [
             {'c_target_ywlx': 'all', 'c_source_ywlx': 'all', 'c_target_zdm': 'C_XB', 'c_source_zdm': 'N_XB',
              'c_target_dzdm': '11400000', 'c_source_dzdm': '10100003', 'c_target_jtmz': '1', 'c_source_jtmz': '1',
              'c_sheet_mc': '审判组织成员人民陪审员-spzzcy', 'c_ms': 'spzzcy', 'c_target_bm': 'T_SPZZCY_RMPSY',
              'c_target_sjlx': 'varchar', 'c_source_bm': 'T_YWGY_RMPSY', 'c_system_type': 'np', 'c_group': 'spzzcy',
              'lx': 'Single'},
             {'c_target_ywlx': 'all', 'c_source_ywlx': 'all', 'c_target_zdm': 'C_XB', 'c_source_zdm': 'N_XB',
              'c_target_dzdm': '11400000', 'c_source_dzdm': '10100003', 'c_target_jtmz': '2', 'c_source_jtmz': '2',
              'c_sheet_mc': '审判组织成员人民陪审员-spzzcy', 'c_ms': 'spzzcy', 'c_target_bm': 'T_SPZZCY_RMPSY',
              'c_target_sjlx': 'varchar', 'c_source_bm': 'T_YWGY_RMPSY', 'c_system_type': 'np', 'c_group': 'spzzcy',
              'lx': 'Single'},
             {'c_target_ywlx': 'all', 'c_source_ywlx': 'all', 'c_target_zdm': 'C_XB', 'c_source_zdm': 'N_XB',
              'c_target_dzdm': '11400000', 'c_source_dzdm': '10100003', 'c_target_jtmz': '9', 'c_source_jtmz': None,
              'c_sheet_mc': '审判组织成员人民陪审员-spzzcy', 'c_ms': 'spzzcy', 'c_target_bm': 'T_SPZZCY_RMPSY',
              'c_target_sjlx': 'varchar', 'c_source_bm': 'T_YWGY_RMPSY', 'c_system_type': 'np', 'c_group': 'spzzcy',
              'lx': 'Single'},
             {'c_target_ywlx': 'all', 'c_source_ywlx': 'all', 'c_target_zdm': 'C_XB', 'c_source_zdm': 'N_XB',
              'c_target_dzdm': '11400000', 'c_source_dzdm': '10100003', 'c_target_jtmz': '0', 'c_source_jtmz': '255',
              'c_sheet_mc': '审判组织成员人民陪审员-spzzcy', 'c_ms': 'spzzcy', 'c_target_bm': 'T_SPZZCY_RMPSY',
              'c_target_sjlx': 'varchar', 'c_source_bm': 'T_YWGY_RMPSY', 'c_system_type': 'np', 'c_group': 'spzzcy',
              'lx': 'Single'},
             {'c_target_ywlx': 'all', 'c_source_ywlx': 'all', 'c_target_zdm': 'C_XB', 'c_source_zdm': 'N_XB',
              'c_target_dzdm': '11400000', 'c_source_dzdm': '10100003', 'c_target_jtmz': '0', 'c_source_jtmz': '0',
              'c_sheet_mc': '审判组织成员人民陪审员-spzzcy', 'c_ms': 'spzzcy', 'c_target_bm': 'T_SPZZCY_RMPSY',
              'c_target_sjlx': 'varchar', 'c_source_bm': 'T_YWGY_RMPSY', 'c_system_type': 'np', 'c_group': 'spzzcy',
              'lx': 'Single'}], [
             {'c_target_ywlx': 'all', 'c_source_ywlx': 'all', 'c_target_zdm': 'C_XB', 'c_source_zdm': 'N_XB',
              'c_target_dzdm': '11400000', 'c_source_dzdm': '10100003', 'c_target_jtmz': '1', 'c_source_jtmz': '1',
              'c_sheet_mc': '审判组织成员人民陪审员-spzzcy', 'c_ms': 'spzzcy', 'c_target_bm': 'T_SPZZCY_RMPSY',
              'c_target_sjlx': 'varchar', 'c_source_bm': 'T_YWGY_RMPSY', 'c_system_type': 'np', 'c_group': 'spzzcy',
              'lx': 'Single'},
             {'c_target_ywlx': 'all', 'c_source_ywlx': 'all', 'c_target_zdm': 'C_XB', 'c_source_zdm': 'N_XB',
              'c_target_dzdm': '11400000', 'c_source_dzdm': '10100003', 'c_target_jtmz': '2', 'c_source_jtmz': '2',
              'c_sheet_mc': '审判组织成员人民陪审员-spzzcy', 'c_ms': 'spzzcy', 'c_target_bm': 'T_SPZZCY_RMPSY',
              'c_target_sjlx': 'varchar', 'c_source_bm': 'T_YWGY_RMPSY', 'c_system_type': 'np', 'c_group': 'spzzcy',
              'lx': 'Single'},
             {'c_target_ywlx': 'all', 'c_source_ywlx': 'all', 'c_target_zdm': 'C_XB', 'c_source_zdm': 'N_XB',
              'c_target_dzdm': '11400000', 'c_source_dzdm': '10100003', 'c_target_jtmz': '9', 'c_source_jtmz': None,
              'c_sheet_mc': '审判组织成员人民陪审员-spzzcy', 'c_ms': 'spzzcy', 'c_target_bm': 'T_SPZZCY_RMPSY',
              'c_target_sjlx': 'varchar', 'c_source_bm': 'T_YWGY_RMPSY', 'c_system_type': 'np', 'c_group': 'spzzcy',
              'lx': 'Single'},
             {'c_target_ywlx': 'all', 'c_source_ywlx': 'all', 'c_target_zdm': 'C_XB', 'c_source_zdm': 'N_XB',
              'c_target_dzdm': '11400000', 'c_source_dzdm': '10100003', 'c_target_jtmz': '0', 'c_source_jtmz': '255',
              'c_sheet_mc': '审判组织成员人民陪审员-spzzcy', 'c_ms': 'spzzcy', 'c_target_bm': 'T_SPZZCY_RMPSY',
              'c_target_sjlx': 'varchar', 'c_source_bm': 'T_YWGY_RMPSY', 'c_system_type': 'np', 'c_group': 'spzzcy',
              'lx': 'Single'},
             {'c_target_ywlx': 'all', 'c_source_ywlx': 'all', 'c_target_zdm': 'C_XB', 'c_source_zdm': 'N_XB',
              'c_target_dzdm': '11400000', 'c_source_dzdm': '10100003', 'c_target_jtmz': '0', 'c_source_jtmz': '0',
              'c_sheet_mc': '审判组织成员人民陪审员-spzzcy', 'c_ms': 'spzzcy', 'c_target_bm': 'T_SPZZCY_RMPSY',
              'c_target_sjlx': 'varchar', 'c_source_bm': 'T_YWGY_RMPSY', 'c_system_type': 'np', 'c_group': 'spzzcy',
              'lx': 'Single'}], [
             {'c_target_ywlx': 'all', 'c_source_ywlx': 'all', 'c_target_zdm': 'C_XB', 'c_source_zdm': 'N_XB',
              'c_target_dzdm': '11400000', 'c_source_dzdm': '10100003', 'c_target_jtmz': '1', 'c_source_jtmz': '1',
              'c_sheet_mc': '审判组织成员人民陪审员-spzzcy', 'c_ms': 'spzzcy', 'c_target_bm': 'T_SPZZCY_RMPSY',
              'c_target_sjlx': 'varchar', 'c_source_bm': 'T_YWGY_RMPSY', 'c_system_type': 'np', 'c_group': 'spzzcy',
              'lx': 'Single'},
             {'c_target_ywlx': 'all', 'c_source_ywlx': 'all', 'c_target_zdm': 'C_XB', 'c_source_zdm': 'N_XB',
              'c_target_dzdm': '11400000', 'c_source_dzdm': '10100003', 'c_target_jtmz': '2', 'c_source_jtmz': '2',
              'c_sheet_mc': '审判组织成员人民陪审员-spzzcy', 'c_ms': 'spzzcy', 'c_target_bm': 'T_SPZZCY_RMPSY',
              'c_target_sjlx': 'varchar', 'c_source_bm': 'T_YWGY_RMPSY', 'c_system_type': 'np', 'c_group': 'spzzcy',
              'lx': 'Single'},
             {'c_target_ywlx': 'all', 'c_source_ywlx': 'all', 'c_target_zdm': 'C_XB', 'c_source_zdm': 'N_XB',
              'c_target_dzdm': '11400000', 'c_source_dzdm': '10100003', 'c_target_jtmz': '9', 'c_source_jtmz': None,
              'c_sheet_mc': '审判组织成员人民陪审员-spzzcy', 'c_ms': 'spzzcy', 'c_target_bm': 'T_SPZZCY_RMPSY',
              'c_target_sjlx': 'varchar', 'c_source_bm': 'T_YWGY_RMPSY', 'c_system_type': 'np', 'c_group': 'spzzcy',
              'lx': 'Single'},
             {'c_target_ywlx': 'all', 'c_source_ywlx': 'all', 'c_target_zdm': 'C_XB', 'c_source_zdm': 'N_XB',
              'c_target_dzdm': '11400000', 'c_source_dzdm': '10100003', 'c_target_jtmz': '0', 'c_source_jtmz': '255',
              'c_sheet_mc': '审判组织成员人民陪审员-spzzcy', 'c_ms': 'spzzcy', 'c_target_bm': 'T_SPZZCY_RMPSY',
              'c_target_sjlx': 'varchar', 'c_source_bm': 'T_YWGY_RMPSY', 'c_system_type': 'np', 'c_group': 'spzzcy',
              'lx': 'Single'},
             {'c_target_ywlx': 'all', 'c_source_ywlx': 'all', 'c_target_zdm': 'C_XB', 'c_source_zdm': 'N_XB',
              'c_target_dzdm': '11400000', 'c_source_dzdm': '10100003', 'c_target_jtmz': '0', 'c_source_jtmz': '0',
              'c_sheet_mc': '审判组织成员人民陪审员-spzzcy', 'c_ms': 'spzzcy', 'c_target_bm': 'T_SPZZCY_RMPSY',
              'c_target_sjlx': 'varchar', 'c_source_bm': 'T_YWGY_RMPSY', 'c_system_type': 'np', 'c_group': 'spzzcy',
              'lx': 'Single'}], [
             {'c_target_ywlx': 'all', 'c_source_ywlx': 'all', 'c_target_zdm': 'C_XB', 'c_source_zdm': 'N_XB',
              'c_target_dzdm': '11400000', 'c_source_dzdm': '10100003', 'c_target_jtmz': '1', 'c_source_jtmz': '1',
              'c_sheet_mc': '审判组织成员人民陪审员-spzzcy', 'c_ms': 'spzzcy', 'c_target_bm': 'T_SPZZCY_RMPSY',
              'c_target_sjlx': 'varchar', 'c_source_bm': 'T_YWGY_RMPSY', 'c_system_type': 'np', 'c_group': 'spzzcy',
              'lx': 'Single'},
             {'c_target_ywlx': 'all', 'c_source_ywlx': 'all', 'c_target_zdm': 'C_XB', 'c_source_zdm': 'N_XB',
              'c_target_dzdm': '11400000', 'c_source_dzdm': '10100003', 'c_target_jtmz': '2', 'c_source_jtmz': '2',
              'c_sheet_mc': '审判组织成员人民陪审员-spzzcy', 'c_ms': 'spzzcy', 'c_target_bm': 'T_SPZZCY_RMPSY',
              'c_target_sjlx': 'varchar', 'c_source_bm': 'T_YWGY_RMPSY', 'c_system_type': 'np', 'c_group': 'spzzcy',
              'lx': 'Single'},
             {'c_target_ywlx': 'all', 'c_source_ywlx': 'all', 'c_target_zdm': 'C_XB', 'c_source_zdm': 'N_XB',
              'c_target_dzdm': '11400000', 'c_source_dzdm': '10100003', 'c_target_jtmz': '9', 'c_source_jtmz': None,
              'c_sheet_mc': '审判组织成员人民陪审员-spzzcy', 'c_ms': 'spzzcy', 'c_target_bm': 'T_SPZZCY_RMPSY',
              'c_target_sjlx': 'varchar', 'c_source_bm': 'T_YWGY_RMPSY', 'c_system_type': 'np', 'c_group': 'spzzcy',
              'lx': 'Single'},
             {'c_target_ywlx': 'all', 'c_source_ywlx': 'all', 'c_target_zdm': 'C_XB', 'c_source_zdm': 'N_XB',
              'c_target_dzdm': '11400000', 'c_source_dzdm': '10100003', 'c_target_jtmz': '0', 'c_source_jtmz': '255',
              'c_sheet_mc': '审判组织成员人民陪审员-spzzcy', 'c_ms': 'spzzcy', 'c_target_bm': 'T_SPZZCY_RMPSY',
              'c_target_sjlx': 'varchar', 'c_source_bm': 'T_YWGY_RMPSY', 'c_system_type': 'np', 'c_group': 'spzzcy',
              'lx': 'Single'},
             {'c_target_ywlx': 'all', 'c_source_ywlx': 'all', 'c_target_zdm': 'C_XB', 'c_source_zdm': 'N_XB',
              'c_target_dzdm': '11400000', 'c_source_dzdm': '10100003', 'c_target_jtmz': '0', 'c_source_jtmz': '0',
              'c_sheet_mc': '审判组织成员人民陪审员-spzzcy', 'c_ms': 'spzzcy', 'c_target_bm': 'T_SPZZCY_RMPSY',
              'c_target_sjlx': 'varchar', 'c_source_bm': 'T_YWGY_RMPSY', 'c_system_type': 'np', 'c_group': 'spzzcy',
              'lx': 'Single'}], [
             {'c_target_ywlx': 'all', 'c_source_ywlx': 'all', 'c_target_zdm': 'C_XB', 'c_source_zdm': 'N_XB',
              'c_target_dzdm': '11400000', 'c_source_dzdm': '10100003', 'c_target_jtmz': '1', 'c_source_jtmz': '1',
              'c_sheet_mc': '审判组织成员人民陪审员-spzzcy', 'c_ms': 'spzzcy', 'c_target_bm': 'T_SPZZCY_RMPSY',
              'c_target_sjlx': 'varchar', 'c_source_bm': 'T_YWGY_RMPSY', 'c_system_type': 'np', 'c_group': 'spzzcy',
              'lx': 'Single'},
             {'c_target_ywlx': 'all', 'c_source_ywlx': 'all', 'c_target_zdm': 'C_XB', 'c_source_zdm': 'N_XB',
              'c_target_dzdm': '11400000', 'c_source_dzdm': '10100003', 'c_target_jtmz': '2', 'c_source_jtmz': '2',
              'c_sheet_mc': '审判组织成员人民陪审员-spzzcy', 'c_ms': 'spzzcy', 'c_target_bm': 'T_SPZZCY_RMPSY',
              'c_target_sjlx': 'varchar', 'c_source_bm': 'T_YWGY_RMPSY', 'c_system_type': 'np', 'c_group': 'spzzcy',
              'lx': 'Single'},
             {'c_target_ywlx': 'all', 'c_source_ywlx': 'all', 'c_target_zdm': 'C_XB', 'c_source_zdm': 'N_XB',
              'c_target_dzdm': '11400000', 'c_source_dzdm': '10100003', 'c_target_jtmz': '9', 'c_source_jtmz': None,
              'c_sheet_mc': '审判组织成员人民陪审员-spzzcy', 'c_ms': 'spzzcy', 'c_target_bm': 'T_SPZZCY_RMPSY',
              'c_target_sjlx': 'varchar', 'c_source_bm': 'T_YWGY_RMPSY', 'c_system_type': 'np', 'c_group': 'spzzcy',
              'lx': 'Single'},
             {'c_target_ywlx': 'all', 'c_source_ywlx': 'all', 'c_target_zdm': 'C_XB', 'c_source_zdm': 'N_XB',
              'c_target_dzdm': '11400000', 'c_source_dzdm': '10100003', 'c_target_jtmz': '0', 'c_source_jtmz': '255',
              'c_sheet_mc': '审判组织成员人民陪审员-spzzcy', 'c_ms': 'spzzcy', 'c_target_bm': 'T_SPZZCY_RMPSY',
              'c_target_sjlx': 'varchar', 'c_source_bm': 'T_YWGY_RMPSY', 'c_system_type': 'np', 'c_group': 'spzzcy',
              'lx': 'Single'},
             {'c_target_ywlx': 'all', 'c_source_ywlx': 'all', 'c_target_zdm': 'C_XB', 'c_source_zdm': 'N_XB',
              'c_target_dzdm': '11400000', 'c_source_dzdm': '10100003', 'c_target_jtmz': '0', 'c_source_jtmz': '0',
              'c_sheet_mc': '审判组织成员人民陪审员-spzzcy', 'c_ms': 'spzzcy', 'c_target_bm': 'T_SPZZCY_RMPSY',
              'c_target_sjlx': 'varchar', 'c_source_bm': 'T_YWGY_RMPSY', 'c_system_type': 'np', 'c_group': 'spzzcy',
              'lx': 'Single'}], [
             {'c_target_ywlx': 'all', 'c_source_ywlx': 'all', 'c_target_zdm': 'C_XB', 'c_source_zdm': 'N_XB',
              'c_target_dzdm': '11400000', 'c_source_dzdm': '10100003', 'c_target_jtmz': '1', 'c_source_jtmz': '1',
              'c_sheet_mc': '审判组织成员人民陪审员-spzzcy', 'c_ms': 'spzzcy', 'c_target_bm': 'T_SPZZCY_RMPSY',
              'c_target_sjlx': 'varchar', 'c_source_bm': 'T_YWGY_RMPSY', 'c_system_type': 'np', 'c_group': 'spzzcy',
              'lx': 'Single'},
             {'c_target_ywlx': 'all', 'c_source_ywlx': 'all', 'c_target_zdm': 'C_XB', 'c_source_zdm': 'N_XB',
              'c_target_dzdm': '11400000', 'c_source_dzdm': '10100003', 'c_target_jtmz': '2', 'c_source_jtmz': '2',
              'c_sheet_mc': '审判组织成员人民陪审员-spzzcy', 'c_ms': 'spzzcy', 'c_target_bm': 'T_SPZZCY_RMPSY',
              'c_target_sjlx': 'varchar', 'c_source_bm': 'T_YWGY_RMPSY', 'c_system_type': 'np', 'c_group': 'spzzcy',
              'lx': 'Single'},
             {'c_target_ywlx': 'all', 'c_source_ywlx': 'all', 'c_target_zdm': 'C_XB', 'c_source_zdm': 'N_XB',
              'c_target_dzdm': '11400000', 'c_source_dzdm': '10100003', 'c_target_jtmz': '9', 'c_source_jtmz': None,
              'c_sheet_mc': '审判组织成员人民陪审员-spzzcy', 'c_ms': 'spzzcy', 'c_target_bm': 'T_SPZZCY_RMPSY',
              'c_target_sjlx': 'varchar', 'c_source_bm': 'T_YWGY_RMPSY', 'c_system_type': 'np', 'c_group': 'spzzcy',
              'lx': 'Single'},
             {'c_target_ywlx': 'all', 'c_source_ywlx': 'all', 'c_target_zdm': 'C_XB', 'c_source_zdm': 'N_XB',
              'c_target_dzdm': '11400000', 'c_source_dzdm': '10100003', 'c_target_jtmz': '0', 'c_source_jtmz': '255',
              'c_sheet_mc': '审判组织成员人民陪审员-spzzcy', 'c_ms': 'spzzcy', 'c_target_bm': 'T_SPZZCY_RMPSY',
              'c_target_sjlx': 'varchar', 'c_source_bm': 'T_YWGY_RMPSY', 'c_system_type': 'np', 'c_group': 'spzzcy',
              'lx': 'Single'},
             {'c_target_ywlx': 'all', 'c_source_ywlx': 'all', 'c_target_zdm': 'C_XB', 'c_source_zdm': 'N_XB',
              'c_target_dzdm': '11400000', 'c_source_dzdm': '10100003', 'c_target_jtmz': '0', 'c_source_jtmz': '0',
              'c_sheet_mc': '审判组织成员人民陪审员-spzzcy', 'c_ms': 'spzzcy', 'c_target_bm': 'T_SPZZCY_RMPSY',
              'c_target_sjlx': 'varchar', 'c_source_bm': 'T_YWGY_RMPSY', 'c_system_type': 'np', 'c_group': 'spzzcy',
              'lx': 'Single'}], [
             {'c_target_ywlx': 'all', 'c_source_ywlx': 'all', 'c_target_zdm': 'C_XB', 'c_source_zdm': 'N_XB',
              'c_target_dzdm': '11400000', 'c_source_dzdm': '10100003', 'c_target_jtmz': '1', 'c_source_jtmz': '1',
              'c_sheet_mc': '审判组织成员人民陪审员-spzzcy', 'c_ms': 'spzzcy', 'c_target_bm': 'T_SPZZCY_RMPSY',
              'c_target_sjlx': 'varchar', 'c_source_bm': 'T_YWGY_RMPSY', 'c_system_type': 'np', 'c_group': 'spzzcy',
              'lx': 'Single'},
             {'c_target_ywlx': 'all', 'c_source_ywlx': 'all', 'c_target_zdm': 'C_XB', 'c_source_zdm': 'N_XB',
              'c_target_dzdm': '11400000', 'c_source_dzdm': '10100003', 'c_target_jtmz': '2', 'c_source_jtmz': '2',
              'c_sheet_mc': '审判组织成员人民陪审员-spzzcy', 'c_ms': 'spzzcy', 'c_target_bm': 'T_SPZZCY_RMPSY',
              'c_target_sjlx': 'varchar', 'c_source_bm': 'T_YWGY_RMPSY', 'c_system_type': 'np', 'c_group': 'spzzcy',
              'lx': 'Single'},
             {'c_target_ywlx': 'all', 'c_source_ywlx': 'all', 'c_target_zdm': 'C_XB', 'c_source_zdm': 'N_XB',
              'c_target_dzdm': '11400000', 'c_source_dzdm': '10100003', 'c_target_jtmz': '9', 'c_source_jtmz': None,
              'c_sheet_mc': '审判组织成员人民陪审员-spzzcy', 'c_ms': 'spzzcy', 'c_target_bm': 'T_SPZZCY_RMPSY',
              'c_target_sjlx': 'varchar', 'c_source_bm': 'T_YWGY_RMPSY', 'c_system_type': 'np', 'c_group': 'spzzcy',
              'lx': 'Single'},
             {'c_target_ywlx': 'all', 'c_source_ywlx': 'all', 'c_target_zdm': 'C_XB', 'c_source_zdm': 'N_XB',
              'c_target_dzdm': '11400000', 'c_source_dzdm': '10100003', 'c_target_jtmz': '0', 'c_source_jtmz': '255',
              'c_sheet_mc': '审判组织成员人民陪审员-spzzcy', 'c_ms': 'spzzcy', 'c_target_bm': 'T_SPZZCY_RMPSY',
              'c_target_sjlx': 'varchar', 'c_source_bm': 'T_YWGY_RMPSY', 'c_system_type': 'np', 'c_group': 'spzzcy',
              'lx': 'Single'},
             {'c_target_ywlx': 'all', 'c_source_ywlx': 'all', 'c_target_zdm': 'C_XB', 'c_source_zdm': 'N_XB',
              'c_target_dzdm': '11400000', 'c_source_dzdm': '10100003', 'c_target_jtmz': '0', 'c_source_jtmz': '0',
              'c_sheet_mc': '审判组织成员人民陪审员-spzzcy', 'c_ms': 'spzzcy', 'c_target_bm': 'T_SPZZCY_RMPSY',
              'c_target_sjlx': 'varchar', 'c_source_bm': 'T_YWGY_RMPSY', 'c_system_type': 'np', 'c_group': 'spzzcy',
              'lx': 'Single'}], [
             {'c_target_ywlx': 'all', 'c_source_ywlx': 'all', 'c_target_zdm': 'C_XB', 'c_source_zdm': 'N_XB',
              'c_target_dzdm': '11400000', 'c_source_dzdm': '10100003', 'c_target_jtmz': '1', 'c_source_jtmz': '1',
              'c_sheet_mc': '审判组织成员人民陪审员-spzzcy', 'c_ms': 'spzzcy', 'c_target_bm': 'T_SPZZCY_RMPSY',
              'c_target_sjlx': 'varchar', 'c_source_bm': 'T_YWGY_RMPSY', 'c_system_type': 'np', 'c_group': 'spzzcy',
              'lx': 'Single'},
             {'c_target_ywlx': 'all', 'c_source_ywlx': 'all', 'c_target_zdm': 'C_XB', 'c_source_zdm': 'N_XB',
              'c_target_dzdm': '11400000', 'c_source_dzdm': '10100003', 'c_target_jtmz': '2', 'c_source_jtmz': '2',
              'c_sheet_mc': '审判组织成员人民陪审员-spzzcy', 'c_ms': 'spzzcy', 'c_target_bm': 'T_SPZZCY_RMPSY',
              'c_target_sjlx': 'varchar', 'c_source_bm': 'T_YWGY_RMPSY', 'c_system_type': 'np', 'c_group': 'spzzcy',
              'lx': 'Single'},
             {'c_target_ywlx': 'all', 'c_source_ywlx': 'all', 'c_target_zdm': 'C_XB', 'c_source_zdm': 'N_XB',
              'c_target_dzdm': '11400000', 'c_source_dzdm': '10100003', 'c_target_jtmz': '9', 'c_source_jtmz': None,
              'c_sheet_mc': '审判组织成员人民陪审员-spzzcy', 'c_ms': 'spzzcy', 'c_target_bm': 'T_SPZZCY_RMPSY',
              'c_target_sjlx': 'varchar', 'c_source_bm': 'T_YWGY_RMPSY', 'c_system_type': 'np', 'c_group': 'spzzcy',
              'lx': 'Single'},
             {'c_target_ywlx': 'all', 'c_source_ywlx': 'all', 'c_target_zdm': 'C_XB', 'c_source_zdm': 'N_XB',
              'c_target_dzdm': '11400000', 'c_source_dzdm': '10100003', 'c_target_jtmz': '0', 'c_source_jtmz': '255',
              'c_sheet_mc': '审判组织成员人民陪审员-spzzcy', 'c_ms': 'spzzcy', 'c_target_bm': 'T_SPZZCY_RMPSY',
              'c_target_sjlx': 'varchar', 'c_source_bm': 'T_YWGY_RMPSY', 'c_system_type': 'np', 'c_group': 'spzzcy',
              'lx': 'Single'},
             {'c_target_ywlx': 'all', 'c_source_ywlx': 'all', 'c_target_zdm': 'C_XB', 'c_source_zdm': 'N_XB',
              'c_target_dzdm': '11400000', 'c_source_dzdm': '10100003', 'c_target_jtmz': '0', 'c_source_jtmz': '0',
              'c_sheet_mc': '审判组织成员人民陪审员-spzzcy', 'c_ms': 'spzzcy', 'c_target_bm': 'T_SPZZCY_RMPSY',
              'c_target_sjlx': 'varchar', 'c_source_bm': 'T_YWGY_RMPSY', 'c_system_type': 'np', 'c_group': 'spzzcy',
              'lx': 'Single'}], [
             {'c_target_ywlx': 'all', 'c_source_ywlx': 'all', 'c_target_zdm': 'C_XB', 'c_source_zdm': 'N_XB',
              'c_target_dzdm': '11400000', 'c_source_dzdm': '10100003', 'c_target_jtmz': '1', 'c_source_jtmz': '1',
              'c_sheet_mc': '审判组织成员人民陪审员-spzzcy', 'c_ms': 'spzzcy', 'c_target_bm': 'T_SPZZCY_RMPSY',
              'c_target_sjlx': 'varchar', 'c_source_bm': 'T_YWGY_RMPSY', 'c_system_type': 'np', 'c_group': 'spzzcy',
              'lx': 'Single'},
             {'c_target_ywlx': 'all', 'c_source_ywlx': 'all', 'c_target_zdm': 'C_XB', 'c_source_zdm': 'N_XB',
              'c_target_dzdm': '11400000', 'c_source_dzdm': '10100003', 'c_target_jtmz': '2', 'c_source_jtmz': '2',
              'c_sheet_mc': '审判组织成员人民陪审员-spzzcy', 'c_ms': 'spzzcy', 'c_target_bm': 'T_SPZZCY_RMPSY',
              'c_target_sjlx': 'varchar', 'c_source_bm': 'T_YWGY_RMPSY', 'c_system_type': 'np', 'c_group': 'spzzcy',
              'lx': 'Single'},
             {'c_target_ywlx': 'all', 'c_source_ywlx': 'all', 'c_target_zdm': 'C_XB', 'c_source_zdm': 'N_XB',
              'c_target_dzdm': '11400000', 'c_source_dzdm': '10100003', 'c_target_jtmz': '9', 'c_source_jtmz': None,
              'c_sheet_mc': '审判组织成员人民陪审员-spzzcy', 'c_ms': 'spzzcy', 'c_target_bm': 'T_SPZZCY_RMPSY',
              'c_target_sjlx': 'varchar', 'c_source_bm': 'T_YWGY_RMPSY', 'c_system_type': 'np', 'c_group': 'spzzcy',
              'lx': 'Single'},
             {'c_target_ywlx': 'all', 'c_source_ywlx': 'all', 'c_target_zdm': 'C_XB', 'c_source_zdm': 'N_XB',
              'c_target_dzdm': '11400000', 'c_source_dzdm': '10100003', 'c_target_jtmz': '0', 'c_source_jtmz': '255',
              'c_sheet_mc': '审判组织成员人民陪审员-spzzcy', 'c_ms': 'spzzcy', 'c_target_bm': 'T_SPZZCY_RMPSY',
              'c_target_sjlx': 'varchar', 'c_source_bm': 'T_YWGY_RMPSY', 'c_system_type': 'np', 'c_group': 'spzzcy',
              'lx': 'Single'},
             {'c_target_ywlx': 'all', 'c_source_ywlx': 'all', 'c_target_zdm': 'C_XB', 'c_source_zdm': 'N_XB',
              'c_target_dzdm': '11400000', 'c_source_dzdm': '10100003', 'c_target_jtmz': '0', 'c_source_jtmz': '0',
              'c_sheet_mc': '审判组织成员人民陪审员-spzzcy', 'c_ms': 'spzzcy', 'c_target_bm': 'T_SPZZCY_RMPSY',
              'c_target_sjlx': 'varchar', 'c_source_bm': 'T_YWGY_RMPSY', 'c_system_type': 'np', 'c_group': 'spzzcy',
              'lx': 'Single'}], [
             {'c_target_ywlx': 'all', 'c_source_ywlx': 'all', 'c_target_zdm': 'C_XB', 'c_source_zdm': 'N_XB',
              'c_target_dzdm': '11400000', 'c_source_dzdm': '10100003', 'c_target_jtmz': '1', 'c_source_jtmz': '1',
              'c_sheet_mc': '审判组织成员人民陪审员-spzzcy', 'c_ms': 'spzzcy', 'c_target_bm': 'T_SPZZCY_RMPSY',
              'c_target_sjlx': 'varchar', 'c_source_bm': 'T_YWGY_RMPSY', 'c_system_type': 'np', 'c_group': 'spzzcy',
              'lx': 'Single'},
             {'c_target_ywlx': 'all', 'c_source_ywlx': 'all', 'c_target_zdm': 'C_XB', 'c_source_zdm': 'N_XB',
              'c_target_dzdm': '11400000', 'c_source_dzdm': '10100003', 'c_target_jtmz': '2', 'c_source_jtmz': '2',
              'c_sheet_mc': '审判组织成员人民陪审员-spzzcy', 'c_ms': 'spzzcy', 'c_target_bm': 'T_SPZZCY_RMPSY',
              'c_target_sjlx': 'varchar', 'c_source_bm': 'T_YWGY_RMPSY', 'c_system_type': 'np', 'c_group': 'spzzcy',
              'lx': 'Single'},
             {'c_target_ywlx': 'all', 'c_source_ywlx': 'all', 'c_target_zdm': 'C_XB', 'c_source_zdm': 'N_XB',
              'c_target_dzdm': '11400000', 'c_source_dzdm': '10100003', 'c_target_jtmz': '9', 'c_source_jtmz': None,
              'c_sheet_mc': '审判组织成员人民陪审员-spzzcy', 'c_ms': 'spzzcy', 'c_target_bm': 'T_SPZZCY_RMPSY',
              'c_target_sjlx': 'varchar', 'c_source_bm': 'T_YWGY_RMPSY', 'c_system_type': 'np', 'c_group': 'spzzcy',
              'lx': 'Single'},
             {'c_target_ywlx': 'all', 'c_source_ywlx': 'all', 'c_target_zdm': 'C_XB', 'c_source_zdm': 'N_XB',
              'c_target_dzdm': '11400000', 'c_source_dzdm': '10100003', 'c_target_jtmz': '0', 'c_source_jtmz': '255',
              'c_sheet_mc': '审判组织成员人民陪审员-spzzcy', 'c_ms': 'spzzcy', 'c_target_bm': 'T_SPZZCY_RMPSY',
              'c_target_sjlx': 'varchar', 'c_source_bm': 'T_YWGY_RMPSY', 'c_system_type': 'np', 'c_group': 'spzzcy',
              'lx': 'Single'},
             {'c_target_ywlx': 'all', 'c_source_ywlx': 'all', 'c_target_zdm': 'C_XB', 'c_source_zdm': 'N_XB',
              'c_target_dzdm': '11400000', 'c_source_dzdm': '10100003', 'c_target_jtmz': '0', 'c_source_jtmz': '0',
              'c_sheet_mc': '审判组织成员人民陪审员-spzzcy', 'c_ms': 'spzzcy', 'c_target_bm': 'T_SPZZCY_RMPSY',
              'c_target_sjlx': 'varchar', 'c_source_bm': 'T_YWGY_RMPSY', 'c_system_type': 'np', 'c_group': 'spzzcy',
              'lx': 'Single'}], [
             {'c_target_ywlx': 'all', 'c_source_ywlx': 'all', 'c_target_zdm': 'C_XB', 'c_source_zdm': 'N_XB',
              'c_target_dzdm': '11400000', 'c_source_dzdm': '10100003', 'c_target_jtmz': '1', 'c_source_jtmz': '1',
              'c_sheet_mc': '审判组织成员人民陪审员-spzzcy', 'c_ms': 'spzzcy', 'c_target_bm': 'T_SPZZCY_RMPSY',
              'c_target_sjlx': 'varchar', 'c_source_bm': 'T_YWGY_RMPSY', 'c_system_type': 'np', 'c_group': 'spzzcy',
              'lx': 'Single'},
             {'c_target_ywlx': 'all', 'c_source_ywlx': 'all', 'c_target_zdm': 'C_XB', 'c_source_zdm': 'N_XB',
              'c_target_dzdm': '11400000', 'c_source_dzdm': '10100003', 'c_target_jtmz': '2', 'c_source_jtmz': '2',
              'c_sheet_mc': '审判组织成员人民陪审员-spzzcy', 'c_ms': 'spzzcy', 'c_target_bm': 'T_SPZZCY_RMPSY',
              'c_target_sjlx': 'varchar', 'c_source_bm': 'T_YWGY_RMPSY', 'c_system_type': 'np', 'c_group': 'spzzcy',
              'lx': 'Single'},
             {'c_target_ywlx': 'all', 'c_source_ywlx': 'all', 'c_target_zdm': 'C_XB', 'c_source_zdm': 'N_XB',
              'c_target_dzdm': '11400000', 'c_source_dzdm': '10100003', 'c_target_jtmz': '9', 'c_source_jtmz': None,
              'c_sheet_mc': '审判组织成员人民陪审员-spzzcy', 'c_ms': 'spzzcy', 'c_target_bm': 'T_SPZZCY_RMPSY',
              'c_target_sjlx': 'varchar', 'c_source_bm': 'T_YWGY_RMPSY', 'c_system_type': 'np', 'c_group': 'spzzcy',
              'lx': 'Single'},
             {'c_target_ywlx': 'all', 'c_source_ywlx': 'all', 'c_target_zdm': 'C_XB', 'c_source_zdm': 'N_XB',
              'c_target_dzdm': '11400000', 'c_source_dzdm': '10100003', 'c_target_jtmz': '0', 'c_source_jtmz': '255',
              'c_sheet_mc': '审判组织成员人民陪审员-spzzcy', 'c_ms': 'spzzcy', 'c_target_bm': 'T_SPZZCY_RMPSY',
              'c_target_sjlx': 'varchar', 'c_source_bm': 'T_YWGY_RMPSY', 'c_system_type': 'np', 'c_group': 'spzzcy',
              'lx': 'Single'},
             {'c_target_ywlx': 'all', 'c_source_ywlx': 'all', 'c_target_zdm': 'C_XB', 'c_source_zdm': 'N_XB',
              'c_target_dzdm': '11400000', 'c_source_dzdm': '10100003', 'c_target_jtmz': '0', 'c_source_jtmz': '0',
              'c_sheet_mc': '审判组织成员人民陪审员-spzzcy', 'c_ms': 'spzzcy', 'c_target_bm': 'T_SPZZCY_RMPSY',
              'c_target_sjlx': 'varchar', 'c_source_bm': 'T_YWGY_RMPSY', 'c_system_type': 'np', 'c_group': 'spzzcy',
              'lx': 'Single'}], [
             {'c_target_ywlx': 'all', 'c_source_ywlx': 'all', 'c_target_zdm': 'C_XB', 'c_source_zdm': 'N_XB',
              'c_target_dzdm': '11400000', 'c_source_dzdm': '10100003', 'c_target_jtmz': '1', 'c_source_jtmz': '1',
              'c_sheet_mc': '审判组织成员人民陪审员-spzzcy', 'c_ms': 'spzzcy', 'c_target_bm': 'T_SPZZCY_RMPSY',
              'c_target_sjlx': 'varchar', 'c_source_bm': 'T_YWGY_RMPSY', 'c_system_type': 'np', 'c_group': 'spzzcy',
              'lx': 'Single'},
             {'c_target_ywlx': 'all', 'c_source_ywlx': 'all', 'c_target_zdm': 'C_XB', 'c_source_zdm': 'N_XB',
              'c_target_dzdm': '11400000', 'c_source_dzdm': '10100003', 'c_target_jtmz': '2', 'c_source_jtmz': '2',
              'c_sheet_mc': '审判组织成员人民陪审员-spzzcy', 'c_ms': 'spzzcy', 'c_target_bm': 'T_SPZZCY_RMPSY',
              'c_target_sjlx': 'varchar', 'c_source_bm': 'T_YWGY_RMPSY', 'c_system_type': 'np', 'c_group': 'spzzcy',
              'lx': 'Single'},
             {'c_target_ywlx': 'all', 'c_source_ywlx': 'all', 'c_target_zdm': 'C_XB', 'c_source_zdm': 'N_XB',
              'c_target_dzdm': '11400000', 'c_source_dzdm': '10100003', 'c_target_jtmz': '9', 'c_source_jtmz': None,
              'c_sheet_mc': '审判组织成员人民陪审员-spzzcy', 'c_ms': 'spzzcy', 'c_target_bm': 'T_SPZZCY_RMPSY',
              'c_target_sjlx': 'varchar', 'c_source_bm': 'T_YWGY_RMPSY', 'c_system_type': 'np', 'c_group': 'spzzcy',
              'lx': 'Single'},
             {'c_target_ywlx': 'all', 'c_source_ywlx': 'all', 'c_target_zdm': 'C_XB', 'c_source_zdm': 'N_XB',
              'c_target_dzdm': '11400000', 'c_source_dzdm': '10100003', 'c_target_jtmz': '0', 'c_source_jtmz': '255',
              'c_sheet_mc': '审判组织成员人民陪审员-spzzcy', 'c_ms': 'spzzcy', 'c_target_bm': 'T_SPZZCY_RMPSY',
              'c_target_sjlx': 'varchar', 'c_source_bm': 'T_YWGY_RMPSY', 'c_system_type': 'np', 'c_group': 'spzzcy',
              'lx': 'Single'},
             {'c_target_ywlx': 'all', 'c_source_ywlx': 'all', 'c_target_zdm': 'C_XB', 'c_source_zdm': 'N_XB',
              'c_target_dzdm': '11400000', 'c_source_dzdm': '10100003', 'c_target_jtmz': '0', 'c_source_jtmz': '0',
              'c_sheet_mc': '审判组织成员人民陪审员-spzzcy', 'c_ms': 'spzzcy', 'c_target_bm': 'T_SPZZCY_RMPSY',
              'c_target_sjlx': 'varchar', 'c_source_bm': 'T_YWGY_RMPSY', 'c_system_type': 'np', 'c_group': 'spzzcy',
              'lx': 'Single'}], [
             {'c_target_ywlx': 'all', 'c_source_ywlx': 'all', 'c_target_zdm': 'C_XB', 'c_source_zdm': 'N_XB',
              'c_target_dzdm': '11400000', 'c_source_dzdm': '10100003', 'c_target_jtmz': '1', 'c_source_jtmz': '1',
              'c_sheet_mc': '审判组织成员人民陪审员-spzzcy', 'c_ms': 'spzzcy', 'c_target_bm': 'T_SPZZCY_RMPSY',
              'c_target_sjlx': 'varchar', 'c_source_bm': 'T_YWGY_RMPSY', 'c_system_type': 'np', 'c_group': 'spzzcy',
              'lx': 'Single'},
             {'c_target_ywlx': 'all', 'c_source_ywlx': 'all', 'c_target_zdm': 'C_XB', 'c_source_zdm': 'N_XB',
              'c_target_dzdm': '11400000', 'c_source_dzdm': '10100003', 'c_target_jtmz': '2', 'c_source_jtmz': '2',
              'c_sheet_mc': '审判组织成员人民陪审员-spzzcy', 'c_ms': 'spzzcy', 'c_target_bm': 'T_SPZZCY_RMPSY',
              'c_target_sjlx': 'varchar', 'c_source_bm': 'T_YWGY_RMPSY', 'c_system_type': 'np', 'c_group': 'spzzcy',
              'lx': 'Single'},
             {'c_target_ywlx': 'all', 'c_source_ywlx': 'all', 'c_target_zdm': 'C_XB', 'c_source_zdm': 'N_XB',
              'c_target_dzdm': '11400000', 'c_source_dzdm': '10100003', 'c_target_jtmz': '9', 'c_source_jtmz': None,
              'c_sheet_mc': '审判组织成员人民陪审员-spzzcy', 'c_ms': 'spzzcy', 'c_target_bm': 'T_SPZZCY_RMPSY',
              'c_target_sjlx': 'varchar', 'c_source_bm': 'T_YWGY_RMPSY', 'c_system_type': 'np', 'c_group': 'spzzcy',
              'lx': 'Single'},
             {'c_target_ywlx': 'all', 'c_source_ywlx': 'all', 'c_target_zdm': 'C_XB', 'c_source_zdm': 'N_XB',
              'c_target_dzdm': '11400000', 'c_source_dzdm': '10100003', 'c_target_jtmz': '0', 'c_source_jtmz': '255',
              'c_sheet_mc': '审判组织成员人民陪审员-spzzcy', 'c_ms': 'spzzcy', 'c_target_bm': 'T_SPZZCY_RMPSY',
              'c_target_sjlx': 'varchar', 'c_source_bm': 'T_YWGY_RMPSY', 'c_system_type': 'np', 'c_group': 'spzzcy',
              'lx': 'Single'},
             {'c_target_ywlx': 'all', 'c_source_ywlx': 'all', 'c_target_zdm': 'C_XB', 'c_source_zdm': 'N_XB',
              'c_target_dzdm': '11400000', 'c_source_dzdm': '10100003', 'c_target_jtmz': '0', 'c_source_jtmz': '0',
              'c_sheet_mc': '审判组织成员人民陪审员-spzzcy', 'c_ms': 'spzzcy', 'c_target_bm': 'T_SPZZCY_RMPSY',
              'c_target_sjlx': 'varchar', 'c_source_bm': 'T_YWGY_RMPSY', 'c_system_type': 'np', 'c_group': 'spzzcy',
              'lx': 'Single'}], [
             {'c_target_ywlx': 'all', 'c_source_ywlx': 'all', 'c_target_zdm': 'C_XB', 'c_source_zdm': 'N_XB',
              'c_target_dzdm': '11400000', 'c_source_dzdm': '10100003', 'c_target_jtmz': '1', 'c_source_jtmz': '1',
              'c_sheet_mc': '审判组织成员人民陪审员-spzzcy', 'c_ms': 'spzzcy', 'c_target_bm': 'T_SPZZCY_RMPSY',
              'c_target_sjlx': 'varchar', 'c_source_bm': 'T_YWGY_RMPSY', 'c_system_type': 'np', 'c_group': 'spzzcy',
              'lx': 'Single'},
             {'c_target_ywlx': 'all', 'c_source_ywlx': 'all', 'c_target_zdm': 'C_XB', 'c_source_zdm': 'N_XB',
              'c_target_dzdm': '11400000', 'c_source_dzdm': '10100003', 'c_target_jtmz': '2', 'c_source_jtmz': '2',
              'c_sheet_mc': '审判组织成员人民陪审员-spzzcy', 'c_ms': 'spzzcy', 'c_target_bm': 'T_SPZZCY_RMPSY',
              'c_target_sjlx': 'varchar', 'c_source_bm': 'T_YWGY_RMPSY', 'c_system_type': 'np', 'c_group': 'spzzcy',
              'lx': 'Single'},
             {'c_target_ywlx': 'all', 'c_source_ywlx': 'all', 'c_target_zdm': 'C_XB', 'c_source_zdm': 'N_XB',
              'c_target_dzdm': '11400000', 'c_source_dzdm': '10100003', 'c_target_jtmz': '9', 'c_source_jtmz': None,
              'c_sheet_mc': '审判组织成员人民陪审员-spzzcy', 'c_ms': 'spzzcy', 'c_target_bm': 'T_SPZZCY_RMPSY',
              'c_target_sjlx': 'varchar', 'c_source_bm': 'T_YWGY_RMPSY', 'c_system_type': 'np', 'c_group': 'spzzcy',
              'lx': 'Single'},
             {'c_target_ywlx': 'all', 'c_source_ywlx': 'all', 'c_target_zdm': 'C_XB', 'c_source_zdm': 'N_XB',
              'c_target_dzdm': '11400000', 'c_source_dzdm': '10100003', 'c_target_jtmz': '0', 'c_source_jtmz': '255',
              'c_sheet_mc': '审判组织成员人民陪审员-spzzcy', 'c_ms': 'spzzcy', 'c_target_bm': 'T_SPZZCY_RMPSY',
              'c_target_sjlx': 'varchar', 'c_source_bm': 'T_YWGY_RMPSY', 'c_system_type': 'np', 'c_group': 'spzzcy',
              'lx': 'Single'},
             {'c_target_ywlx': 'all', 'c_source_ywlx': 'all', 'c_target_zdm': 'C_XB', 'c_source_zdm': 'N_XB',
              'c_target_dzdm': '11400000', 'c_source_dzdm': '10100003', 'c_target_jtmz': '0', 'c_source_jtmz': '0',
              'c_sheet_mc': '审判组织成员人民陪审员-spzzcy', 'c_ms': 'spzzcy', 'c_target_bm': 'T_SPZZCY_RMPSY',
              'c_target_sjlx': 'varchar', 'c_source_bm': 'T_YWGY_RMPSY', 'c_system_type': 'np', 'c_group': 'spzzcy',
              'lx': 'Single'}], [
             {'c_target_ywlx': 'all', 'c_source_ywlx': 'all', 'c_target_zdm': 'C_XB', 'c_source_zdm': 'N_XB',
              'c_target_dzdm': '11400000', 'c_source_dzdm': '10100003', 'c_target_jtmz': '1', 'c_source_jtmz': '1',
              'c_sheet_mc': '审判组织成员人民陪审员-spzzcy', 'c_ms': 'spzzcy', 'c_target_bm': 'T_SPZZCY_RMPSY',
              'c_target_sjlx': 'varchar', 'c_source_bm': 'T_YWGY_RMPSY', 'c_system_type': 'np', 'c_group': 'spzzcy',
              'lx': 'Single'},
             {'c_target_ywlx': 'all', 'c_source_ywlx': 'all', 'c_target_zdm': 'C_XB', 'c_source_zdm': 'N_XB',
              'c_target_dzdm': '11400000', 'c_source_dzdm': '10100003', 'c_target_jtmz': '2', 'c_source_jtmz': '2',
              'c_sheet_mc': '审判组织成员人民陪审员-spzzcy', 'c_ms': 'spzzcy', 'c_target_bm': 'T_SPZZCY_RMPSY',
              'c_target_sjlx': 'varchar', 'c_source_bm': 'T_YWGY_RMPSY', 'c_system_type': 'np', 'c_group': 'spzzcy',
              'lx': 'Single'},
             {'c_target_ywlx': 'all', 'c_source_ywlx': 'all', 'c_target_zdm': 'C_XB', 'c_source_zdm': 'N_XB',
              'c_target_dzdm': '11400000', 'c_source_dzdm': '10100003', 'c_target_jtmz': '9', 'c_source_jtmz': None,
              'c_sheet_mc': '审判组织成员人民陪审员-spzzcy', 'c_ms': 'spzzcy', 'c_target_bm': 'T_SPZZCY_RMPSY',
              'c_target_sjlx': 'varchar', 'c_source_bm': 'T_YWGY_RMPSY', 'c_system_type': 'np', 'c_group': 'spzzcy',
              'lx': 'Single'},
             {'c_target_ywlx': 'all', 'c_source_ywlx': 'all', 'c_target_zdm': 'C_XB', 'c_source_zdm': 'N_XB',
              'c_target_dzdm': '11400000', 'c_source_dzdm': '10100003', 'c_target_jtmz': '0', 'c_source_jtmz': '255',
              'c_sheet_mc': '审判组织成员人民陪审员-spzzcy', 'c_ms': 'spzzcy', 'c_target_bm': 'T_SPZZCY_RMPSY',
              'c_target_sjlx': 'varchar', 'c_source_bm': 'T_YWGY_RMPSY', 'c_system_type': 'np', 'c_group': 'spzzcy',
              'lx': 'Single'},
             {'c_target_ywlx': 'all', 'c_source_ywlx': 'all', 'c_target_zdm': 'C_XB', 'c_source_zdm': 'N_XB',
              'c_target_dzdm': '11400000', 'c_source_dzdm': '10100003', 'c_target_jtmz': '0', 'c_source_jtmz': '0',
              'c_sheet_mc': '审判组织成员人民陪审员-spzzcy', 'c_ms': 'spzzcy', 'c_target_bm': 'T_SPZZCY_RMPSY',
              'c_target_sjlx': 'varchar', 'c_source_bm': 'T_YWGY_RMPSY', 'c_system_type': 'np', 'c_group': 'spzzcy',
              'lx': 'Single'}], [
             {'c_target_ywlx': 'all', 'c_source_ywlx': 'all', 'c_target_zdm': 'C_XB', 'c_source_zdm': 'N_XB',
              'c_target_dzdm': '11400000', 'c_source_dzdm': '10100003', 'c_target_jtmz': '1', 'c_source_jtmz': '1',
              'c_sheet_mc': '审判组织成员人民陪审员-spzzcy', 'c_ms': 'spzzcy', 'c_target_bm': 'T_SPZZCY_RMPSY',
              'c_target_sjlx': 'varchar', 'c_source_bm': 'T_YWGY_RMPSY', 'c_system_type': 'np', 'c_group': 'spzzcy',
              'lx': 'Single'},
             {'c_target_ywlx': 'all', 'c_source_ywlx': 'all', 'c_target_zdm': 'C_XB', 'c_source_zdm': 'N_XB',
              'c_target_dzdm': '11400000', 'c_source_dzdm': '10100003', 'c_target_jtmz': '2', 'c_source_jtmz': '2',
              'c_sheet_mc': '审判组织成员人民陪审员-spzzcy', 'c_ms': 'spzzcy', 'c_target_bm': 'T_SPZZCY_RMPSY',
              'c_target_sjlx': 'varchar', 'c_source_bm': 'T_YWGY_RMPSY', 'c_system_type': 'np', 'c_group': 'spzzcy',
              'lx': 'Single'},
             {'c_target_ywlx': 'all', 'c_source_ywlx': 'all', 'c_target_zdm': 'C_XB', 'c_source_zdm': 'N_XB',
              'c_target_dzdm': '11400000', 'c_source_dzdm': '10100003', 'c_target_jtmz': '9', 'c_source_jtmz': None,
              'c_sheet_mc': '审判组织成员人民陪审员-spzzcy', 'c_ms': 'spzzcy', 'c_target_bm': 'T_SPZZCY_RMPSY',
              'c_target_sjlx': 'varchar', 'c_source_bm': 'T_YWGY_RMPSY', 'c_system_type': 'np', 'c_group': 'spzzcy',
              'lx': 'Single'},
             {'c_target_ywlx': 'all', 'c_source_ywlx': 'all', 'c_target_zdm': 'C_XB', 'c_source_zdm': 'N_XB',
              'c_target_dzdm': '11400000', 'c_source_dzdm': '10100003', 'c_target_jtmz': '0', 'c_source_jtmz': '255',
              'c_sheet_mc': '审判组织成员人民陪审员-spzzcy', 'c_ms': 'spzzcy', 'c_target_bm': 'T_SPZZCY_RMPSY',
              'c_target_sjlx': 'varchar', 'c_source_bm': 'T_YWGY_RMPSY', 'c_system_type': 'np', 'c_group': 'spzzcy',
              'lx': 'Single'},
             {'c_target_ywlx': 'all', 'c_source_ywlx': 'all', 'c_target_zdm': 'C_XB', 'c_source_zdm': 'N_XB',
              'c_target_dzdm': '11400000', 'c_source_dzdm': '10100003', 'c_target_jtmz': '0', 'c_source_jtmz': '0',
              'c_sheet_mc': '审判组织成员人民陪审员-spzzcy', 'c_ms': 'spzzcy', 'c_target_bm': 'T_SPZZCY_RMPSY',
              'c_target_sjlx': 'varchar', 'c_source_bm': 'T_YWGY_RMPSY', 'c_system_type': 'np', 'c_group': 'spzzcy',
              'lx': 'Single'}], [
             {'c_target_ywlx': 'all', 'c_source_ywlx': 'all', 'c_target_zdm': 'C_XB', 'c_source_zdm': 'N_XB',
              'c_target_dzdm': '11400000', 'c_source_dzdm': '10100003', 'c_target_jtmz': '1', 'c_source_jtmz': '1',
              'c_sheet_mc': '审判组织成员人民陪审员-spzzcy', 'c_ms': 'spzzcy', 'c_target_bm': 'T_SPZZCY_RMPSY',
              'c_target_sjlx': 'varchar', 'c_source_bm': 'T_YWGY_RMPSY', 'c_system_type': 'np', 'c_group': 'spzzcy',
              'lx': 'Single'},
             {'c_target_ywlx': 'all', 'c_source_ywlx': 'all', 'c_target_zdm': 'C_XB', 'c_source_zdm': 'N_XB',
              'c_target_dzdm': '11400000', 'c_source_dzdm': '10100003', 'c_target_jtmz': '2', 'c_source_jtmz': '2',
              'c_sheet_mc': '审判组织成员人民陪审员-spzzcy', 'c_ms': 'spzzcy', 'c_target_bm': 'T_SPZZCY_RMPSY',
              'c_target_sjlx': 'varchar', 'c_source_bm': 'T_YWGY_RMPSY', 'c_system_type': 'np', 'c_group': 'spzzcy',
              'lx': 'Single'},
             {'c_target_ywlx': 'all', 'c_source_ywlx': 'all', 'c_target_zdm': 'C_XB', 'c_source_zdm': 'N_XB',
              'c_target_dzdm': '11400000', 'c_source_dzdm': '10100003', 'c_target_jtmz': '9', 'c_source_jtmz': None,
              'c_sheet_mc': '审判组织成员人民陪审员-spzzcy', 'c_ms': 'spzzcy', 'c_target_bm': 'T_SPZZCY_RMPSY',
              'c_target_sjlx': 'varchar', 'c_source_bm': 'T_YWGY_RMPSY', 'c_system_type': 'np', 'c_group': 'spzzcy',
              'lx': 'Single'},
             {'c_target_ywlx': 'all', 'c_source_ywlx': 'all', 'c_target_zdm': 'C_XB', 'c_source_zdm': 'N_XB',
              'c_target_dzdm': '11400000', 'c_source_dzdm': '10100003', 'c_target_jtmz': '0', 'c_source_jtmz': '255',
              'c_sheet_mc': '审判组织成员人民陪审员-spzzcy', 'c_ms': 'spzzcy', 'c_target_bm': 'T_SPZZCY_RMPSY',
              'c_target_sjlx': 'varchar', 'c_source_bm': 'T_YWGY_RMPSY', 'c_system_type': 'np', 'c_group': 'spzzcy',
              'lx': 'Single'},
             {'c_target_ywlx': 'all', 'c_source_ywlx': 'all', 'c_target_zdm': 'C_XB', 'c_source_zdm': 'N_XB',
              'c_target_dzdm': '11400000', 'c_source_dzdm': '10100003', 'c_target_jtmz': '0', 'c_source_jtmz': '0',
              'c_sheet_mc': '审判组织成员人民陪审员-spzzcy', 'c_ms': 'spzzcy', 'c_target_bm': 'T_SPZZCY_RMPSY',
              'c_target_sjlx': 'varchar', 'c_source_bm': 'T_YWGY_RMPSY', 'c_system_type': 'np', 'c_group': 'spzzcy',
              'lx': 'Single'}], [
             {'c_target_ywlx': 'all', 'c_source_ywlx': 'all', 'c_target_zdm': 'C_XB', 'c_source_zdm': 'N_XB',
              'c_target_dzdm': '11400000', 'c_source_dzdm': '10100003', 'c_target_jtmz': '1', 'c_source_jtmz': '1',
              'c_sheet_mc': '审判组织成员人民陪审员-spzzcy', 'c_ms': 'spzzcy', 'c_target_bm': 'T_SPZZCY_RMPSY',
              'c_target_sjlx': 'varchar', 'c_source_bm': 'T_YWGY_RMPSY', 'c_system_type': 'np', 'c_group': 'spzzcy',
              'lx': 'Single'},
             {'c_target_ywlx': 'all', 'c_source_ywlx': 'all', 'c_target_zdm': 'C_XB', 'c_source_zdm': 'N_XB',
              'c_target_dzdm': '11400000', 'c_source_dzdm': '10100003', 'c_target_jtmz': '2', 'c_source_jtmz': '2',
              'c_sheet_mc': '审判组织成员人民陪审员-spzzcy', 'c_ms': 'spzzcy', 'c_target_bm': 'T_SPZZCY_RMPSY',
              'c_target_sjlx': 'varchar', 'c_source_bm': 'T_YWGY_RMPSY', 'c_system_type': 'np', 'c_group': 'spzzcy',
              'lx': 'Single'},
             {'c_target_ywlx': 'all', 'c_source_ywlx': 'all', 'c_target_zdm': 'C_XB', 'c_source_zdm': 'N_XB',
              'c_target_dzdm': '11400000', 'c_source_dzdm': '10100003', 'c_target_jtmz': '9', 'c_source_jtmz': None,
              'c_sheet_mc': '审判组织成员人民陪审员-spzzcy', 'c_ms': 'spzzcy', 'c_target_bm': 'T_SPZZCY_RMPSY',
              'c_target_sjlx': 'varchar', 'c_source_bm': 'T_YWGY_RMPSY', 'c_system_type': 'np', 'c_group': 'spzzcy',
              'lx': 'Single'},
             {'c_target_ywlx': 'all', 'c_source_ywlx': 'all', 'c_target_zdm': 'C_XB', 'c_source_zdm': 'N_XB',
              'c_target_dzdm': '11400000', 'c_source_dzdm': '10100003', 'c_target_jtmz': '0', 'c_source_jtmz': '255',
              'c_sheet_mc': '审判组织成员人民陪审员-spzzcy', 'c_ms': 'spzzcy', 'c_target_bm': 'T_SPZZCY_RMPSY',
              'c_target_sjlx': 'varchar', 'c_source_bm': 'T_YWGY_RMPSY', 'c_system_type': 'np', 'c_group': 'spzzcy',
              'lx': 'Single'},
             {'c_target_ywlx': 'all', 'c_source_ywlx': 'all', 'c_target_zdm': 'C_XB', 'c_source_zdm': 'N_XB',
              'c_target_dzdm': '11400000', 'c_source_dzdm': '10100003', 'c_target_jtmz': '0', 'c_source_jtmz': '0',
              'c_sheet_mc': '审判组织成员人民陪审员-spzzcy', 'c_ms': 'spzzcy', 'c_target_bm': 'T_SPZZCY_RMPSY',
              'c_target_sjlx': 'varchar', 'c_source_bm': 'T_YWGY_RMPSY', 'c_system_type': 'np', 'c_group': 'spzzcy',
              'lx': 'Single'}], [
             {'c_target_ywlx': 'all', 'c_source_ywlx': 'all', 'c_target_zdm': 'C_XB', 'c_source_zdm': 'N_XB',
              'c_target_dzdm': '11400000', 'c_source_dzdm': '10100003', 'c_target_jtmz': '1', 'c_source_jtmz': '1',
              'c_sheet_mc': '审判组织成员人民陪审员-spzzcy', 'c_ms': 'spzzcy', 'c_target_bm': 'T_SPZZCY_RMPSY',
              'c_target_sjlx': 'varchar', 'c_source_bm': 'T_YWGY_RMPSY', 'c_system_type': 'np', 'c_group': 'spzzcy',
              'lx': 'Single'},
             {'c_target_ywlx': 'all', 'c_source_ywlx': 'all', 'c_target_zdm': 'C_XB', 'c_source_zdm': 'N_XB',
              'c_target_dzdm': '11400000', 'c_source_dzdm': '10100003', 'c_target_jtmz': '2', 'c_source_jtmz': '2',
              'c_sheet_mc': '审判组织成员人民陪审员-spzzcy', 'c_ms': 'spzzcy', 'c_target_bm': 'T_SPZZCY_RMPSY',
              'c_target_sjlx': 'varchar', 'c_source_bm': 'T_YWGY_RMPSY', 'c_system_type': 'np', 'c_group': 'spzzcy',
              'lx': 'Single'},
             {'c_target_ywlx': 'all', 'c_source_ywlx': 'all', 'c_target_zdm': 'C_XB', 'c_source_zdm': 'N_XB',
              'c_target_dzdm': '11400000', 'c_source_dzdm': '10100003', 'c_target_jtmz': '9', 'c_source_jtmz': None,
              'c_sheet_mc': '审判组织成员人民陪审员-spzzcy', 'c_ms': 'spzzcy', 'c_target_bm': 'T_SPZZCY_RMPSY',
              'c_target_sjlx': 'varchar', 'c_source_bm': 'T_YWGY_RMPSY', 'c_system_type': 'np', 'c_group': 'spzzcy',
              'lx': 'Single'},
             {'c_target_ywlx': 'all', 'c_source_ywlx': 'all', 'c_target_zdm': 'C_XB', 'c_source_zdm': 'N_XB',
              'c_target_dzdm': '11400000', 'c_source_dzdm': '10100003', 'c_target_jtmz': '0', 'c_source_jtmz': '255',
              'c_sheet_mc': '审判组织成员人民陪审员-spzzcy', 'c_ms': 'spzzcy', 'c_target_bm': 'T_SPZZCY_RMPSY',
              'c_target_sjlx': 'varchar', 'c_source_bm': 'T_YWGY_RMPSY', 'c_system_type': 'np', 'c_group': 'spzzcy',
              'lx': 'Single'},
             {'c_target_ywlx': 'all', 'c_source_ywlx': 'all', 'c_target_zdm': 'C_XB', 'c_source_zdm': 'N_XB',
              'c_target_dzdm': '11400000', 'c_source_dzdm': '10100003', 'c_target_jtmz': '0', 'c_source_jtmz': '0',
              'c_sheet_mc': '审判组织成员人民陪审员-spzzcy', 'c_ms': 'spzzcy', 'c_target_bm': 'T_SPZZCY_RMPSY',
              'c_target_sjlx': 'varchar', 'c_source_bm': 'T_YWGY_RMPSY', 'c_system_type': 'np', 'c_group': 'spzzcy',
              'lx': 'Single'}], [
             {'c_target_ywlx': 'all', 'c_source_ywlx': 'all', 'c_target_zdm': 'C_XB', 'c_source_zdm': 'N_XB',
              'c_target_dzdm': '11400000', 'c_source_dzdm': '10100003', 'c_target_jtmz': '1', 'c_source_jtmz': '1',
              'c_sheet_mc': '审判组织成员人民陪审员-spzzcy', 'c_ms': 'spzzcy', 'c_target_bm': 'T_SPZZCY_RMPSY',
              'c_target_sjlx': 'varchar', 'c_source_bm': 'T_YWGY_RMPSY', 'c_system_type': 'np', 'c_group': 'spzzcy',
              'lx': 'Single'},
             {'c_target_ywlx': 'all', 'c_source_ywlx': 'all', 'c_target_zdm': 'C_XB', 'c_source_zdm': 'N_XB',
              'c_target_dzdm': '11400000', 'c_source_dzdm': '10100003', 'c_target_jtmz': '2', 'c_source_jtmz': '2',
              'c_sheet_mc': '审判组织成员人民陪审员-spzzcy', 'c_ms': 'spzzcy', 'c_target_bm': 'T_SPZZCY_RMPSY',
              'c_target_sjlx': 'varchar', 'c_source_bm': 'T_YWGY_RMPSY', 'c_system_type': 'np', 'c_group': 'spzzcy',
              'lx': 'Single'},
             {'c_target_ywlx': 'all', 'c_source_ywlx': 'all', 'c_target_zdm': 'C_XB', 'c_source_zdm': 'N_XB',
              'c_target_dzdm': '11400000', 'c_source_dzdm': '10100003', 'c_target_jtmz': '9', 'c_source_jtmz': None,
              'c_sheet_mc': '审判组织成员人民陪审员-spzzcy', 'c_ms': 'spzzcy', 'c_target_bm': 'T_SPZZCY_RMPSY',
              'c_target_sjlx': 'varchar', 'c_source_bm': 'T_YWGY_RMPSY', 'c_system_type': 'np', 'c_group': 'spzzcy',
              'lx': 'Single'},
             {'c_target_ywlx': 'all', 'c_source_ywlx': 'all', 'c_target_zdm': 'C_XB', 'c_source_zdm': 'N_XB',
              'c_target_dzdm': '11400000', 'c_source_dzdm': '10100003', 'c_target_jtmz': '0', 'c_source_jtmz': '255',
              'c_sheet_mc': '审判组织成员人民陪审员-spzzcy', 'c_ms': 'spzzcy', 'c_target_bm': 'T_SPZZCY_RMPSY',
              'c_target_sjlx': 'varchar', 'c_source_bm': 'T_YWGY_RMPSY', 'c_system_type': 'np', 'c_group': 'spzzcy',
              'lx': 'Single'},
             {'c_target_ywlx': 'all', 'c_source_ywlx': 'all', 'c_target_zdm': 'C_XB', 'c_source_zdm': 'N_XB',
              'c_target_dzdm': '11400000', 'c_source_dzdm': '10100003', 'c_target_jtmz': '0', 'c_source_jtmz': '0',
              'c_sheet_mc': '审判组织成员人民陪审员-spzzcy', 'c_ms': 'spzzcy', 'c_target_bm': 'T_SPZZCY_RMPSY',
              'c_target_sjlx': 'varchar', 'c_source_bm': 'T_YWGY_RMPSY', 'c_system_type': 'np', 'c_group': 'spzzcy',
              'lx': 'Single'}], [
             {'c_target_ywlx': 'all', 'c_source_ywlx': 'all', 'c_target_zdm': 'C_XB', 'c_source_zdm': 'N_XB',
              'c_target_dzdm': '11400000', 'c_source_dzdm': '10100003', 'c_target_jtmz': '1', 'c_source_jtmz': '1',
              'c_sheet_mc': '审判组织成员人民陪审员-spzzcy', 'c_ms': 'spzzcy', 'c_target_bm': 'T_SPZZCY_RMPSY',
              'c_target_sjlx': 'varchar', 'c_source_bm': 'T_YWGY_RMPSY', 'c_system_type': 'np', 'c_group': 'spzzcy',
              'lx': 'Single'},
             {'c_target_ywlx': 'all', 'c_source_ywlx': 'all', 'c_target_zdm': 'C_XB', 'c_source_zdm': 'N_XB',
              'c_target_dzdm': '11400000', 'c_source_dzdm': '10100003', 'c_target_jtmz': '2', 'c_source_jtmz': '2',
              'c_sheet_mc': '审判组织成员人民陪审员-spzzcy', 'c_ms': 'spzzcy', 'c_target_bm': 'T_SPZZCY_RMPSY',
              'c_target_sjlx': 'varchar', 'c_source_bm': 'T_YWGY_RMPSY', 'c_system_type': 'np', 'c_group': 'spzzcy',
              'lx': 'Single'},
             {'c_target_ywlx': 'all', 'c_source_ywlx': 'all', 'c_target_zdm': 'C_XB', 'c_source_zdm': 'N_XB',
              'c_target_dzdm': '11400000', 'c_source_dzdm': '10100003', 'c_target_jtmz': '9', 'c_source_jtmz': None,
              'c_sheet_mc': '审判组织成员人民陪审员-spzzcy', 'c_ms': 'spzzcy', 'c_target_bm': 'T_SPZZCY_RMPSY',
              'c_target_sjlx': 'varchar', 'c_source_bm': 'T_YWGY_RMPSY', 'c_system_type': 'np', 'c_group': 'spzzcy',
              'lx': 'Single'},
             {'c_target_ywlx': 'all', 'c_source_ywlx': 'all', 'c_target_zdm': 'C_XB', 'c_source_zdm': 'N_XB',
              'c_target_dzdm': '11400000', 'c_source_dzdm': '10100003', 'c_target_jtmz': '0', 'c_source_jtmz': '255',
              'c_sheet_mc': '审判组织成员人民陪审员-spzzcy', 'c_ms': 'spzzcy', 'c_target_bm': 'T_SPZZCY_RMPSY',
              'c_target_sjlx': 'varchar', 'c_source_bm': 'T_YWGY_RMPSY', 'c_system_type': 'np', 'c_group': 'spzzcy',
              'lx': 'Single'},
             {'c_target_ywlx': 'all', 'c_source_ywlx': 'all', 'c_target_zdm': 'C_XB', 'c_source_zdm': 'N_XB',
              'c_target_dzdm': '11400000', 'c_source_dzdm': '10100003', 'c_target_jtmz': '0', 'c_source_jtmz': '0',
              'c_sheet_mc': '审判组织成员人民陪审员-spzzcy', 'c_ms': 'spzzcy', 'c_target_bm': 'T_SPZZCY_RMPSY',
              'c_target_sjlx': 'varchar', 'c_source_bm': 'T_YWGY_RMPSY', 'c_system_type': 'np', 'c_group': 'spzzcy',
              'lx': 'Single'}], [
             {'c_target_ywlx': 'all', 'c_source_ywlx': 'all', 'c_target_zdm': 'C_XB', 'c_source_zdm': 'N_XB',
              'c_target_dzdm': '11400000', 'c_source_dzdm': '10100003', 'c_target_jtmz': '1', 'c_source_jtmz': '1',
              'c_sheet_mc': '审判组织成员人民陪审员-spzzcy', 'c_ms': 'spzzcy', 'c_target_bm': 'T_SPZZCY_RMPSY',
              'c_target_sjlx': 'varchar', 'c_source_bm': 'T_YWGY_RMPSY', 'c_system_type': 'np', 'c_group': 'spzzcy',
              'lx': 'Single'},
             {'c_target_ywlx': 'all', 'c_source_ywlx': 'all', 'c_target_zdm': 'C_XB', 'c_source_zdm': 'N_XB',
              'c_target_dzdm': '11400000', 'c_source_dzdm': '10100003', 'c_target_jtmz': '2', 'c_source_jtmz': '2',
              'c_sheet_mc': '审判组织成员人民陪审员-spzzcy', 'c_ms': 'spzzcy', 'c_target_bm': 'T_SPZZCY_RMPSY',
              'c_target_sjlx': 'varchar', 'c_source_bm': 'T_YWGY_RMPSY', 'c_system_type': 'np', 'c_group': 'spzzcy',
              'lx': 'Single'},
             {'c_target_ywlx': 'all', 'c_source_ywlx': 'all', 'c_target_zdm': 'C_XB', 'c_source_zdm': 'N_XB',
              'c_target_dzdm': '11400000', 'c_source_dzdm': '10100003', 'c_target_jtmz': '9', 'c_source_jtmz': None,
              'c_sheet_mc': '审判组织成员人民陪审员-spzzcy', 'c_ms': 'spzzcy', 'c_target_bm': 'T_SPZZCY_RMPSY',
              'c_target_sjlx': 'varchar', 'c_source_bm': 'T_YWGY_RMPSY', 'c_system_type': 'np', 'c_group': 'spzzcy',
              'lx': 'Single'},
             {'c_target_ywlx': 'all', 'c_source_ywlx': 'all', 'c_target_zdm': 'C_XB', 'c_source_zdm': 'N_XB',
              'c_target_dzdm': '11400000', 'c_source_dzdm': '10100003', 'c_target_jtmz': '0', 'c_source_jtmz': '255',
              'c_sheet_mc': '审判组织成员人民陪审员-spzzcy', 'c_ms': 'spzzcy', 'c_target_bm': 'T_SPZZCY_RMPSY',
              'c_target_sjlx': 'varchar', 'c_source_bm': 'T_YWGY_RMPSY', 'c_system_type': 'np', 'c_group': 'spzzcy',
              'lx': 'Single'},
             {'c_target_ywlx': 'all', 'c_source_ywlx': 'all', 'c_target_zdm': 'C_XB', 'c_source_zdm': 'N_XB',
              'c_target_dzdm': '11400000', 'c_source_dzdm': '10100003', 'c_target_jtmz': '0', 'c_source_jtmz': '0',
              'c_sheet_mc': '审判组织成员人民陪审员-spzzcy', 'c_ms': 'spzzcy', 'c_target_bm': 'T_SPZZCY_RMPSY',
              'c_target_sjlx': 'varchar', 'c_source_bm': 'T_YWGY_RMPSY', 'c_system_type': 'np', 'c_group': 'spzzcy',
              'lx': 'Single'}], [
             {'c_target_ywlx': 'all', 'c_source_ywlx': 'all', 'c_target_zdm': 'C_XB', 'c_source_zdm': 'N_XB',
              'c_target_dzdm': '11400000', 'c_source_dzdm': '10100003', 'c_target_jtmz': '1', 'c_source_jtmz': '1',
              'c_sheet_mc': '审判组织成员人民陪审员-spzzcy', 'c_ms': 'spzzcy', 'c_target_bm': 'T_SPZZCY_RMPSY',
              'c_target_sjlx': 'varchar', 'c_source_bm': 'T_YWGY_RMPSY', 'c_system_type': 'np', 'c_group': 'spzzcy',
              'lx': 'Single'},
             {'c_target_ywlx': 'all', 'c_source_ywlx': 'all', 'c_target_zdm': 'C_XB', 'c_source_zdm': 'N_XB',
              'c_target_dzdm': '11400000', 'c_source_dzdm': '10100003', 'c_target_jtmz': '2', 'c_source_jtmz': '2',
              'c_sheet_mc': '审判组织成员人民陪审员-spzzcy', 'c_ms': 'spzzcy', 'c_target_bm': 'T_SPZZCY_RMPSY',
              'c_target_sjlx': 'varchar', 'c_source_bm': 'T_YWGY_RMPSY', 'c_system_type': 'np', 'c_group': 'spzzcy',
              'lx': 'Single'},
             {'c_target_ywlx': 'all', 'c_source_ywlx': 'all', 'c_target_zdm': 'C_XB', 'c_source_zdm': 'N_XB',
              'c_target_dzdm': '11400000', 'c_source_dzdm': '10100003', 'c_target_jtmz': '9', 'c_source_jtmz': None,
              'c_sheet_mc': '审判组织成员人民陪审员-spzzcy', 'c_ms': 'spzzcy', 'c_target_bm': 'T_SPZZCY_RMPSY',
              'c_target_sjlx': 'varchar', 'c_source_bm': 'T_YWGY_RMPSY', 'c_system_type': 'np', 'c_group': 'spzzcy',
              'lx': 'Single'},
             {'c_target_ywlx': 'all', 'c_source_ywlx': 'all', 'c_target_zdm': 'C_XB', 'c_source_zdm': 'N_XB',
              'c_target_dzdm': '11400000', 'c_source_dzdm': '10100003', 'c_target_jtmz': '0', 'c_source_jtmz': '255',
              'c_sheet_mc': '审判组织成员人民陪审员-spzzcy', 'c_ms': 'spzzcy', 'c_target_bm': 'T_SPZZCY_RMPSY',
              'c_target_sjlx': 'varchar', 'c_source_bm': 'T_YWGY_RMPSY', 'c_system_type': 'np', 'c_group': 'spzzcy',
              'lx': 'Single'},
             {'c_target_ywlx': 'all', 'c_source_ywlx': 'all', 'c_target_zdm': 'C_XB', 'c_source_zdm': 'N_XB',
              'c_target_dzdm': '11400000', 'c_source_dzdm': '10100003', 'c_target_jtmz': '0', 'c_source_jtmz': '0',
              'c_sheet_mc': '审判组织成员人民陪审员-spzzcy', 'c_ms': 'spzzcy', 'c_target_bm': 'T_SPZZCY_RMPSY',
              'c_target_sjlx': 'varchar', 'c_source_bm': 'T_YWGY_RMPSY', 'c_system_type': 'np', 'c_group': 'spzzcy',
              'lx': 'Single'}], [
             {'c_target_ywlx': 'all', 'c_source_ywlx': 'all', 'c_target_zdm': 'C_XB', 'c_source_zdm': 'N_XB',
              'c_target_dzdm': '11400000', 'c_source_dzdm': '10100003', 'c_target_jtmz': '1', 'c_source_jtmz': '1',
              'c_sheet_mc': '审判组织成员人民陪审员-spzzcy', 'c_ms': 'spzzcy', 'c_target_bm': 'T_SPZZCY_RMPSY',
              'c_target_sjlx': 'varchar', 'c_source_bm': 'T_YWGY_RMPSY', 'c_system_type': 'np', 'c_group': 'spzzcy',
              'lx': 'Single'},
             {'c_target_ywlx': 'all', 'c_source_ywlx': 'all', 'c_target_zdm': 'C_XB', 'c_source_zdm': 'N_XB',
              'c_target_dzdm': '11400000', 'c_source_dzdm': '10100003', 'c_target_jtmz': '2', 'c_source_jtmz': '2',
              'c_sheet_mc': '审判组织成员人民陪审员-spzzcy', 'c_ms': 'spzzcy', 'c_target_bm': 'T_SPZZCY_RMPSY',
              'c_target_sjlx': 'varchar', 'c_source_bm': 'T_YWGY_RMPSY', 'c_system_type': 'np', 'c_group': 'spzzcy',
              'lx': 'Single'},
             {'c_target_ywlx': 'all', 'c_source_ywlx': 'all', 'c_target_zdm': 'C_XB', 'c_source_zdm': 'N_XB',
              'c_target_dzdm': '11400000', 'c_source_dzdm': '10100003', 'c_target_jtmz': '9', 'c_source_jtmz': None,
              'c_sheet_mc': '审判组织成员人民陪审员-spzzcy', 'c_ms': 'spzzcy', 'c_target_bm': 'T_SPZZCY_RMPSY',
              'c_target_sjlx': 'varchar', 'c_source_bm': 'T_YWGY_RMPSY', 'c_system_type': 'np', 'c_group': 'spzzcy',
              'lx': 'Single'},
             {'c_target_ywlx': 'all', 'c_source_ywlx': 'all', 'c_target_zdm': 'C_XB', 'c_source_zdm': 'N_XB',
              'c_target_dzdm': '11400000', 'c_source_dzdm': '10100003', 'c_target_jtmz': '0', 'c_source_jtmz': '255',
              'c_sheet_mc': '审判组织成员人民陪审员-spzzcy', 'c_ms': 'spzzcy', 'c_target_bm': 'T_SPZZCY_RMPSY',
              'c_target_sjlx': 'varchar', 'c_source_bm': 'T_YWGY_RMPSY', 'c_system_type': 'np', 'c_group': 'spzzcy',
              'lx': 'Single'},
             {'c_target_ywlx': 'all', 'c_source_ywlx': 'all', 'c_target_zdm': 'C_XB', 'c_source_zdm': 'N_XB',
              'c_target_dzdm': '11400000', 'c_source_dzdm': '10100003', 'c_target_jtmz': '0', 'c_source_jtmz': '0',
              'c_sheet_mc': '审判组织成员人民陪审员-spzzcy', 'c_ms': 'spzzcy', 'c_target_bm': 'T_SPZZCY_RMPSY',
              'c_target_sjlx': 'varchar', 'c_source_bm': 'T_YWGY_RMPSY', 'c_system_type': 'np', 'c_group': 'spzzcy',
              'lx': 'Single'}], [
             {'c_target_ywlx': 'all', 'c_source_ywlx': 'all', 'c_target_zdm': 'C_XB', 'c_source_zdm': 'N_XB',
              'c_target_dzdm': '11400000', 'c_source_dzdm': '10100003', 'c_target_jtmz': '1', 'c_source_jtmz': '1',
              'c_sheet_mc': '审判组织成员人民陪审员-spzzcy', 'c_ms': 'spzzcy', 'c_target_bm': 'T_SPZZCY_RMPSY',
              'c_target_sjlx': 'varchar', 'c_source_bm': 'T_YWGY_RMPSY', 'c_system_type': 'np', 'c_group': 'spzzcy',
              'lx': 'Single'},
             {'c_target_ywlx': 'all', 'c_source_ywlx': 'all', 'c_target_zdm': 'C_XB', 'c_source_zdm': 'N_XB',
              'c_target_dzdm': '11400000', 'c_source_dzdm': '10100003', 'c_target_jtmz': '2', 'c_source_jtmz': '2',
              'c_sheet_mc': '审判组织成员人民陪审员-spzzcy', 'c_ms': 'spzzcy', 'c_target_bm': 'T_SPZZCY_RMPSY',
              'c_target_sjlx': 'varchar', 'c_source_bm': 'T_YWGY_RMPSY', 'c_system_type': 'np', 'c_group': 'spzzcy',
              'lx': 'Single'},
             {'c_target_ywlx': 'all', 'c_source_ywlx': 'all', 'c_target_zdm': 'C_XB', 'c_source_zdm': 'N_XB',
              'c_target_dzdm': '11400000', 'c_source_dzdm': '10100003', 'c_target_jtmz': '9', 'c_source_jtmz': None,
              'c_sheet_mc': '审判组织成员人民陪审员-spzzcy', 'c_ms': 'spzzcy', 'c_target_bm': 'T_SPZZCY_RMPSY',
              'c_target_sjlx': 'varchar', 'c_source_bm': 'T_YWGY_RMPSY', 'c_system_type': 'np', 'c_group': 'spzzcy',
              'lx': 'Single'},
             {'c_target_ywlx': 'all', 'c_source_ywlx': 'all', 'c_target_zdm': 'C_XB', 'c_source_zdm': 'N_XB',
              'c_target_dzdm': '11400000', 'c_source_dzdm': '10100003', 'c_target_jtmz': '0', 'c_source_jtmz': '255',
              'c_sheet_mc': '审判组织成员人民陪审员-spzzcy', 'c_ms': 'spzzcy', 'c_target_bm': 'T_SPZZCY_RMPSY',
              'c_target_sjlx': 'varchar', 'c_source_bm': 'T_YWGY_RMPSY', 'c_system_type': 'np', 'c_group': 'spzzcy',
              'lx': 'Single'},
             {'c_target_ywlx': 'all', 'c_source_ywlx': 'all', 'c_target_zdm': 'C_XB', 'c_source_zdm': 'N_XB',
              'c_target_dzdm': '11400000', 'c_source_dzdm': '10100003', 'c_target_jtmz': '0', 'c_source_jtmz': '0',
              'c_sheet_mc': '审判组织成员人民陪审员-spzzcy', 'c_ms': 'spzzcy', 'c_target_bm': 'T_SPZZCY_RMPSY',
              'c_target_sjlx': 'varchar', 'c_source_bm': 'T_YWGY_RMPSY', 'c_system_type': 'np', 'c_group': 'spzzcy',
              'lx': 'Single'}], [
             {'c_target_ywlx': 'all', 'c_source_ywlx': 'all', 'c_target_zdm': 'C_XB', 'c_source_zdm': 'N_XB',
              'c_target_dzdm': '11400000', 'c_source_dzdm': '10100003', 'c_target_jtmz': '1', 'c_source_jtmz': '1',
              'c_sheet_mc': '审判组织成员人民陪审员-spzzcy', 'c_ms': 'spzzcy', 'c_target_bm': 'T_SPZZCY_RMPSY',
              'c_target_sjlx': 'varchar', 'c_source_bm': 'T_YWGY_RMPSY', 'c_system_type': 'np', 'c_group': 'spzzcy',
              'lx': 'Single'},
             {'c_target_ywlx': 'all', 'c_source_ywlx': 'all', 'c_target_zdm': 'C_XB', 'c_source_zdm': 'N_XB',
              'c_target_dzdm': '11400000', 'c_source_dzdm': '10100003', 'c_target_jtmz': '2', 'c_source_jtmz': '2',
              'c_sheet_mc': '审判组织成员人民陪审员-spzzcy', 'c_ms': 'spzzcy', 'c_target_bm': 'T_SPZZCY_RMPSY',
              'c_target_sjlx': 'varchar', 'c_source_bm': 'T_YWGY_RMPSY', 'c_system_type': 'np', 'c_group': 'spzzcy',
              'lx': 'Single'},
             {'c_target_ywlx': 'all', 'c_source_ywlx': 'all', 'c_target_zdm': 'C_XB', 'c_source_zdm': 'N_XB',
              'c_target_dzdm': '11400000', 'c_source_dzdm': '10100003', 'c_target_jtmz': '9', 'c_source_jtmz': None,
              'c_sheet_mc': '审判组织成员人民陪审员-spzzcy', 'c_ms': 'spzzcy', 'c_target_bm': 'T_SPZZCY_RMPSY',
              'c_target_sjlx': 'varchar', 'c_source_bm': 'T_YWGY_RMPSY', 'c_system_type': 'np', 'c_group': 'spzzcy',
              'lx': 'Single'},
             {'c_target_ywlx': 'all', 'c_source_ywlx': 'all', 'c_target_zdm': 'C_XB', 'c_source_zdm': 'N_XB',
              'c_target_dzdm': '11400000', 'c_source_dzdm': '10100003', 'c_target_jtmz': '0', 'c_source_jtmz': '255',
              'c_sheet_mc': '审判组织成员人民陪审员-spzzcy', 'c_ms': 'spzzcy', 'c_target_bm': 'T_SPZZCY_RMPSY',
              'c_target_sjlx': 'varchar', 'c_source_bm': 'T_YWGY_RMPSY', 'c_system_type': 'np', 'c_group': 'spzzcy',
              'lx': 'Single'},
             {'c_target_ywlx': 'all', 'c_source_ywlx': 'all', 'c_target_zdm': 'C_XB', 'c_source_zdm': 'N_XB',
              'c_target_dzdm': '11400000', 'c_source_dzdm': '10100003', 'c_target_jtmz': '0', 'c_source_jtmz': '0',
              'c_sheet_mc': '审判组织成员人民陪审员-spzzcy', 'c_ms': 'spzzcy', 'c_target_bm': 'T_SPZZCY_RMPSY',
              'c_target_sjlx': 'varchar', 'c_source_bm': 'T_YWGY_RMPSY', 'c_system_type': 'np', 'c_group': 'spzzcy',
              'lx': 'Single'}], [
             {'c_target_ywlx': 'all', 'c_source_ywlx': 'all', 'c_target_zdm': 'C_XB', 'c_source_zdm': 'N_XB',
              'c_target_dzdm': '11400000', 'c_source_dzdm': '10100003', 'c_target_jtmz': '1', 'c_source_jtmz': '1',
              'c_sheet_mc': '审判组织成员人民陪审员-spzzcy', 'c_ms': 'spzzcy', 'c_target_bm': 'T_SPZZCY_RMPSY',
              'c_target_sjlx': 'varchar', 'c_source_bm': 'T_YWGY_RMPSY', 'c_system_type': 'np', 'c_group': 'spzzcy',
              'lx': 'Single'},
             {'c_target_ywlx': 'all', 'c_source_ywlx': 'all', 'c_target_zdm': 'C_XB', 'c_source_zdm': 'N_XB',
              'c_target_dzdm': '11400000', 'c_source_dzdm': '10100003', 'c_target_jtmz': '2', 'c_source_jtmz': '2',
              'c_sheet_mc': '审判组织成员人民陪审员-spzzcy', 'c_ms': 'spzzcy', 'c_target_bm': 'T_SPZZCY_RMPSY',
              'c_target_sjlx': 'varchar', 'c_source_bm': 'T_YWGY_RMPSY', 'c_system_type': 'np', 'c_group': 'spzzcy',
              'lx': 'Single'},
             {'c_target_ywlx': 'all', 'c_source_ywlx': 'all', 'c_target_zdm': 'C_XB', 'c_source_zdm': 'N_XB',
              'c_target_dzdm': '11400000', 'c_source_dzdm': '10100003', 'c_target_jtmz': '9', 'c_source_jtmz': None,
              'c_sheet_mc': '审判组织成员人民陪审员-spzzcy', 'c_ms': 'spzzcy', 'c_target_bm': 'T_SPZZCY_RMPSY',
              'c_target_sjlx': 'varchar', 'c_source_bm': 'T_YWGY_RMPSY', 'c_system_type': 'np', 'c_group': 'spzzcy',
              'lx': 'Single'},
             {'c_target_ywlx': 'all', 'c_source_ywlx': 'all', 'c_target_zdm': 'C_XB', 'c_source_zdm': 'N_XB',
              'c_target_dzdm': '11400000', 'c_source_dzdm': '10100003', 'c_target_jtmz': '0', 'c_source_jtmz': '255',
              'c_sheet_mc': '审判组织成员人民陪审员-spzzcy', 'c_ms': 'spzzcy', 'c_target_bm': 'T_SPZZCY_RMPSY',
              'c_target_sjlx': 'varchar', 'c_source_bm': 'T_YWGY_RMPSY', 'c_system_type': 'np', 'c_group': 'spzzcy',
              'lx': 'Single'},
             {'c_target_ywlx': 'all', 'c_source_ywlx': 'all', 'c_target_zdm': 'C_XB', 'c_source_zdm': 'N_XB',
              'c_target_dzdm': '11400000', 'c_source_dzdm': '10100003', 'c_target_jtmz': '0', 'c_source_jtmz': '0',
              'c_sheet_mc': '审判组织成员人民陪审员-spzzcy', 'c_ms': 'spzzcy', 'c_target_bm': 'T_SPZZCY_RMPSY',
              'c_target_sjlx': 'varchar', 'c_source_bm': 'T_YWGY_RMPSY', 'c_system_type': 'np', 'c_group': 'spzzcy',
              'lx': 'Single'}], [
             {'c_target_ywlx': 'all', 'c_source_ywlx': 'all', 'c_target_zdm': 'C_XB', 'c_source_zdm': 'N_XB',
              'c_target_dzdm': '11400000', 'c_source_dzdm': '10100003', 'c_target_jtmz': '1', 'c_source_jtmz': '1',
              'c_sheet_mc': '审判组织成员人民陪审员-spzzcy', 'c_ms': 'spzzcy', 'c_target_bm': 'T_SPZZCY_RMPSY',
              'c_target_sjlx': 'varchar', 'c_source_bm': 'T_YWGY_RMPSY', 'c_system_type': 'np', 'c_group': 'spzzcy',
              'lx': 'Single'},
             {'c_target_ywlx': 'all', 'c_source_ywlx': 'all', 'c_target_zdm': 'C_XB', 'c_source_zdm': 'N_XB',
              'c_target_dzdm': '11400000', 'c_source_dzdm': '10100003', 'c_target_jtmz': '2', 'c_source_jtmz': '2',
              'c_sheet_mc': '审判组织成员人民陪审员-spzzcy', 'c_ms': 'spzzcy', 'c_target_bm': 'T_SPZZCY_RMPSY',
              'c_target_sjlx': 'varchar', 'c_source_bm': 'T_YWGY_RMPSY', 'c_system_type': 'np', 'c_group': 'spzzcy',
              'lx': 'Single'},
             {'c_target_ywlx': 'all', 'c_source_ywlx': 'all', 'c_target_zdm': 'C_XB', 'c_source_zdm': 'N_XB',
              'c_target_dzdm': '11400000', 'c_source_dzdm': '10100003', 'c_target_jtmz': '9', 'c_source_jtmz': None,
              'c_sheet_mc': '审判组织成员人民陪审员-spzzcy', 'c_ms': 'spzzcy', 'c_target_bm': 'T_SPZZCY_RMPSY',
              'c_target_sjlx': 'varchar', 'c_source_bm': 'T_YWGY_RMPSY', 'c_system_type': 'np', 'c_group': 'spzzcy',
              'lx': 'Single'},
             {'c_target_ywlx': 'all', 'c_source_ywlx': 'all', 'c_target_zdm': 'C_XB', 'c_source_zdm': 'N_XB',
              'c_target_dzdm': '11400000', 'c_source_dzdm': '10100003', 'c_target_jtmz': '0', 'c_source_jtmz': '255',
              'c_sheet_mc': '审判组织成员人民陪审员-spzzcy', 'c_ms': 'spzzcy', 'c_target_bm': 'T_SPZZCY_RMPSY',
              'c_target_sjlx': 'varchar', 'c_source_bm': 'T_YWGY_RMPSY', 'c_system_type': 'np', 'c_group': 'spzzcy',
              'lx': 'Single'},
             {'c_target_ywlx': 'all', 'c_source_ywlx': 'all', 'c_target_zdm': 'C_XB', 'c_source_zdm': 'N_XB',
              'c_target_dzdm': '11400000', 'c_source_dzdm': '10100003', 'c_target_jtmz': '0', 'c_source_jtmz': '0',
              'c_sheet_mc': '审判组织成员人民陪审员-spzzcy', 'c_ms': 'spzzcy', 'c_target_bm': 'T_SPZZCY_RMPSY',
              'c_target_sjlx': 'varchar', 'c_source_bm': 'T_YWGY_RMPSY', 'c_system_type': 'np', 'c_group': 'spzzcy',
              'lx': 'Single'}], [
             {'c_target_ywlx': 'all', 'c_source_ywlx': 'all', 'c_target_zdm': 'C_XB', 'c_source_zdm': 'N_XB',
              'c_target_dzdm': '11400000', 'c_source_dzdm': '10100003', 'c_target_jtmz': '1', 'c_source_jtmz': '1',
              'c_sheet_mc': '审判组织成员人民陪审员-spzzcy', 'c_ms': 'spzzcy', 'c_target_bm': 'T_SPZZCY_RMPSY',
              'c_target_sjlx': 'varchar', 'c_source_bm': 'T_YWGY_RMPSY', 'c_system_type': 'np', 'c_group': 'spzzcy',
              'lx': 'Single'},
             {'c_target_ywlx': 'all', 'c_source_ywlx': 'all', 'c_target_zdm': 'C_XB', 'c_source_zdm': 'N_XB',
              'c_target_dzdm': '11400000', 'c_source_dzdm': '10100003', 'c_target_jtmz': '2', 'c_source_jtmz': '2',
              'c_sheet_mc': '审判组织成员人民陪审员-spzzcy', 'c_ms': 'spzzcy', 'c_target_bm': 'T_SPZZCY_RMPSY',
              'c_target_sjlx': 'varchar', 'c_source_bm': 'T_YWGY_RMPSY', 'c_system_type': 'np', 'c_group': 'spzzcy',
              'lx': 'Single'},
             {'c_target_ywlx': 'all', 'c_source_ywlx': 'all', 'c_target_zdm': 'C_XB', 'c_source_zdm': 'N_XB',
              'c_target_dzdm': '11400000', 'c_source_dzdm': '10100003', 'c_target_jtmz': '9', 'c_source_jtmz': None,
              'c_sheet_mc': '审判组织成员人民陪审员-spzzcy', 'c_ms': 'spzzcy', 'c_target_bm': 'T_SPZZCY_RMPSY',
              'c_target_sjlx': 'varchar', 'c_source_bm': 'T_YWGY_RMPSY', 'c_system_type': 'np', 'c_group': 'spzzcy',
              'lx': 'Single'},
             {'c_target_ywlx': 'all', 'c_source_ywlx': 'all', 'c_target_zdm': 'C_XB', 'c_source_zdm': 'N_XB',
              'c_target_dzdm': '11400000', 'c_source_dzdm': '10100003', 'c_target_jtmz': '0', 'c_source_jtmz': '255',
              'c_sheet_mc': '审判组织成员人民陪审员-spzzcy', 'c_ms': 'spzzcy', 'c_target_bm': 'T_SPZZCY_RMPSY',
              'c_target_sjlx': 'varchar', 'c_source_bm': 'T_YWGY_RMPSY', 'c_system_type': 'np', 'c_group': 'spzzcy',
              'lx': 'Single'},
             {'c_target_ywlx': 'all', 'c_source_ywlx': 'all', 'c_target_zdm': 'C_XB', 'c_source_zdm': 'N_XB',
              'c_target_dzdm': '11400000', 'c_source_dzdm': '10100003', 'c_target_jtmz': '0', 'c_source_jtmz': '0',
              'c_sheet_mc': '审判组织成员人民陪审员-spzzcy', 'c_ms': 'spzzcy', 'c_target_bm': 'T_SPZZCY_RMPSY',
              'c_target_sjlx': 'varchar', 'c_source_bm': 'T_YWGY_RMPSY', 'c_system_type': 'np', 'c_group': 'spzzcy',
              'lx': 'Single'}], [
             {'c_target_ywlx': 'all', 'c_source_ywlx': 'all', 'c_target_zdm': 'C_XB', 'c_source_zdm': 'N_XB',
              'c_target_dzdm': '11400000', 'c_source_dzdm': '10100003', 'c_target_jtmz': '1', 'c_source_jtmz': '1',
              'c_sheet_mc': '审判组织成员人民陪审员-spzzcy', 'c_ms': 'spzzcy', 'c_target_bm': 'T_SPZZCY_RMPSY',
              'c_target_sjlx': 'varchar', 'c_source_bm': 'T_YWGY_RMPSY', 'c_system_type': 'np', 'c_group': 'spzzcy',
              'lx': 'Single'},
             {'c_target_ywlx': 'all', 'c_source_ywlx': 'all', 'c_target_zdm': 'C_XB', 'c_source_zdm': 'N_XB',
              'c_target_dzdm': '11400000', 'c_source_dzdm': '10100003', 'c_target_jtmz': '2', 'c_source_jtmz': '2',
              'c_sheet_mc': '审判组织成员人民陪审员-spzzcy', 'c_ms': 'spzzcy', 'c_target_bm': 'T_SPZZCY_RMPSY',
              'c_target_sjlx': 'varchar', 'c_source_bm': 'T_YWGY_RMPSY', 'c_system_type': 'np', 'c_group': 'spzzcy',
              'lx': 'Single'},
             {'c_target_ywlx': 'all', 'c_source_ywlx': 'all', 'c_target_zdm': 'C_XB', 'c_source_zdm': 'N_XB',
              'c_target_dzdm': '11400000', 'c_source_dzdm': '10100003', 'c_target_jtmz': '9', 'c_source_jtmz': None,
              'c_sheet_mc': '审判组织成员人民陪审员-spzzcy', 'c_ms': 'spzzcy', 'c_target_bm': 'T_SPZZCY_RMPSY',
              'c_target_sjlx': 'varchar', 'c_source_bm': 'T_YWGY_RMPSY', 'c_system_type': 'np', 'c_group': 'spzzcy',
              'lx': 'Single'},
             {'c_target_ywlx': 'all', 'c_source_ywlx': 'all', 'c_target_zdm': 'C_XB', 'c_source_zdm': 'N_XB',
              'c_target_dzdm': '11400000', 'c_source_dzdm': '10100003', 'c_target_jtmz': '0', 'c_source_jtmz': '255',
              'c_sheet_mc': '审判组织成员人民陪审员-spzzcy', 'c_ms': 'spzzcy', 'c_target_bm': 'T_SPZZCY_RMPSY',
              'c_target_sjlx': 'varchar', 'c_source_bm': 'T_YWGY_RMPSY', 'c_system_type': 'np', 'c_group': 'spzzcy',
              'lx': 'Single'},
             {'c_target_ywlx': 'all', 'c_source_ywlx': 'all', 'c_target_zdm': 'C_XB', 'c_source_zdm': 'N_XB',
              'c_target_dzdm': '11400000', 'c_source_dzdm': '10100003', 'c_target_jtmz': '0', 'c_source_jtmz': '0',
              'c_sheet_mc': '审判组织成员人民陪审员-spzzcy', 'c_ms': 'spzzcy', 'c_target_bm': 'T_SPZZCY_RMPSY',
              'c_target_sjlx': 'varchar', 'c_source_bm': 'T_YWGY_RMPSY', 'c_system_type': 'np', 'c_group': 'spzzcy',
              'lx': 'Single'}]]

    a = {"targetDB": {
        "ip": "172.18.19.88",
        "port": "6543",
        "userid": "t3wh",
        "password": "t3wh@6789#JKL",
        "database": "DB_FY"
    },
        "sourceDB": {
            "ip": "172.18.17.186",
            "port": "5000",
            "userid": "sa",
            "password": "np@release",
            "database": "YWST",
            "schema": "dbo"
        }
    }
    b = "执行sql"
    c = GetSql(d, a, b)
    c.main()
