# _*_ coding: utf-8 _*_
__filename__ = 'TestMain'
__author__ = 'chengtianlun'
__date__ = '2019/10/21 9:49'

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from Tool import Data_Creator,Map_Labeler
from Algorithm import kMeans
from Models import *
from TestModel import *


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

companysQuery = session.query(CompanyTest)  # 读取所有公司信息
stationsQuery = session.query(StationTest)  # 读取所有地铁站信息
in_out_sheetQuery = session.query(InOutSheetTest)  # 读取投入产出表
industry_labelQuery = session.query(IndustryLabelTest)

#region 准备数据
IndustryLabelDict = Data_Creator.EntityToDict(industry_labelQuery)
CompanySet = Data_Creator.EntityToDataSet(companysQuery,IndustryLabelDict)
StationSet = Data_Creator.EntityToDataSet(stationsQuery,{})
InOutMtrix = Data_Creator.EntityToMatrix(in_out_sheetQuery)
#endregion
#print(CompanySet)
kMeansTest = kMeans.kMeansCal(InOutMtrix, StationSet)
#temp = kMeansTest.topsisDis(CompanySet[0], CompanySet[1])
myCentroids,clusterAssing = kMeansTest.pro_kMeans(CompanySet,18)
#myCentroids,clusterAssing = kMeansTest.pro_biKmeans(CompanySet,10)

#TODO 将聚类结果列表clusterAssing和CompanySet组合在一起，回填数据库
print(myCentroids)
#print(clusterAssing)
#region 将聚类结果列表clusterAssing和CompanySet组合在一起，回填数据库
for row in zip(CompanySet,clusterAssing):
    #company = session.query(CompanyTest).filter(CompanyTest.InterID==int(row[0][0,4])).first()
    row[0][0,4] = row[1][0,0]
    session.query(CompanyTest).filter(CompanyTest.InterID==int(row[0][0,0])).update({CompanyTest.clusterID:int(row[1][0,0])})
    session.commit()
#endregion

companysQuery = session.query(CompanyTest)  # 读取所有公司信息
Map_Labeler.DrawPointMap(companysQuery, stationsQuery,"./result/Cluster_Result_05_use_station_test",labelType='cluster')
#print(StationSet)

