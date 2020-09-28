""" 比较 SMD 和 SWagger的数据 """
import xlrd


class ExeclOpera(object):

    def __init__(self, filename,sheetname,title_row, start_rows):
        self.filename = filename
        self.sheetname = sheetname
        self.title_row = title_row
        self.start_row = start_rows

    def get_excel_info(self):
        bk = xlrd.open_workbook(self.filename)
        sh = bk.sheet_by_name(self.sheetname)
        row_num = sh.nrows
        data_list = []
        if sh.row_values(self.title_row)[0] == '':
            self.start_row += 1
            self.title_row += 1

        try:

            for i in range(self.start_row, row_num):
                row_data = sh.row_values(i)
                data = {}
                for index, key in enumerate(sh.row_values(self.title_row)):
                    data[key] = row_data[index]
                if data not in data_list:
                    data_list.append(data)
        except Exception as e:
            print("数据获取失败.，请小主检查对应文件配置...")
            print(e)
        print("数据获取完成...开始进行下一步,请小主喝杯咖啡继续等待......")
        return data_list
