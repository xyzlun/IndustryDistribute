# _*_ coding: utf-8 _*_
__filename__ = 'TestMain'
__author__ = 'chengtianlun'
__date__ = '2019/10/21 9:49'

import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from collections import Counter

from Tool import Data_Creator,Map_Labeler
from Algorithm import kMeans
from Models import *
from TestModel import *

def SingleFigDrawing(companysQuery, stationsQuery,k):

    for i in range(k):
        #统计出属于行业数量最高的10个行业的企业
        input_companysQuery = companysQuery.filter(CompanyTest.clusterID==i)
        cluster_label = input_companysQuery.with_entities(CompanyTest.industry_label)
        temp_list = []
        # cluster_label是行业标签构成的列表，里面的元素均为tuple
        for item in cluster_label:
            temp_list.append(item[0])

        #数量前十的行业
        label_list = []
        ElemCounter = Counter(temp_list).most_common(10)
        for var in ElemCounter:
            label_list.append(var[0])

        #筛选出属于数量前十的企业query
        top10_companysQuery = input_companysQuery.filter(CompanyTest.industry_label.in_(label_list))
        nowTime = datetime.datetime.now().strftime('%Y-%m-%d')
        fileName = "Cluster_"+str(i)+"_Result_industry_label_"+nowTime
        #region 对某一聚类的行业分布
        Map_Labeler.DrawPointMap(top10_companysQuery, stationsQuery,fileName,labelType='industry')
        print('Cluster '+str(i)+' is finished')
        #endregion
    print('Single Fig Draw finished')



if __name__=='__main__':
    # 创建连接引擎
    host = 'localhost'
    port = 3306
    username = 'root'
    password = 'password'
    db = 'qcc_data'
    connect_str = 'mysql+mysqlconnector://{}:{}@{}:{}/{}'.format(username, password, host, port, db)

    engine = create_engine(connect_str, echo=True)
    Session = sessionmaker(bind=engine)
    session = Session()

    k=18
    companysQuery = session.query(CompanyTest)
    stationsQuery = session.query(StationTest)  # 读取所有地铁站信息
    SingleFigDrawing(companysQuery,stationsQuery,k)

    # 对某一聚类的行业分布
    # companysQuery = session.query(CompanyTest).filter(CompanyTest.clusterID == 14).all()
    # ElemCounter = Counter(companysQuery).most_common(10)
    # fileName = "Cluster_" + str(14) + "_Result_industry_label"
    # Map_Labeler.DrawPointMap(companysQuery, stationsQuery, fileName, labelType='industry')