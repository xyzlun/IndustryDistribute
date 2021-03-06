# _*_ coding: utf-8 _*_
__filename__ = 'Company_Statistic'
__author__ = 'chengtianlun'
__date__ = '2019/11/2 12:16'

import os
import xlwt
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from collections import Counter


from Tool import Data_Creator
from Models import *
from TestModel import *

def CompanyStatistic(companys,industryLabelDict,k,filename):
    workbook = xlwt.Workbook(encoding='utf-8')  # 新建工作簿
    sheet1 = workbook.add_sheet('sheet1')  # 新建sheet

    num_style = xlwt.XFStyle()  # 设置数字单元格样式
    num_style.num_format_str='0.00%'
    num_style.alignment.horz = 2  # 水平居中

    str_style = xlwt.XFStyle()  # 设置中文单元格样式
    str_style.alignment.horz = 2  # 水平居中

    # 填写行标题
    for i in range(k):
        sheet1.write(0,i*2,'Cluster '+str(i),style=str_style)
        sheet1.col(i*2).width = 256 * 15
        sheet1.write(0,i*2 + 1,'占比',style=str_style)
        sheet1.col(i*2+1).width = 256 * 15

    for i in range(k):
        cluster_label = companys.with_entities(CompanyTest.industry_label).filter(CompanyTest.clusterID == i)
        total = cluster_label.count()
        temp_list = []
        for item in cluster_label:
            temp_list.append(industryLabelDict[item[0]])
        ElemCounter = Counter(temp_list).items()
        ElemList = sorted(ElemCounter, key=lambda x: x[1],reverse=True)
        for j,item in enumerate(ElemList):
            sheet1.write(j+1,i*2,item[0],str_style)
            # sheet1.write(j+1,i*2+1,ElemCounter[item])  # 个数
            sheet1.write(j+1,i*2+1,float(item[1]/total),style=num_style)  # 百分比

    if filename=='test': workbook.save('../result/'+filename+'.xls')   #保存test
    else : workbook.save('./result/'+filename+'.xls')   #保存

    print('company statistic sheet saved')



if __name__=='__main__':
    # 创建连接引擎
    host = 'localhost'
    port = 3306
    username = 'root'
    password = 'password'
    db = 'qcc_data'
    connect_str = 'mysql+mysqlconnector://{}:{}@{}:{}/{}'.format(username, password, host, port,db)

    engine = create_engine(connect_str, echo=True)
    Session = sessionmaker(bind=engine)
    session = Session()

    #companysQuery = session.query(CompanyTest).filter(CompanyTest.clusterID==1)  # 读取所有公司信息
    companysQuery = session.query(CompanyTest)
    categoryInfoQuery = session.query(CategoryInfoTest)
    industry_labelQuery = session.query(IndustryLabelTest)
    IndustryLabelDict = Data_Creator.CategoryDict(categoryInfoQuery)  # 键为ID，值为行业名

    CompanyStatistic(companysQuery,IndustryLabelDict,18,'test')