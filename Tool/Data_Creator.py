# _*_ coding: utf-8 _*_
__filename__ = 'MtrixCreator'
__author__ = 'chengtianlun'
__date__ = '2019/10/19 17:34'

from numpy import *
from TestModel import CategoryInfoTest

'''
将sql session对象转化为矩阵
'''
def EntityToMatrix(entity):
    tempMat = []
    for row in entity:
        memberList = dir(row)[:42]  # 获取类成员列表，为了保证顺序，使用list
        memberDic=row.__dict__  # 获取类成员字典
        tempLine = []
        for item in memberList:
            tempLine.append(memberDic[item])
        tempMat.append(tempLine)
    return mat(tempMat)

'''
将sql session对象转化为DataSet
'''
def EntityToDataSet(entity):
    tempMat = []
    # 如果传入实体为Company
    if  type(entity[0]).__name__ in ('Company','CompanyTest'):

        for row in entity:
            tempLine = []
            tempLine.append(row.InterID)
            tempLine.append(float(row.lng))
            tempLine.append(float(row.lat))
            tempLine.append(row.industry_label-1)  # 在投入产出表中的分类ID
            tempLine.append(row.clusterID)
            tempMat.append(tempLine)
    # 如果传入实体为Station
    if type(entity[0]).__name__ in ('Station','StationTest'):
        tempMat = []
        for row in entity:
            tempLine = []
            tempLine.append(row.StationID)
            tempLine.append(row.StaType)
            tempLine.append(float(row.lng))
            tempLine.append(float(row.lat))
            tempMat.append(tempLine)
    return mat(tempMat)

'''
将sql session对象转化为Dict
'''
def EntityToDict(entity):
    DepartmentDic = {}
    for row in entity:
        temp = row.label.strip()
        DepartmentDic[temp] = int(row.ff_label)
    return DepartmentDic

'''
建立行业大类字典
'''
def CategoryDict(categoryInfo):
    DepartmentDic = {}
    for item in categoryInfo:
        catID = item.catID
        catName = item.catName
        DepartmentDic[catID] = catName.strip()
    return DepartmentDic