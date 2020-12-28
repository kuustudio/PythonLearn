"""
导入外部信息信息
"""
import os
from AT_00_SystemConstant import SystemConstant
from AT_02_ExportOutInputData import ExportOutDataConstant


class ExportOutData(object):
    ExportOutDataAddress = None
    dict_config_content = None

    def __init__(self, path, filename):
        self.path = path
        self.filename = filename

    def __getattr__(self, item):
        return  SystemConstant.ClassErrorMessage

    def export_main(self):
        self.spilt_config_path()
        self.get_config_content()
        return self.dict_config_content

    def spilt_config_path(self):
        """
          Description: 根据当前项目目录 拼接外部 文件地址

        """
        pwd = os.getcwd()
        grader_father = os.path.abspath(os.path.dirname(pwd) + os.path.sep + SystemConstant.FatherDirFlag)
        self.ExportOutDataAddress = grader_father + SystemConstant.DirSpiltFlag + \
                                    self.path + SystemConstant.DirSpiltFlag + self.filename

    def get_config_content(self):
        """
         获取配置内容
        :return:
        """
        try:
            file = open(self.ExportOutDataAddress, 'r', encoding="UTF-8")
            file_content = file.read()
            # eval  将字典字符串转字典。
            self.dict_config_content = eval(file_content)
        except Exception as e:
            print(SystemConstant.ExceptErrorList[SystemConstant.JsonError])
            exit()




if __name__ == '__main__':
    a = ExportOutData(ExportOutDataConstant.Constant.DirName, ExportOutDataConstant.Constant.FileName)
    result = a.export_main()
    print(result)
