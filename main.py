# -*- coding: UTF-8 -*-
# coding=utf-8   #等号两边不能有空格，格式要求,编码方式可改gbk等
from buildTree import *
dataMat, label, columnName = loadDataSet("/Users/Liang/PycharmProjects/DecisionTree/dataset2.txt")
#print caluInfomationGainConsecution(dataMat, label, 6)
# columnRanges = columnsDiffRange(dataMat, columnName)
# displayArray(columnRanges)
# node = buildID3Tree(dataMat, label, columnName, columnRanges)
# print '-----图4.4------'
# displayTree(node)
# print '-----图4.5------'
# print len(columnName)
# newDataMat, newLabel, testDataMat, testLabel = splitDataMatAndLabel(dataMat, label, [0, 1, 2, 5, 6, 9, 13, 14, 15, 16])
# newNode = buildID3Tree(newDataMat, newLabel, columnName, columnRanges, 0, caluInformationGainRate, handlePositive)
# newNode = buildID3Tree(newDataMat, newLabel, columnName, columnRanges, 0, caluInfomationGain, handleNegitive)
# displayTree(newNode)
# print leftOutTest(newNode, testDataMat, testLabel, columnName)
