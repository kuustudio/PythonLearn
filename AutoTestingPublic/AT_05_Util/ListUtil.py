from AT_02_Constant import Constants


def add_element(data, element):
    for i in data:
        if isinstance(i, dict) and isinstance(element, dict) is True:
            i.update(element)


def get_element(data, element) -> list:
    for i in data:
        if isinstance(i, dict) and isinstance(element, str) is True:
            if element in i.keys():
                value = list(i.values())[Constants.Zero]
                return value
            else:
                pass
