from AT_02_Constant import QTConstant


class DictMethod(object):
    def __init__(self):
        self.data = QTConstant.QTConstant.Dict
        pass

    def __getattr__(self, item):
        return "未定义方法"

    def clear(self):
        """
        清空词典所有条目
        """
        Empty = self.data.clear()
        print(Empty)


if __name__ == '__main__':
    dict_method = DictMethod()
    dict_method.clear()  # {}
