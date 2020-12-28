# encoding: utf-8
import psycopg2, jaydebeapi
from AT_00_SystemConstant import SystemConstant
from AT_03_OperaDBServer import TargetDBConstant
from AT_09_CommonMethod import CommonMethodServer
from AT_06_ResultExport import SqlConstant

class ConnectDB(object):
    cur = None
    sql_result = []
    filter_rule = None
    sql = None
    conn = None
    FieldResultData = []

    def __init__(self, db_info, opera):
        self.Database = db_info[SystemConstant.DataBase]
        self.User = db_info[SystemConstant.User]
        self.Password = db_info[SystemConstant.Password]
        self.host = db_info[SystemConstant.IP]
        self.port = db_info[SystemConstant.Port]
        self.opera = opera

    def __getattr__(self, item):
        return SystemConstant.ClassErrorMessage


class TargetDB(ConnectDB):
    Constant = TargetDBConstant.Constant

    def main(self):
        if self.opera == TargetDBConstant.Constant.GetSingleAllSqlMC:
            self.sql = TargetDBConstant.Constant.GetSingleAllSql
            self.filter_rule = TargetDBConstant.Constant.GetSingleFieldList
        elif self.opera == TargetDBConstant.Constant.GetFieldRelation:
            self.sql = TargetDBConstant.Constant.GetFieldAllSql
            self.filter_rule = TargetDBConstant.Constant.GetFieldList

        else:
            pass
        if not self.cur:
            self.connect_target_db()
        if self.opera == TargetDBConstant.Constant.ExecuteSqlMark:
            self.execute_sql()
        elif self.opera == SqlConstant.SqlConstant.GetScopeOpera:
            self.execute_sql()
        elif self.opera is True:
            self.execute_sql()

        else:
            self.get_target_db_xx()
            return self.sql_result

    def connect_target_db(self):
        self.conn = psycopg2.connect(database=self.Database, user=self.User, password=self.Password, host=self.host,
                                port=self.port)
        self.cur = self.conn.cursor()

    def get_target_db_xx(self):
        self.sql_result = []
        self.execute_sql()
        rows = self.cur.fetchall()
        desc = self.cur.description
        for j in rows:
            data_list = [{desc[i][SystemConstant.Zero]: j[i]} for i in range(len(rows[SystemConstant.Zero]))]
            dict_list = CommonMethodServer.list_to_dict(data_list, self.filter_rule)
            self.sql_result.append(dict_list)
        if self.opera == TargetDBConstant.Constant.GetFieldRelation:
            # 获取单值代码字段
            self.sql_result = CommonMethodServer.list_filter_field_null(self.sql_result,
                                                                        self.Constant.filter_target_field,
                                                                        self.Constant.filter_source_field)


            self.get_np_field()

    def get_np_field(self):
        """
          过滤获取np的单值代码字段
        """
        if self.sql_result:
            for i in self.sql_result:
                # 有效的数据为 np数据 且 非ay
                if i[self.Constant.FieldSystemMark] == self.Constant.SystemMark:
                    self.FieldResultData.append(i)

    def execute_sql(self):
        self.cur.execute(self.sql)


class SourceDB(object):
    cur = None
    coon = None
    sql = None

    def __init__(self, db_info):
        self.User = db_info[SystemConstant.User]
        self.Password = db_info[SystemConstant.Password]
        self.Address = SystemConstant.PreSource + db_info[SystemConstant.IP] + SystemConstant.Semicolon + db_info[SystemConstant.Port] + \
                       SystemConstant.Slash + db_info[SystemConstant.DataBase]


    def main(self):

        if not self.cur:
            self.connect_source_db()
        self.ex_source_sql()
        pass

    def connect_source_db(self):
        try:

            self.conn = jaydebeapi.connect('com.sybase.jdbc3.jdbc.SybDriver', self.Address,
                                           [self.User, self.Password],
                                           'jconn-3.jar')
            self.cur = self.conn.cursor()

        except Exception as e:
            print(e)

    def ex_source_sql(self):
        self.cur.execute(self.sql)
        # rows = self.cur.fetchall()
        # desc = self.cur.description
        # print(rows[SystemConstant.Zero][SystemConstant.Zero])
        # print(desc[SystemConstant.Zero][SystemConstant.Zero])
        # self.cur.close()
        # self.conn.close()


if __name__ == '__main__':
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

    source = SourceDB(a['sourceDB'])
    source.main()
    pass
