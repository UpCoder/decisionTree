# -*- coding: UTF-8 -*-
from selectColumnFunction import *
import copy
# 处理正相关的函数，在这里包括信息增益、信息增益率
def handlePositive(dataMat, label, caluFunction,columnName):
    maxColumnResult = SelectColumnResult(0, columnName[0], False, -1000000)
    # print "columnName is "+str(len(dataMat[0]))
    for i in range(len(dataMat[0])):
        selectColumnResult = caluFunction(dataMat, label, i, columnName[i])
        if selectColumnResult > maxColumnResult:
            maxColumnResult = selectColumnResult
    return maxColumnResult
# 处理负相关的函数，在这里包括信息增益、信息增益率
def handleNegitive(dataMat, label, caluFunction, columnName):
    minColumnResult = SelectColumnResult(0, columnName[0], False, 99999999)
    for i in range(len(dataMat[0])):
        # print 'i is ', i
        selectColumnResult = caluFunction(dataMat, label, i, columnName[i])
        if selectColumnResult < minColumnResult:
            minColumnResult = selectColumnResult
    return minColumnResult
class GenerateDecisionTree:
    def __init__(self):
        print 'generate Decision Tree'
    # dataMat 构建的数据集
    # label 数据集对应的标签
    # columnName 每一列的名字，主要是用来构建树的时候使用
    # columnRange 每一列的取值范围
    # height 当前树的高度／深度
    # caluFunction 选择最优划分列时候的计算函数，可以选择handleCaluGain(信息增益) handleCaluGainRate（信息增益率） handleCaluGini（基尼系数）
    # handleFunction 于上面的函数有关，表面是正相关还是负相关 handleCaluGain(信息增益)：正相关 handleCaluGainRate（信息增益率）：正相关 handleCaluGini（基尼系数）：负相关
    def buildDecisionTree(self,
                          dataMat,
                          label,
                          columnName,
                          columnRanges,
                          height = 0,
                          caluFunction = handleCaluGain,
                          handleFunction = handlePositive):
        node = {}
        columnName = copy.deepcopy(columnName)
        # dataMat内已经属于同一类，不必再划分
        if countDifferentLabel(label) == 1:
            # displayArray(label)
            # print 'left node1', label[0]
            node["value"] = label[0]
            node["height"] = height
            return node
        # dataMat 不等于空 并且 他的烈数为0，就不用划分，叶子节点
        if len(dataMat) != 0 and len(dataMat[0]) == 0:
            # print 'left node2', label[0]
            node["value"] = maxDifferentLabel(label)
            node["height"] = height
            return node
        # 寻找最优的划分属性
        # print 'dataMat is'
        # displayArray(dataMat)
        selectColumnResult = handleFunction(dataMat, label, caluFunction, columnName)
        # 确定以第maxValue列的属性作为划分的属性
        # print 'maxValue is ', columnName[selectColumnResult.getIndex()]
        # displayMatAndLabel(dataMat, label)
        node["value"] = selectColumnResult
        node["height"] = height
        if not selectColumnResult.isNumber:
            # 离散值的分类方法
            # canSelectValue = arrayDifferentDataMat(dataMat, maxValue)
            canSelectValue = columnRanges[columnName[selectColumnResult.getIndex()]]
            # displayArray(canSelectValue)
            del columnName[selectColumnResult.index]
            for i in canSelectValue:
                # print i
                # displayMatAndLabel(dataMat, label)
                newDataMat, newLabel = findRows(dataMat, label, selectColumnResult.index, i)
                if len(newDataMat) == 0:
                    # print 'left node3 ', maxDifferentLabel(label)
                    newNode = {}
                    newNode["value"] = maxDifferentLabel(label)
                    newNode["height"] = height + 1
                    node[i] = newNode
                    continue
                # displayMatAndLabel(newDataMat, newLabel)
                node[i] = self.buildDecisionTree(newDataMat, newLabel, copy.deepcopy(columnName), columnRanges, height + 1)
        else:
            # 连续值的分类方法
            consecutiveValue = selectColumnResult.getSelectValue()
            # print 'splitValue is ', consecutiveValue
            newDataMatBig, newLabelBig, newDataMatSmall, newLabelSmall = findRowsWithConsecutiveValue(
                dataMat,
                label,
                selectColumnResult.index,
                consecutiveValue)
            if len(newDataMatBig) == 0:
                newNode = {}
                newNode["value"] = maxDifferentLabel(label)
                newNode["height"] = height + 1
                node["否"] = newNode
            else:
                node["否"] = self.buildDecisionTree(newDataMatBig, newLabelBig, copy.deepcopy(columnName), columnRanges,
                                         height + 1)
            if len(newDataMatSmall) == 0:
                newNode = {}
                newNode["value"] = maxDifferentLabel(label)
                newNode["height"] = height + 1
                node["是"] = newNode
            else:
                node["是"] = self.buildDecisionTree(newDataMatSmall, newLabelSmall, copy.deepcopy(columnName), columnRanges,
                                         height + 1)
                # print 'number'
        return node
class TestAccurate:
    def __init__(self):
        print 'test accurate'
    def leftOutTest(self,node,testData,testLabel,columnName):
        right = 0
        for x in range(len(testData)):
            predictResult = self.executePredict(node, testData[x], columnName)
            # print predictResult, testLabel[x]
            if predictResult == testLabel[x]:
                displayArray(testData[x])
                print testLabel[x]
                right += 1
        return (1.0 * right) / (1.0 * len(testLabel))
    def executePredict(self,node,row,columnName):
        while isinstance(node, dict):
            rootName = node['value']  # columnName
            if isinstance(rootName, SelectColumnResult):
                # print rootName.getIndex()
                if rootName.getIsNumber():
                    # 联系值的划分节点
                    splitValue = rootName.getSelectValue()  # 获得被选中过的值
                    # print '1 name is ', rootName.getName(), 'index is ', translateChinese(rootName.getName(), columnName)
                    value = row[translateChinese(rootName.getName(), columnName)]
                    if value <= splitValue:
                        # print 'finish single1'
                        node = node["是"]
                    else:

                        # print 'finish single2'
                        node = node["否"]
                else:
                    # 离散的划分节点
                    rootIndex = translateChinese(rootName.getName(), columnName)
                    # print '2 name is ', rootName.getName(), 'index is ', translateChinese(rootName.getName(), columnName)
                    if rootIndex == len(columnName):
                        # print 'finish single3'
                        return rootName
                    value = row[rootIndex]
                    node = node[value]
            else:
                # print 'finish single4'
                return rootName  # 不是SelectColumnResult类型的话，说明就是叶子节点
        return 'error'
