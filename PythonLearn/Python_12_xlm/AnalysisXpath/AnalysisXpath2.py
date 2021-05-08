# -*- coding: utf-8 -*-

# @Project  : PythonLearn
# @File     : AnalysisXML.py
# @Date     : 2021-03-31
# @Author   : Administrator
# @Info     :
# @Introduce:
import requests, re
from xml.dom.minidom import parseString
import xml.dom.minidom
from functools import wraps


def test_request() -> str:
    url = "http://172.18.21.144:8086/api/v1/writCheckForZj"
    data = {
        "content": "河南省郑州市中级人民法院\n行 政 裁 定 书\n（2019）豫01行终492号\n上诉人（原审原告）冯子军，男，汉族，1952年1月16日出生。\n"
                   "被上诉人（原审被告）荥阳市司法局，住所地：荥阳市万山路政法街2号。统一社会信用代码：11410182005291054B。\n法定代表人贾学军，局长。\n"
                   "委托代理人聂志强，河南神龙剑律师事务所律师。\n上诉人冯子军因诉被上诉人荥阳市司法局其他行政行为一案，不服河南省巩义市人民法院（2019）豫0181行初25"
                   "号行政裁定，向本院提起上诉。本院受理后，依法组成合议庭审理了本案。现已审理终结。\n原审法院认为：冯子军所诉的荥阳市司法局于2016年6月3"
                   "日作出的处理意见书，是其对信访事项的处理，本案被诉行政行为属于信访事项，根据《最高人民法院关于适用〈中华人民共和国行政诉讼法〉的解释》第一条第二款第九项之规定，不属于人民法院行政诉讼的受案范围，故冯子军提起本案诉讼不符合《中华人民共和国行政诉讼法》第四十九条第四项规定的条件。对其起诉应不予立案，已经立案的，应当裁定驳回起诉。依照《最高人民法院关于适用〈中华人民共和国行政诉讼法〉的解释》第六十九条第一款第一项、第三款之规定，裁定：驳回冯子军的起诉。案件受理费50元，待本裁定生效后退还冯子军。\n上诉人冯子军不服，上诉称：由于市信访局登记受理转交的是一宗共三个诉求内容的信访案件，荥阳市司法局接到该信访件后，有关党务的，应当申明理由，退给市信访局，其不但不退，又不把三项诉求内容放在一起做出一份信访事项处理意见书，而是做出三份信访事项处理意见书。且冯子军手中有荥组（1977）100号文件，在市信访局填写的登记受理申请表中就没有该项诉求，但荥阳市司法局却对该文件做出了处理意见书。上述行为导致受众群体不明真相，使冯子军的人格尊严受到质疑，应认定违法。故请求：撤销一审裁定，支持冯子军的一审诉讼主张。\n被上诉人荥阳市司法局辩称，冯子军2016年6月3日做出的信访事项处理意见书的行为并非行政行为，不属于行政诉讼的受案范围。二、冯子军所诉事项属于重复起诉，依法应当不予受理。在（2016）豫0181行初96号行政裁定书、（2016）豫01行辖终769号行政裁定书、（2018）豫行申617号行政裁定书中均对本案冯子军所诉内容及事实做出了结论，认为属于信访事项，不属于人民法院行政案件的受案范围，以上均为生效文书。现冯子军旧事重提，显然是重复诉讼的行为，依法应当不予受理该案。综上，请求法院依法裁决。\n经审理查明，冯子军于2016年2月16日到荥阳市信访局反映问题，并在登记表上写明反映的主要问题是：三十多年前开除、恢复党籍文件，组织部不让本人见到，更不发给本人。通过局党总支向组织部提出申请，要求把开除、恢复党籍文件发给本人，但三年来没有结果。三十多年前恢复工作文件，组织部不让本人见到，更不发给本人。通过局党总支向组织部提出申请，组织部把文件补发给了本人。但针对不补发工资的决定，向组织部提出做出该决定的政策依据是什么，三年来未作出回复。同时写明信访诉求是：1.要求将开除、恢复党籍文件发给本人。2.要求组织部提供不补发工资决定的政策依据。荥阳市信访局将上述信访件转给荥阳市司法局，荥阳市司法局于2016年5月26日下发并向冯子军送达了信访事项处理意见书（编号LF20160033102），就信访人要求补发恢复党籍的文件、信访人1980年至1985年“工资不再补发”问题作出处理意见：1.恢复党籍文件因历史原因未查找到。2.不再补发工资问题有文件批示。荥阳市司法局又于2016年6月2日下发并于次日向冯子军送达了信访事项处理意见书（编号LF20160033102），就信访人要求补发恢复党籍文件的问题作出处理意见。该处理意见查明1977年9月24日荥阳县委组织部关于荥组（1977）100号文的内容，并查明此文件由荥阳市档案馆对冯子军本人出具盖有档案馆印鉴的复制件。冯子军又向荥阳市人民政府申请对要求补发开除党籍文件问题进行复查。荥阳市人民政府于2016年9月8日作出并于次日向冯子军送达了信访事项复查不予受理告知书，认为冯子军申请复查的信访事项，按照《信访条例》和《信访事项复查复核受理办理指导意见》规定，属于不予受理的情况，不应重复或越级上访。冯子军对荥阳市司法局于2016年6月2日下发并于次日送达的信访事项处理意见书（编号LF20160033102）提起本案之诉，要求确认违法并予以撤销。\n本院认为，冯子军所诉的荥阳市司法局于2016年6月2日下发并于次日送达的信访事项处理意见书（编号LF20160033102），是就信访人要求补发恢复党籍文件的问题作出处理意见。由于该被诉行政行为属于冯子军提起的信访事项，依据《最高人民法院关于适用〈中华人民共和国行政诉讼法〉的解释》第一条第二款第九项之规定，行政机关针对信访事项作出的登记、受理、交办、转送、复查、复核意见等行为不属于人民法院行政诉讼的受案范围，故冯子军提起本案之诉不符合《中华人民共和国行政诉讼法》第四十九条第四项规定的起诉条件。对其起诉应不予立案，已经立案的，应当裁定驳回其起诉。因此一审驳回冯子军的起诉并无不当。另外，针对冯子军的一个信访件，反映的三个信访诉求，荥阳市司法局为何不形成一个处理意见而是形成两个处理意见，荥阳市司法局解释称由于涉及历史、档案问题，需要进行调查，在部分查清后，就先部分答复，所以先后查清就先后形成了两个处理意见。据此本院认为，荥阳市司法局的解释基本符合常理，且也无相关法律法规要求针对包含多个诉求的一个信访件必须形成一个处理意见。但是由于冯子军反映的三个诉求确实具有一定的关联性和历史连续性，荥阳市司法局形成两个处理意见确有不当，在以后信访事项处理工作中应予改进。由于冯子军的工作、党籍等问题均予以恢复和落实，该处理意见不至于使冯子军的人格尊严受到质疑，如有其他侵犯其人格尊严权利的事实及行为的，可通过法律途径另行主张权利。\n综上，冯子军的上诉理由不能成立，本院不予支持。一审裁定适用法律正确，依照《中华人民共和国行政诉讼法》第八十九条第一款第一项规定，裁定如下：\n驳回上诉，维持原裁定。\n二审案件受理费50元，退还冯子军。\n本裁定为终审裁定。\n审判长　　崔航微\n审判员　　王　冰\n审判员　　姚付良\n二〇一九年六月二十日\n书记员　　平　航",
        "indexBh": "d82ba897eeba48519a250a85256b2883",
        "checkType": "1", }

    headers = {'Content-Type': "application/json"}

    res = requests.post(url=url, json=data, headers=headers)
    res.encoding = 'utf-8'
    interface_content = res.text
    return interface_content


