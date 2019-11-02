# _*_ coding: utf-8 _*_

__filename__ = 'TestMain'
__author__ = 'chengtianlun'
__date__ = '2019/10/21 9:49'

import datetime

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from Tool import Data_Creator,Map_Labeler,Company_Statistic
from Algorithm import kMeans
from Models import *
from TestModel import *
from FigDrawing import *



'''
测试用
'''
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

#region 从数据库读取数据
companysQuery = session.query(CompanyTest)  # 读取所有公司信息
stationsQuery = session.query(StationTest)  # 读取所有地铁站信息
in_out_sheetQuery = session.query(InOutSheetTest)  # 读取投入产出表
industry_labelQuery = session.query(IndustryLabelTest)
categoryInfoQuery = session.query(CategoryInfoTest)  # 读取行业大类信息
#endregion

#region 预处理数据
#IndustryLabelDict = Data_Creator.EntityToDict(industry_labelQuery)  # 废弃
CompanySet = Data_Creator.EntityToDataSet(companysQuery)
StationSet = Data_Creator.EntityToDataSet(stationsQuery)
InOutMtrix = Data_Creator.EntityToMatrix(in_out_sheetQuery)
IndustryLabelDict = Data_Creator.CategoryDict(categoryInfoQuery)  # 键为ID，值为行业名
#endregion


#region 聚类
k = 18
kMeansTest = kMeans.kMeansCal(InOutMtrix, StationSet)
myCentroids,clusterAssing = kMeansTest.pro_kMeans(CompanySet,k)
#myCentroids,clusterAssing = kMeansTest.pro_biKmeans(CompanySet,10)
#endregion

#region 将聚类结果列表clusterAssing和CompanySet组合在一起，回填数据库
for row in zip(CompanySet,clusterAssing):
    #company = session.query(CompanyTest).filter(CompanyTest.InterID==int(row[0][0,4])).first()
    row[0][0,4] = row[1][0,0]
    companysQuery.filter(CompanyTest.InterID==int(row[0][0,0])).update({CompanyTest.clusterID:int(row[1][0,0])})
    session.commit()
#endregion

nowTime = datetime.datetime.now().strftime('%Y-%m-%d')
filename = "Cluster_Result_1_use_station_test_" + nowTime


#region 统计聚类结果
Company_Statistic.CompanyStatistic(companysQuery,IndustryLabelDict,18,filename)
#endregion

#region 绘图
Map_Labeler.DrawPointMap(companysQuery, stationsQuery,filename,labelType='cluster')
#endregion

#region 绘制单个聚类的行业分布情况
SingleFigDrawing(companysQuery,stationsQuery,k)
#endregion