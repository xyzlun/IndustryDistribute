# _*_ coding: utf-8 _*_
__filename__ = 'Start'
__author__ = 'chengtianlun'
__date__ = '2019/10/19 17:29'

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from Tool import Data_Creator
from Algorithm import kMeans
from Models import *
from TestModel import *

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

companysQuery = session.query(Company)  # 读取所有公司信息
stationsQuery = session.query(Station)  # 读取所有地铁站信息
in_out_sheetQuery = session.query(InOutSheet)  # 读取投入产出表
industry_labelQuery = session.query(IndustryLabel)

#region 准备数据
IndustryLabelDict = Data_Creator.EntityToDict(industry_labelQuery)
CompanySet = Data_Creator.EntityToDataSet(companysQuery,IndustryLabelDict)
StationSet = Data_Creator.EntityToDataSet(stationsQuery,{})
InOutMtrix = Data_Creator.EntityToMatrix(in_out_sheetQuery)
#endregion

#TODO
kMeans = kMeans.kMeansCal(InOutMtrix, StationSet)
myCentroids,clusterAssing = kMeans.pro_kMeans(CompanySet,2)
#Map_Labeler.DrawPointMap(companys, stations)
print(StationSet)
