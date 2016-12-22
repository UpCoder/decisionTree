# -*- coding: UTF-8 -*-
from selectColumnFunction import *
import copy
# 处理正相关的函数，在这里包括信息增益、信息增益率
def handlePositive(dataMat, label, caluFunction):
    maxIndex = -100.0
    maxValue = ""
    for i in range(len(dataMat[0])):
        curGain = caluFunction(dataMat, label, i)
        if curGain > maxIndex:
            maxValue = i
            maxIndex = curGain
    return maxIndex, maxValue
# 处理负相关的函数，在这里包括信息增益、信息增益率
def handleNegitive(dataMat, label, caluFunction):
    maxIndex = 999999.0
    maxValue = ""
    for i in range(len(dataMat[0])):
        curGain = caluFunction(dataMat, label, i)
        if curGain < maxIndex:
            maxValue = i
            maxIndex = curGain
    return maxIndex, maxValue
# 构建决策数，现在默认的是使用信息增益作为评判的标准
def buildID3Tree(dataMat,label,columnName,columnRanges,height=0, caluFunction=caluInfomationGain,handleFunction = handlePositive):
    node = {}
    columnName = copy.deepcopy(columnName)
    # dataMat内已经属于同一类，不必再划分
    if countDifferentLabel(label) == 1:
        displayArray(label)
        print 'left node1', label[0]
        node["value"] = label[0]
        node["height"] = height
        return node
    # dataMat 不等于空 并且 他的烈数为0，就不用划分，叶子节点
    if len(dataMat) != 0 and len(dataMat[0]) == 0:
        print 'left node2', label[0]
        node["value"] = maxDifferentLabel(label)
        node["height"] = height
        return node
    # 寻找最优的划分属性
    maxIndex, maxValue = handleFunction(dataMat, label, caluFunction)
    # 确定以第maxValue列的属性作为划分的属性
    print 'maxValue is ', maxValue
    displayArray(columnName)
    node["value"] = columnName[maxValue]
    node["height"] = height
    # canSelectValue = arrayDifferentDataMat(dataMat, maxValue)
    canSelectValue = columnRanges[columnName[maxValue]]
    displayArray(canSelectValue)
    del columnName[maxValue]
    for i in canSelectValue:
        print i
        displayMatAndLabel(dataMat, label)
        newDataMat, newLabel = findRows(dataMat, label, maxValue, i)
        if len(newDataMat) == 0:
            print 'left node3 ', maxDifferentLabel(label)
            newNode = {}
            newNode["value"] = maxDifferentLabel(label)
            newNode["height"] = height + 1
            node[i] = newNode
            continue
        displayMatAndLabel(newDataMat, newLabel)
        node[i] = buildID3Tree(newDataMat, newLabel, copy.deepcopy(columnName), columnRanges, height+1)
    return node
#获取所有的列的取值范围
def columnsDiffRange(dataMat, columnName):
    res = {}
    for x in range(len(dataMat[0])):
        temp = set([])
        for y in range(len(dataMat)):
            temp.add(dataMat[y][x])
        res[columnName[x]] = temp;
    return res
# 留出法测试
def leftOutTest(node, testData ,testLabel,columnName):
    right = 0
    for x in range(len(testData)):
        predictResult = executePredict(node, testData[x], columnName)
        print predictResult, testLabel[x]
        if predictResult == testLabel[x]:
            right += 1
    return (1.0*right)/(1.0*len(testLabel))
# 根据node进行预测
def executePredict(node, row,columnName):
    while isinstance(node, dict):
        rootName = node['value'] #columnName
        rootIndex = translateChinese(rootName, columnName)
        if(rootIndex == len(columnName)):
            return rootName
        value = row[rootIndex]
        node = node[value]
    return 'error'
