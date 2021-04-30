# -*- coding: utf-8 -*-

# @Project  : PythonLearn
# @File     : __init__.py.py
# @Date     : 2021-03-31
# @Author   : Administrator
# @Info     :
# @Introduce:
import xml.etree.ElementTree as ET

unique_id = 1

def walkData(root_node, level, result_list,parent_tag,mark):
    global unique_id
    if parent_tag:
        temp = parent_tag.split(".")
        tp = []
        for o in range(0,len(temp)):
            if temp[o+1:]:
                if temp[o+1]!= temp[o]:
                    tp.append(temp[o])

            else:
                tp.append(temp[o])
        
        parent_tag = ".".join(tp)
    temp_list = [unique_id, level, root_node.tag, root_node.text,parent_tag]

    result_list.append(temp_list)
    unique_id += 1
    mark = 1
    if parent_tag:
       pass
    # 遍历每个子节点
    children_node = root_node.getchildren()

    if len(children_node) == 0:

        return
    for child in children_node:
        if unique_id == 376:
            print(level)
        if mark ==2:
            parent_tag = parent_tag.rsplit(".",1)[0]
        if isinstance(parent_tag,str):
            parent = parent_tag.rsplit(".",1)[0]
            if parent:
                parent_tag = (parent + '.' +root_node.tag + '.' + child.tag)
            else:
                parent_tag = ( root_node.tag + '.' + child.tag)
        else:
            parent_tag = (root_node.tag + '.' + child.tag)
        mark = 2


        walkData(child, level + 1, result_list,parent_tag,mark)
    return


# 获得原始数据
# out:
# [
#    #ID, Level, Attr Map
#    [1, 1, {'ID':1, 'Name':'test1'}],
#    [2, 1, {'ID':1, 'Name':'test2'}],
# ]
def getXmlData(file_name):
    level = 1  # 节点的深度从1开始
    result_list = []
    root = ET.parse(file_name).getroot()
    parent_tag = None
    mark = 2
    walkData(root, level, result_list,parent_tag,mark)

    return result_list


if __name__ == '__main__':
    file_name = 'D:\\SJT\\01_interfacedatacomparator\\文书质检自动化\\文书质检\\static\\files\\export\\ywxx_1.xml'
    R = getXmlData(file_name)
    for x in R:
        print(x)
    pass