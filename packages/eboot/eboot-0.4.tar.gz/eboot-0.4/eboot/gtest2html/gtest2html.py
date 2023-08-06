import re
import os
from pathlib import Path
from typing import List
import xml.etree.ElementTree as ET
from eboot import PlatformEnvirConfigs
from eboot.gtest2html import CreateTestReports

# 判断是否是GTest XML格式的测试报告


def isGtestXML(xml: str):
    tree = ET.parse(xml)
    root = tree.getroot()
    if (root.tag != "testsuites"):
        return False

    for child in root:
        if (child.tag != "testsuite"):
            return False
        for children in child:
            if (children.tag != "testcase"):
                return False
    return True


def gtest2html(files: List[Path], output: Path):
    output = os.path.abspath(os.path.realpath(output))
    file_list = []
    for file in files:
        file = os.path.abspath(os.path.realpath(file))
        if os.path.isfile(file) and isGtestXML(file):
            file_list.append(file)
        else:
            listdir = os.listdir(file)
            for value in listdir:
                match = re.match(".*.xml", value)
                if match and isGtestXML(os.path.join(file, match.group())):
                    file_list.append(os.path.join(file, match.group()))
    # 如果输出文件夹不存在，就创建
    if not os.path.isdir(output):
        os.makedirs(output)
    report = os.path.join(output, "test_report.xml")
    if os.path.exists(report):
        os.remove(report)

    # 创建合并的报告文件
    with open(report, "w", encoding="utf-8") as f:
        f.write(r"<?xml version='1.0' encoding='utf-8'?><testsuites></testsuites>")
        f.close()
    tree = ET.parse(report)
    root = tree.getroot()
    testsuiteMap = {}
    kind = ["tests", "failures", "disabled", "errors"]

    # 遍历文件列表
    for file in file_list:
        tmpTree = ET.parse(file)
        tmpRoot = tmpTree.getroot()

        # 合并元素
        for child in tmpRoot:
            if testsuiteMap.get(child.attrib.get('name'), False):

                tmpChild = testsuiteMap[child.attrib.get('name')]

                for key in child.attrib.keys():
                    if key in kind:
                        ET.Element.set(tmpChild, key, str(int(tmpChild.attrib.get(
                            key, "0")) + int(child.attrib.get(key, "0"))))
                    elif key == "time":
                        t1 = float(tmpChild.attrib.get(key, "0"))
                        t2 = float(child.attrib.get(key, "0"))
                        if t1 < t2:
                            t1 = t2
                        ET.Element.set(tmpChild, key, str(t1))
                    else:
                        ET.Element.set(
                            tmpChild, key, child.attrib.get(key, "0"))

                for subchild in child:
                    tmpChild.append(subchild)
                testsuiteMap[child.attrib.get('name')] = tmpChild
            else:
                testsuiteMap[child.attrib.get('name')] = child

    # 计算root的属性值，并将元素加入root节点里
    for child in testsuiteMap.values():
        for key in child.attrib.keys():
            if key in kind:
                ET.Element.set(root, key, str(int(root.attrib.get(
                    key, "0")) + int(child.attrib.get(key, "0"))))
            elif key == "time":
                ET.Element.set(root, key, str(float(root.attrib.get(
                    key, "0")) + float(child.attrib.get(key, "0"))))
            else:
                ET.Element.set(root, key, child.attrib.get(key, "0"))
        root.append(child)

    # 输出报告文件
    tree.write(report, "utf-8", True)
    PlatformEnvirConfigs.LoadConfig()
    CreateTestReports.CreateTestReports(output)
