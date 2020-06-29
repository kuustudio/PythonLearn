# 这个是关于Python操作file的方法文件
import os


class FileMethod:
    pass


def get_file_path():

    pwd = os.getcwd()
    father_path = os.path.abspath(os.path.dirname(pwd) + os.path.sep + ".")
    grader_father = os.path.abspath(os.path.dirname(pwd) + os.path.sep + "..")
    return grader_father