def deal_xml(content, target_path, **kwargs):
    target_tag = None
    try:
        if target_path:
            path_list = target_path.split(".")
            if path_list:
                DOMTree = parseString(content)
                collection = DOMTree.documentElement
                # 确定是不是可以解析的 起始元素
                rule_tags, start_index = start_element(collection, path_list)
                # 起始元素要放在递归外面
                target_element = get_target_node(collection, start_index,  path_list)
                print(target_element)

    except Exception as e:
        print(e)

    return target_tag


def get_target_node(collection, start_index, path_list):
    result = None
    pos = None
    temp_str = path_list[start_index].split("[")[0]
    # 获取第几个元素
    pd = re.compile(r'[[](.*)[]]', re.S)
    temp_index = re.findall(pd, path_list[start_index])
    if temp_index:
        pos = int(temp_index[0])-1
        # 如果是最后一个,且没有指定获取第几个
    elif not path_list[start_index +1:]:
        pos = -1
    else:
        pos = 0
    temp_node_list = collection.getElementsByTagName(temp_str)
    if temp_node_list:
        result = temp_node_list[pos]
        start_index += 1
        if start_index == len(path_list) and "Text" in str(type(result.childNodes[0])):
            return result.childNodes[0].data
        return get_target_node(result, start_index, path_list)



def start_element(collection, path_list):
    """
     确定是不是可以解析的 起始元素
    :param collection:  DOM初始值
    :param path_list:  元素列表
    :return: 返回结果
    """
    rule_tags = None
    temp_index = None
    for  i in path_list:
        j = i.split('[')[0]
        rule_tags = collection.getElementsByTagName(j)
        if rule_tags:
            temp_index = path_list.index(i)
            break
    return rule_tags, temp_index


def has_element_child(node_name):
    has_element = 0
    for child in node_name.childNodes:
        if child.nodeType == 1:
            has_element += 1
    return has_element


if __name__ == '__main__':
    x = test_request()
    path = "result.writcheck[1].ruleerror[2].sentences[1].sentence"
    # 使用参数 Opera 判断是否分解整个xml 如果没时间后续规划
    Opera = False
    # 使用 动态参数 flag 如果有值则比较没有值直接获取目标
    flag = {"gzbs", "DC1045"}
    deal_xml(x, path)
