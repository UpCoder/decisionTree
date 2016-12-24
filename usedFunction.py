# -*- coding: UTF-8 -*-
import Queue
from numpy import *
def displayArray(array):
    index = 0
    for x in array:
        if isinstance(x,list) or  isinstance(x, set):
            print index,
            displayArray(x)
        else:
            print x,
        index += 1
    print '\n'
# 展示一棵树 层次序遍历
def displayTree(node):
    q = Queue.Queue()
    q.put(node)
    curH = 0
    while not q.empty():
        curNode = q.get()
        if isinstance(curNode, dict):
            for x in curNode:
                if x == 'value':
                    if curNode['height'] != curH:
                        print '\n\n\n'
                        curH = curNode['height']
                    print curNode[x],
                elif x != 'height':
                    q.put(curNode[x])
    print '\n\n\n'
# 展示dataMat 和 label两个（两个行数相同）
def displayMatAndLabel(dataMat,label):
    i = 0
    for x in dataMat:
        print i,
        for y in x:
            print y,
        print label[i]
        i += 1
# 将selectIndex（数组）里面的行挑出来 分成两组数据
def splitDataMatAndLabel(dataMat,label,selectIndex):
    newDataMat = []
    newLabel = []
    otherDataMat = []
    otherLabel = []

    for i in range(len(dataMat)):
        if i in selectIndex:
            newDataMat.append(dataMat[i])
            newLabel.append(label[i])
        else:
            otherDataMat.append(dataMat[i])
            otherLabel.append(label[i])
    return newDataMat, newLabel, otherDataMat, otherLabel
def loadDataSet(filePath,splitMark,loadFirst):
    dataMat = []
    label = []
    columnName = []
    with open(filePath) as readFile:
        line = readFile.readline()
        splitRes = line.strip().split(splitMark)
        if loadFirst:
            columnName.extend(splitRes[0:len(splitRes)-1])
        else:
            columnName.extend(splitRes[1:len(splitRes)-1])
        for line in readFile.readlines():
            splitRes = line.strip().split(splitMark) # 要注意把多余的空格删去 strip即可，否则划分的时候容易多出来其他值
            tempArr = []
            for x in range(len(splitRes)-1):
                if x == 0 and loadFirst:
                    if isNumber(splitRes[x]):
                        tempArr.append(double(splitRes[x]))
                    else:
                        tempArr.append(splitRes[x])
                    continue
                if x == 0 and (not loadFirst):
                    continue
                if isNumber(splitRes[x]):
                    tempArr.append(double(splitRes[x]))
                else:
                    tempArr.append(splitRes[x])
            dataMat.append(tempArr)
            label.append(splitRes[-1])
    return dataMat, label, columnName
# 返回label有多少个类比
def countDifferentLabel(label):
    labelSet = set(label)
    return len(labelSet)
# 返回datamat第i列有多少可选的属性值
def arrayDifferentDataMat(dataMat,j):
    array = set([])
    for i in range(len(dataMat)):
        array.add(dataMat[i][j])
    return array
# 返回datamat第i列有多少可选的属性值以及出现的次数 [index value(出现的次数)]
def dictDifferentDataMat(dataMat,j):
    dict = {}
    for x in dataMat:
        if x[j] in dict:
            dict[x[j]] += 1
        else:
            dict[x[j]] = 1
    return dict
# 返回label里面不同标签出现次数最多的标签的个数
def maxDifferentLabel(label):
    maxIndex = 0
    maxValue = label[0]
    setContainer = {}
    for x in label:
        if x in setContainer:
            setContainer[x] += 1
            if setContainer[x] > maxIndex:
                maxValue = x
        else:
            setContainer[x] = 1
    return maxValue
# 找到dataMat第index列的值位value的行，并且找到对应的label行
def findRows(dataMat,label,index,value):
    newDataMat = []
    newLabel = []
    i = 0
    for x in dataMat:
        if x[index] == value:
            newDataMat.append(x)
            newDataMat[len(newDataMat)-1] = newDataMat[len(newDataMat)-1][0:index]+newDataMat[len(newDataMat)-1][index+1:]
            newLabel.append(label[i])
        i += 1
    return newDataMat, newLabel
# 将dataMat的第index列根据splitvalue 划分成小雨等于和大于的两部分
def findRowsWithConsecutiveValue(dataMat,label,index,splitVale):
    newDataMatBig = []
    newLabelBig = []
    newDataSmall = []
    newLabelSmall = []
    i = 0
    for x in dataMat:
        if double(x[index]) <= double(splitVale):
            newDataSmall.append(x)
            newLabelSmall.append(label[i])
        else:
            newDataMatBig.append(x)
            newLabelBig.append(label[i])
        i += 1
    return newDataMatBig, newLabelBig, newDataSmall, newLabelSmall
def translateChinese(value,columnName):
    res = 0
    for x in columnName:
        if x == value:
            return res
        res += 1
    return res
def isNumber(x):
    try:
        double(x)
        return True
    except:
        return False
