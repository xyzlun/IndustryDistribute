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


stationsQuery = session.query(StationTest)  # 读取所有地铁站信息

for i in range(15):
    companysQuery = session.query(CompanyTest) .filter(CompanyTest.clusterID==i)
    fileName = "./result/Cluster_"+str(i)+"_Result_industry_label"
    #region 对某一聚类的行业分布
    Map_Labeler.DrawPointMap(companysQuery, stationsQuery,fileName,labelType='industry')
    print('Cluster '+str(i)+' is finish')
    #endregion
print('finish!')

companysQuery = session.query(CompanyTest).filter(CompanyTest.clusterID == 14)
fileName = "./result/Cluster_" + str(14) + "_Result_industry_label"
# region 对某一聚类的行业分布
Map_Labeler.DrawPointMap(companysQuery, stationsQuery, fileName, labelType='industry')