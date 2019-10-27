# _*_ coding: utf-8 _*_
__filename__ = 'Industry_Classifier'
__author__ = 'chengtianlun'
__date__ = '2019/10/2 20:21'

from Models import Company

# 导入引擎模块
from sqlalchemy import create_engine
# 导入会话模块
from sqlalchemy.orm import sessionmaker


def Industry_Classify(models):
    pass



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

    models = session.query(Company)
    Industry_Classify(models)