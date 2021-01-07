import xlrd,logging,re

# -*- coding: utf-8 -*-

# @Project  : 内蒙openApi比对工具
# @File     : Check.py
# @Date     : 2020-12-31
# @Author   : Administrator
# @Info     :
# @Introduce:

def program_error(message,file_name,):

    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    fh = logging.FileHandler(file_name)
    fh.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(userid)s - %(message)s')
    fh.setFormatter(formatter)
    logger.addHandler(fh)

    logger.info(message,extra={'userid':"1"})


class ConstantClass(object):
    bh_log_file = 'E:/安装包/Test/数据库表/bh.txt'
    url_log_file = 'E:/安装包/Test/数据库表/url.txt'
    invoke_log_file = 'E:/安装包/Test/数据库表/invoke.txt'
    sheet_list = [
        "t_openapi_apixxdy",
        "t_openapi_apizcxx",
        "t_openapi_xxdy",
        "t_openapi_zcxx"
    ]
    BH = 'c_bh'
    source_filename = "E:/安装包/Test/数据库表/source.xlsx"
    target_filename = "E:/安装包/Test/数据库表/target.xlsx"
    ip_value = '133.4.4'
    Url = 'c_url'
    Server = 'c_yymc'
    InvokeMark = 'c_sfqy'

class ExeclOpera(object):

    def __init__(self, filename, sheetname, title_row, start_rows):
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


class GetData(object):

    def __init__(self):
        pass

    def main(self):
        source = self.get_data(ConstantClass.source_filename)
        target =  self.get_data(ConstantClass.target_filename)
        return source, target

    def get_data(self, filename):
        """

        """
        sheet_list = ConstantClass.sheet_list
        result = {}
        for sheet in sheet_list:
            try:
                Execl = ExeclOpera(filename,sheet, 0, 1)
                one_sheet = Execl.get_excel_info()
                result[sheet] = one_sheet

            except Exception as e:
                print(e)
        return result


class Compare(object):

    def __init__(self,source, target):
        self.source = source
        self.target = target

    def main(self):
        # bh_result = self.deal_bh()
        # if bh_result:
        #     program_error(bh_result,ConstantClass.bh_log_file)
        # url_result = self.deal_url()
        # if url_result:
        #     program_error(url_result,ConstantClass.url_log_file)
        invoke_result = self.deal_invoke()
        if invoke_result:
            program_error(invoke_result, ConstantClass.invoke_log_file)

    def get_except_data(self,key):
        if self.source and self.target:
            if key in self.target.keys():
                source_except_value = self.source[key]
                target_except_value = self.target[key]
                return source_except_value,target_except_value,target_except_value
        else:
            return None

    def deal_url(self):

        result = []
        except_data = self.get_except_data('t_openapi_zcxx')
        if except_data:
            target_data = except_data[1]
            for one_data in target_data:
                if ConstantClass.Url in one_data.keys():
                    url = one_data[ConstantClass.Url]
                    if url:
                        url_list = re.split('//|:',url)
                        if len(url_list)>=3:
                            if ConstantClass.ip_value in url_list[2]:
                                result.append(one_data[ConstantClass.Server])
        if result:
            return result

    def deal_bh(self):
        result = {}
        if self.source and self.target:
            for key in self.source:
                if key in self.target.keys():
                    source = self.source[key]
                    target = self.target[key]
                    source_bh_list = self.get_bh(source,ConstantClass.BH)
                    target_bh_list = self.get_bh(target,ConstantClass.BH)
                    one_result = self.compare_bh(source_bh_list, target_bh_list)
                    value_list = []
                    if one_result:
                        for j  in one_result:
                            for k in source:
                                if k[ConstantClass.BH] ==j:
                                    value_list.append(k)

                    result[key] = value_list

        return result

    def deal_invoke(self):
        result = []
        except_data = self.get_except_data('t_openapi_zcxx')
        if except_data:
            target_data = except_data[1]
            for one_data in target_data:
                if ConstantClass.InvokeMark in one_data.keys():
                    invoke = one_data[ConstantClass.InvokeMark]
                    if invoke and invoke == '1':
                        value = one_data[ConstantClass.Server]
                        result.append(value)
        if result:
            return result





    @staticmethod
    def compare_bh(source,target):
        one_table_result = []
        for i in source:
            if i not in target:
                one_table_result.append(i)
        return one_table_result






    @staticmethod
    def get_bh(target,key):
        value_list =[]
        for one in target:
            if key in one.keys():
                value = one[key]
                value_list.append(value)
        return value_list


if __name__ == '__main__':
    a = GetData()
    c = a.main()
    d = Compare(c[0],c[1])
    d.main()
