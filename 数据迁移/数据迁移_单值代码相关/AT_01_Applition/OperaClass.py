'''
操作类
'''
from AT_02_ExportOutInputData import ExportOutDataServer, ExportOutDataConstant
from AT_03_OperaDBServer import TargetDBServer, TargetDBConstant
from AT_00_SystemConstant import SystemConstant
from AT_04_DBDataProcess import ProcessServer
from AT_07_FilteringRules import FilterRulesServer
from AT_05_Stitch_SQL import SQLServer


class OperaClassApplication(object):
    DB_info = None
    Target = None
    Source = None

    def __int__(self):
        pass

    def main(self):
        OutData = ExportOutDataServer.ExportOutData(ExportOutDataConstant.Constant.DirName, ExportOutDataConstant.Constant.FileName)
        self.DB_info = OutData.export_main()
        if self.DB_info:
            Mark = TargetDBConstant.Constant
            TargetDB_single = TargetDBServer.TargetDB(self.DB_info[SystemConstant.targetDB], Mark.GetSingleAllSqlMC)
            single_xx = TargetDB_single.main()
            TargetDB_field = TargetDBServer.TargetDB(self.DB_info[SystemConstant.targetDB],Mark.GetFieldRelation)
            field_xx = TargetDB_field.main()
            field_filter_server = FilterRulesServer.FilterDataServer(field_xx)
            field_info = field_filter_server.main()
            # 需要过滤掉 field 是文书的字段
            HandleSingleValue = ProcessServer.HandleSingleValue(field_info, single_xx)
            Single = HandleSingleValue.main()
            # b = []
            # for i in Single:
            #     if len(i) > 1:
            #         if i[0]['c_group'] == "tj":
            #             b.append(i)
            # print(b)
            # exit()
            HandleMoreValue = ProcessServer.HandleMoreValue(field_info,single_xx)

            More = HandleMoreValue.main()
            a = []
            for i in More:
                if len(i)>1:
                    if i[0]['c_sheet_mc'] == '审判组织成员人民陪审员-spzzcy' and i[0]['c_target_zdm'] == 'C_XB' :
                        a.append(i)
            print(a)
            exit()



            SwitchSql = SQLServer.GetSql(More, self.DB_info, TargetDBConstant.Constant.ExecuteSqlMark)
            SwitchSql.main()
            # SourceDB = TargetDBServer.SourceDB(self.DB_info[SystemConstant.sourceDB])
            # SourceDB.main()




