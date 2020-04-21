# _*_ coding: utf-8 _*_
__filename__ = 'Map_Labeler'
__author__ = 'chengtianlun'
__date__ = '2019/9/30 16:36'

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
from matplotlib.patches import Polygon
from Models import Company,Station,InOutSheet
from TestModel import *

# 导入引擎模块
from sqlalchemy import create_engine
# 导入会话模块
from sqlalchemy.orm import sessionmaker

'''
绘制全部车站和企业
'''
#labelType='industry'时，按行业标记，为'cluster'时，按聚类标记
#model='single'时，只绘制某一聚类的行业分布，为'all'时，绘制全部
def DrawPointMap(companys,stations,picName='temp',labelType='industry',mode='single'):
    fig = plt.figure()
    ax1 = fig.add_axes([0.1,0.1,0.8,0.8])#[left,bottom,width,height]
    #region 绘制底图
    map = Basemap(projection='mill',lat_0=29,lon_0=109, \
                  llcrnrlat=28 ,urcrnrlat=32.5,llcrnrlon=105,urcrnrlon=111, \
                  ax=ax1,rsphere=6371200.,resolution='h',area_thresh=10000)
    # shp_info = map.readshapefile('CHN_adm/CHN_adm3','states',drawbounds=False)
    shp_info = map.readshapefile('../CHN_adm/CHN_adm3','states',drawbounds=False)
    for info, shp in zip(map.states_info, map.states):
        proid = info['NAME_1']
        if proid == 'Chongqing':
            poly = Polygon(shp,facecolor='w',edgecolor='k', lw=1.0, alpha=0.1)#注意设置透明度alpha，否则点会被地图覆盖
            ax1.add_patch(poly)

    parallels = np.arange(28.0,41.0,0.1)
    #map.drawparallels(parallels,labels=[1,0,0,0],fontsize=10) #parallels
    meridians = np.arange(105.0,110.0,0.1)
    #map.drawmeridians(meridians,labels=[0,0,0,1],fontsize=10) #meridians
    map.drawmapboundary()  #边界线
    #map.fillcontinents()
    map.drawstates()
    #map.drawcoastlines()  #海岸线
    map.drawcountries()
    map.drawcounties()
    #endregion

    #region 初始化颜色字典
    # 行业分类颜色字典
    IndustryColorDic={
        1:"#b71c1c",
        2:"#f48fb1",
        3:"#6a1b9a",
        4:"#311b92",
        5:"#536dfe",
        6:"#1a237e",
        7:"#4fc3f7",
        8:"#18ffff",
        9:"#64ffda",
        10:"#4caf50",
        11:"#b2ff59",
        12:"#9e9d24",
        13:"#ffff00",
        14:"#ffb300",
        15:"#f4511e",
        16:"#6d4c41",
        17:"#616161",
        18:"#607d8b",
    }
    # 聚类分类颜色字典
    ClusterColorDic={
        0:"#DC143C", # 猩红
        1:"#0000FF", # 纯蓝
        2:"#008000", # 纯绿
        3:"#FFFF00", # 纯黄
        4:"#536dfe",
        5:"#1a237e",
        6:"#4fc3f7",
        7:"#18ffff",
        8:"#64ffda",
        9:"#4caf50",
        10:"#b2ff59",
        11:"#9e9d24",
        12:"#ffff00",
        13:"#ffb300",
        14:"#f4511e",
        15:"#6d4c41",
        16:"#616161",
        17:"#607d8b"
    }
    #endregion

    #region 遍历所有公司信息
    temp_lat_list = []
    temp_lng_list = []
    temp_name_list = []
    for model in companys:
        #生成单行业图片
        # if(model.industry_label not in (7,)):
        #     continue
        temp_lat_list.append(model.lat)
        temp_lng_list.append(model.lng)
        temp_name_list.append(model.InterID)

    lat = np.array(temp_lat_list,dtype=float)#获取经纬度坐标
    lon = np.array(temp_lng_list,dtype=float)
    x,y = map(lon,lat)
    map.scatter(x, y,s=10,marker='.',edgecolors='none',color = 'r') #要标记的点的坐标、大小及颜色
    #endregion

    #region 公司位置标记文字
    # for i in range(len(temp_name_list)):
    #     temp_x=float(temp_lng_list[i])
    #     temp_y=float(temp_lat_list[i])
    #     temp_id = temp_name_list[i]
    #     x,y = map(temp_x,temp_y)
    #     plt.text(x,y,temp_id,fontsize=0.00005,ha='left',va='center',color='k')
    #endregion

    #region 遍历所有地铁站信息
    temp_sta_lat_list = []
    temp_sta_lng_list = []
    temp_staID_list = []
    for model in stations:
        #if model.StaType in (1,2):continue
        temp_sta_lat_list.append(model.lat)
        temp_sta_lng_list.append(model.lng)
        temp_staID_list.append(model.StationID)

    lat_sta = np.array(temp_sta_lat_list,dtype=float)#获取经纬度坐标
    lon_sta = np.array(temp_sta_lng_list,dtype=float)
    ID_sta= np.array(temp_staID_list,dtype=str)

    m,n = map(lon_sta,lat_sta)
    map.scatter(m, n, s=1, marker='.', edgecolor='b',color='w')  # 要标记的点的坐标、大小及颜色
    #endregion

    #size = (val-np.min(val)+0.05)*800#对点的数值作离散化，使得大小的显示明显
    #map.scatter(x, y,s=size,marker='.',edgecolors='none',color = 'r') #要标记的点的坐标、大小及颜色
    # for i in range(0,3):
    #     plt.text(x[i]+5000,y[i]+5000,str(val[i]))

    #region 标记文字
    # for i in range(len(temp_staID_list)):
    #     temp_x=float(temp_sta_lng_list[i])
    #     temp_y=float(temp_sta_lat_list[i])
    #     temp_id = temp_staID_list[i]
    #     x,y = map(temp_x,temp_y)
    #     plt.text(x,y,temp_id,fontsize=0.00005,ha='left',va='center',color='k')
    #endregion

    #region 生成图片
    figName = picName
    plt.title(figName)#标题
    plt.savefig('../result/'+figName+'.png', dpi=1000,bbox_inches='tight')#文件命名为Chongqing.png存储
    plt.close()
    #plt.show()
    print('picture drawing finished')
    #endregion


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

    companys = None
    stations = None
    companys = session.query(CompanyTest) #  读取所有公司信息
    stations = session.query(StationTest) #  读取所有地铁站信息
    #models = session.query(Company).get(1)
    #companys = None
    DrawPointMap(companys,stations,"Stations_and_Companys_location",mode='all')
