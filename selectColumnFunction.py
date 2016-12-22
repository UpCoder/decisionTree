# -*- coding: UTF-8 -*-
from usedFunction import *
from numpy import *
# label 是标签
def caluInformationEntropy(label):
    res = 0.0
    countAll = len(label)
    if(countAll == 0):
        return 0.0
    setContainer = {}
    for i in range(len(label)):
        if label[i] in setContainer:
            setContainer[label[i]] += 1
        else:
            setContainer[label[i]] = 1
    for x in setContainer:
        p = (setContainer[x]*1.0)/(countAll*1.0)
        if p == 0:
            continue
        res += p*log2(p)
    return -res
# datamat 是样本数据 label是样本标签 x 是根据第x个属性划分数据集 x的值是连续的
def caluInfomationGainConsecution(dataMat,label,x):
    res = 99999999
    resIndex = dataMat[0][x]
    values = [];
    for temp in dataMat:
        values.append(double(temp[x]))
    values.sort()   # 进行排序,从小到大
    for i in range(len(values)-1):
        splitValue = (1.0*values[i]+1.0*values[i+1])/2.0
        print splitValue
        newDataMatSmall = []
        newLabelSmall = []
        newDataMatBig = []
        newLabelBig = []
        index = 0
        for temp in dataMat:
            if double(temp[x]) <= splitValue:
                newDataMatSmall.append(temp)
                newLabelSmall.append(label[index])
            else:
                newDataMatBig.append(temp)
                newLabelBig.append(label[index])
            index += 1
        tempValue = caluInformationEntropy(newLabelBig)*((1.0*len(newLabelBig))/(1.0*len(label)))\
                    +caluInformationEntropy(newLabelSmall)*((1.0*len(newLabelSmall))/(1.0*len(label)))
        if tempValue < res:
            res = tempValue
            resIndex = splitValue
    return caluInformationEntropy(label)-res, resIndex
# datamat 是样本数据 label是样本标签 x 是根据第x个属性划分数据集
def caluInfomationGain(dataMat,label,x):
    res = 0.0
    allX = set([])  # set 集合,可以去重
    for temp in dataMat:
        allX.add(temp[x])
    for i in allX:
        newDataMat = []
        newLabel = []
        indexJ = 0
        for j in dataMat:
            if j[x] == i:
                newDataMat.append(j)
                newLabel.append(label[indexJ])
            indexJ += 1
        res += caluInformationEntropy(newLabel)*((1.0*len(newLabel))/(1.0*len(label)))
    res = caluInformationEntropy(label) - res
    return res
# datamat 是样本数据 label是样本标签 x 是根据第x个属性划分数据集 信息增益率
def caluInformationGainRate(dataMat,label,x):
    gain = caluInfomationGain(dataMat, label, x)
    dict = dictDifferentDataMat(dataMat,x)
    IV = 0.0;
    for x in dict:
        posibility = (dict[x]*1.0)/(1.0*len(label))
        IV += posibility*log2(posibility)
    IV = -IV
    return gain/IV
# datamat 是样本数据 label是样本标签 x 是根据第x个属性划分数据集 基尼系数
def caluInformationGini(dataMat,label,x):
    res = 0.0
    dict = dictDifferentDataMat(dataMat, x)
    for x in dict:
        posibility = (dict[x]*1.0)/(1.0*len(label))
        res += posibility*posibility
    res = 1 - res
    return res
