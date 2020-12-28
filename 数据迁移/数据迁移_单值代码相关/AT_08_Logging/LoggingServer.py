from  AT_00_SystemConstant import SystemConstant
from  AT_09_CommonMethod import CommonMethodServer
import logging, os, json,traceback


def get_log_file(error,group):
    file = None
    try:
        DirName = SystemConstant.location
        pwd = os.getcwd()
        grader_father = os.path.abspath(os.path.dirname(pwd) + os.path.sep + SystemConstant.FatherDirFlag)
        LogPath = grader_father + SystemConstant.DirSpiltFlag + SystemConstant.LogPath
        if not os.path.exists(LogPath):
            os.mkdir(LogPath)
        TodayDir = LogPath + SystemConstant.DirSpiltFlag + DirName
        if not os.path.exists(TodayDir):
            os.mkdir(TodayDir)
        ServerDir = TodayDir + SystemConstant.DirSpiltFlag + group
        if not os.path.exists(ServerDir):
            os.mkdir(ServerDir)

        file = ServerDir + SystemConstant.DirSpiltFlag + error \
               + SystemConstant.LogPath + SystemConstant.StrLocalTime + ".txt"
    except Exception as e:
        print(e)
    if file:
        return file


def program_error(message,error_type,file_name, mark,*args):

    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    fh = logging.FileHandler(file_name)
    fh.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(userid)s - %(message)s')
    fh.setFormatter(formatter)
    logger.addHandler(fh)
    Info = ""

    for i in args:
        if isinstance(i,dict):
            result = CommonMethodServer.dict_to_str(i)
            logger.debug(result,extra={'userid':SystemConstant.Debug})
        else:
            one = "\n" +i
            Info += one
    logger.info(message,extra={'userid':SystemConstant.Info})
    logger.info(error_type,extra={'userid':SystemConstant.Info})
    a = "\n"+"="*50
    Info += a
    if mark == SystemConstant.One:
        logger.error(Info,extra={'userid':SystemConstant.Info})

    elif mark == SystemConstant.Tow:
        logger.debug(Info,extra={'userid':SystemConstant.Info})
    logger.removeHandler(fh)

if __name__ == '__main__':
    pass
    program_error("ValueError", 2, "eedsds", "fegegrgrg")