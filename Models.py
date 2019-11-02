# _*_ coding: utf-8 _*_
__filename__ = 'models'
__author__ = 'chengtianlun'
__date__ = '2019/10/2 18:31'

# 导入基类模块
from sqlalchemy.ext.declarative import declarative_base
# 导入字段类
from sqlalchemy import Column, Integer, String,Float

# 实体类的基类
Base = declarative_base()

# 公司实体类
class Company(Base):
    __tablename__ = 'company_info_brief'
    InterID = Column(Integer, primary_key=True, autoincrement=True)
    company_name = Column(String(255))
    company_address = Column(String(255))
    industry_field = Column(String(255))
    lng=Column(String(255))
    lat=Column(String(255))
    industry_label=Column(Integer)
    clusterID=Column(Integer)

# 地铁站实体类
class Station(Base):
    __tablename__ = 'station_info'
    StationID = Column(Integer, primary_key=True, autoincrement=True)
    StaName = Column(String(255))
    Line=Column(Integer)
    StaType=Column(Integer)
    lng=Column(String(255))
    lat=Column(String(255))

# 投入产出表实体类
class InOutSheet(Base):
    __tablename__ = 'in_out_sheet'
    Col_01 = Column(Float,primary_key=True, autoincrement=True)
    Col_02 = Column(Float)
    Col_03 = Column(Float)
    Col_04 = Column(Float)
    Col_05 = Column(Float)
    Col_06 = Column(Float)
    Col_07 = Column(Float)
    Col_08 = Column(Float)
    Col_09 = Column(Float)
    Col_10 = Column(Float)
    Col_11 = Column(Float)
    Col_12 = Column(Float)
    Col_13 = Column(Float)
    Col_14 = Column(Float)
    Col_15 = Column(Float)
    Col_16 = Column(Float)
    Col_17 = Column(Float)
    Col_18 = Column(Float)
    Col_19 = Column(Float)
    Col_20 = Column(Float)
    Col_21 = Column(Float)
    Col_22 = Column(Float)
    Col_23 = Column(Float)
    Col_24 = Column(Float)
    Col_25 = Column(Float)
    Col_26 = Column(Float)
    Col_27 = Column(Float)
    Col_28 = Column(Float)
    Col_29 = Column(Float)
    Col_30 = Column(Float)
    Col_31 = Column(Float)
    Col_32 = Column(Float)
    Col_33 = Column(Float)
    Col_34 = Column(Float)
    Col_35 = Column(Float)
    Col_36 = Column(Float)
    Col_37 = Column(Float)
    Col_38 = Column(Float)
    Col_39 = Column(Float)
    Col_40 = Column(Float)
    Col_41 = Column(Float)
    Col_42 = Column(Float)

# 行业标签实体类
class IndustryLabel(Base):
    __tablename__ = 'industry_label'
    label = Column(String(255), primary_key=True, autoincrement=True)
    f_label = Column(String(255))
    ff_label=Column(Integer)
    label_no=Column(Integer)

# 行业大类实体类
class CategoryInfo(Base):
    __tablename__ = 'category_info'
    catID = Column(Integer, primary_key=True, autoincrement=True)
    catName = Column(String(255))