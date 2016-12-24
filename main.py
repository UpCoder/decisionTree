# -*- coding: UTF-8 -*-
# coding=utf-8   #等号两边不能有空格，格式要求,编码方式可改gbk等
from buildTree import *
import math
# bank 数据集
dataMat, label, columnName = loadDataSet("./bank.txt", ';', True)
testDataMat, testLabel, testColumnName = loadDataSet("./banktest.txt", ";", True)
columnRanges = columnsDiffRange(dataMat, columnName)
displayArray(columnRanges)
node = buildID3Tree(dataMat, label, columnName, columnRanges, 0, handleCaluGini, handleNegitive)
displayTree(node)
print leftOutTest(node, testDataMat, testLabel, columnName)


# dataMat, label, columnName = loadDataSet("./dataset3.txt", ',')
# columnRanges = columnsDiffRange(dataMat, columnName)
# node = buildID3Tree(dataMat, label, columnName, columnRanges)
# print '-----图4.4------'
# displayTree(node)
# print leftOutTest(node,testDataMat, testLabel, columnName)
# print '-----图4.5------'
# print len(columnName)

# dataMat, label, columnName = loadDataSet("./dataset3.txt", ',', False)
# displayArray(columnName)
# displayMatAndLabel(dataMat, label)
# columnRanges = columnsDiffRange(dataMat, columnName)
# newDataMat, newLabel, testDataMat, testLabel = splitDataMatAndLabel(dataMat, label, [0, 1, 2, 5, 6, 9, 13, 14, 15, 16])
# newNode = buildID3Tree(newDataMat, newLabel, columnName, columnRanges, 0, handleCaluGini, handleNegitive)
# print 'test value is '
# displayMatAndLabel(testDataMat, testLabel)
# print 'columnName is '
# displayArray(columnName)
# displayTree(newNode)
# print leftOutTest(newNode, testDataMat, testLabel, columnName)
