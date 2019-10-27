# _*_ coding: utf-8 _*_
__filename__ = 'kMeans'
__author__ = 'chengtianlun'
__date__ = '2019/10/17 21:48'

from numpy import *
from random import sample
from collections import Counter

class kMeansCal():
    def __init__(self,InOutMtrix,StationSet):
        self.distMax = 2196.936200645564  # 假设距离最大值
        self.distMin = 0.0  # 假设距离最小值
        self.relMin = 0.000113  # 完全消耗系数最小值
        self.relMax = 1.056232  # 完全消耗系数最大值
        self.InOutMatrix = InOutMtrix
        self.StationSet = StationSet


    # 文本导入函数
    @staticmethod
    def loadDataSet(fileName):
        dataMat = []
        fr = open(fileName)
        for line in fr.readlines():
            curLine = line.strip().split('\t')
            fltLine=[]
            for item in map(float,curLine):
                fltLine.append(item)
            dataMat.append(fltLine)
        #print(dataMat)
        return dataMat

    # 距离欧式计算函数
    @staticmethod
    def distEclud(vecA,vecB):
        return sqrt(sum(power(vecA[0,1:3]-vecB[0,1:3],2)))

    # 利用地铁站作为质心 TODO 未完成，需要考虑将车站构建为公司的结构需要虚拟的数值
    def stationRandcent(self,dataSet,k):
        '''
        选择质心时，将所有的终点站和换乘站作为质心，即StationSet中StaType为0、2、3的站
        '''
        n = shape(dataSet)[1]  # company数据的列数
        centroids = mat(zeros((k,n)))
        tempStaList = []  # 所有非区间站
        for station in self.StationSet:
            if station[0,1] in (1,2): continue
            cenLine = [0,station[0,2],station[0,3],29,0]  # 地铁站作为质心，其投入产出分类ID为-1，聚类ID为0
            tempStaList.append(cenLine)
        terminalSta = mat(tempStaList)

        if k < shape(terminalSta)[0]:
            centroids = mat(sample(terminalSta.tolist(),k))
        else:
            for j in range(shape(terminalSta)[0]):
                centroids[j,:] = terminalSta[j,:]

        print('initial centroids:')
        print(centroids)
        return centroids

    # Topsis方法确定广义距离
    # TODO 考虑这样的改进方法：产业相关性的计算，应为某个簇出现频率较高的几个产业之间的相关性
    def topsisDis(self,vecA,vecB,numList):
        '''
        :param vecA: 质心
        :param vecB: 当前点
        :param numList: 质心所在簇出现次数前三多的行业
        :return: 广义距离
        '''
        dist=0.0
        rel_input_list = []  # 当前点与前三行业的投入相关系数列表
        rel_output_list = []  # 当前点与前三行业的产出相关系数列表

        #SlcDist = self.distSLC(vecA[0,1:3],vecB[0,1:3])  # 计算球面距离

        a = sin(vecA[0,2]*pi/180) * sin(vecB[0,2]*pi/180)
        b = cos(vecA[0,2]*pi/180) * cos(vecB[0,2]*pi/180) * \
        cos(pi * (vecB[0,1]-vecA[0,1]) /180)
        SlcDist = arccos(a + b)*6371.0

        dist_min = sqrt(power(SlcDist-self.distMin,2))
        dist_max = sqrt(power(SlcDist-self.distMax,2))
        dist = dist_min/(dist_min+dist_max)  # 计算Topsis处理后的距离

        for pair in numList:
            inputIndex = self.InOutMatrix[int(vecB[0,3]),int(pair[0])]  # 投入vecA产出vecB
            input_min = sqrt(power(inputIndex-self.relMin,2))
            input_max = sqrt(power(inputIndex-self.relMax,2))
            rel_input_list.append(input_min/(input_min+input_max))

            outputIndex = self.InOutMatrix[int(pair[0]),int(vecB[0,3])]  # 投入vecB产出vecA
            output_min = sqrt(power(outputIndex-self.relMin,2))
            output_max = sqrt(power(outputIndex-self.relMax,2))
            rel_output_list.append(output_min/(output_min+output_max))

        if numList == []:
            mean_rel_input = 0
            mean_rel_output = 0
            total_rel_index = 0  # 加入结果中的产业相关性
        else:
            mean_rel_input = mean(rel_input_list)  # 投入相关系数平均值
            mean_rel_output = mean(rel_output_list)  # 产出相关系数平均值
            total_rel_index = 1 / (mean_rel_input + mean_rel_output)  # 加入结果中的产业相关性
        result = dist + total_rel_index
        #result = dist
        return  result # 因为rel_input和rel_output越大越好，所以应取反

    # 球面距离计算
    @staticmethod
    def distSLC(vecA, vecB):
        a = sin(vecA[0,2]*pi/180) * sin(vecB[0,2]*pi/180)
        b = cos(vecA[0,2]*pi/180) * cos(vecB[0,2]*pi/180) * \
                        cos(pi * (vecB[0,1]-vecA[0,1]) /180)
        return arccos(a + b)*6371.0

    # 创建随机质心
    def randCent(self,dataSet,k):
        n = shape(dataSet)[1]
        centroids = mat(zeros((k,n)))
        for j in range(n):
            minJ = min(dataSet[:,j])
            rangeJ = float(max(dataSet[:,j])-minJ)
            centroids[:,j]=minJ+rangeJ*random.rand(k,1)
        print('initial centroids')
        print(centroids)
        return centroids

    # 常规K-均值聚类算法
    def kMeans(self,dataSet,k,distMeas=distEclud,creatCent=randCent):
        m = shape(dataSet)[0]
        clusterAssment = mat(zeros((m,2)))
        centroids = creatCent(dataSet,k)
        clusterChanged = True

        while clusterChanged:
            clusterChanged = False
            for i in range(m):
                minDist = inf  # 正无穷
                minIndex = -1
                for j in range(k):
                    distJI = distMeas(centroids[j,:],dataSet[i,:])
                    if distJI < minDist:
                        minDist = distJI
                        minIndex = j
                if clusterAssment[i,0] != minIndex:
                    clusterChanged = True
                # clusterAssment有两列，第一列为对应dataSet中的点被划归到哪个簇的索引，第二列为误差
                clusterAssment[i,:] = minIndex,minDist**2
            print(centroids)
            for cent in range(k):
                ptsInClust = dataSet[nonzero(clusterAssment[:,0].A==cent)[0]]  # 取出以cent为质心的所有坐标
                centroids[cent,:] = mean(ptsInClust,axis=0)  # 对上面一步取出的坐标求平均值，作为新的质心
        return centroids,clusterAssment

    # 常规二分K-均值聚类算法
    def biKmeans(self,dataSet, k, distMeas=distEclud):
        m = shape(dataSet)[0]
        clusterAssment = mat(zeros((m,2)))
        centroid0 = mean(dataSet, axis=0).tolist()[0]
        centList =[centroid0] #create a list with one centroid
        for j in range(m):#calc initial Error
            clusterAssment[j,1] = distMeas(mat(centroid0), dataSet[j,:])**2
        while (len(centList) < k):
            lowestSSE = inf
            for i in range(len(centList)):
                ptsInCurrCluster = dataSet[nonzero(clusterAssment[:,0].A==i)[0],:]#get the data points currently in cluster i
                centroidMat, splitClustAss = self.kMeans(ptsInCurrCluster, 2, distMeas)
                sseSplit = sum(splitClustAss[:,1])#compare the SSE to the currrent minimum
                sseNotSplit = sum(clusterAssment[nonzero(clusterAssment[:,0].A!=i)[0],1])
                print("sseSplit, and notSplit: ",sseSplit,sseNotSplit)
                if (sseSplit + sseNotSplit) < lowestSSE:
                    bestCentToSplit = i
                    bestNewCents = centroidMat
                    bestClustAss = splitClustAss.copy()
                    lowestSSE = sseSplit + sseNotSplit
            bestClustAss[nonzero(bestClustAss[:,0].A == 1)[0],0] = len(centList) #change 1 to 3,4, or whatever
            bestClustAss[nonzero(bestClustAss[:,0].A == 0)[0],0] = bestCentToSplit
            print('the bestCentToSplit is: ',bestCentToSplit)
            print('the len of bestClustAss is: ', len(bestClustAss))
            centList[bestCentToSplit] = bestNewCents[0,:].tolist()[0]#replace a centroid with two best centroids
            centList.append(bestNewCents[1,:].tolist()[0])
            clusterAssment[nonzero(clusterAssment[:,0].A == bestCentToSplit)[0],:]= bestClustAss#reassign new clusters, and SSE
        return mat(centList), clusterAssment

    # 改进的常规K-均值聚类算法
    def pro_kMeans(self,dataSet,k,distMeas=topsisDis,creatCent=stationRandcent):
        m = shape(dataSet)[0]
        clusterAssment = mat(zeros((m,2)))
        centroids = creatCent(self,dataSet,k)
        clusterChanged = True
        while clusterChanged:
            clusterChanged = False
            for i in range(m):
                minDist = inf  # 正无穷
                minIndex = -1
                for j in range(k):
                    # TODO 统计簇中出现频次最高的三个类别，计算距离的时候应计算当前点与前三的类别的相关性
                    # 取出以j为质心的所有坐标的分类ID
                    currentClust = dataSet[nonzero(clusterAssment[:,0].A==j)[0]][:,3].getA().tolist()
                    temp_list = []

                    # 将currentClust转化成可迭代list
                    for x in currentClust:
                        for y in x:
                            temp_list.append(y)
                    #建立计数器，统计目前以j为质心的簇出现前三多的行业分类ID
                    ElemCounter = Counter(temp_list)
                    numTop3 =  ElemCounter.most_common(3)  # 出现次数前三多的列表，其中元素为tuple

                    #距离函数
                    #distJI = distMeas(self,centroids[j,:],dataSet[i,:],numTop3)
                    distJI = kMeansCal.distSLC(centroids[j,:],dataSet[i,:])
                    #distJI = kMeansCal.distEclud(centroids[j,:],dataSet[i,:])

                    if distJI < minDist:
                        minDist = distJI
                        minIndex = j
                #print('curent assment:')
                currentAssmentIndex = clusterAssment[i,0]
                #print(currentAssmentIndex)
                if clusterAssment[i,0] != minIndex:
                    # print('change to:')
                    # print(minIndex)
                    clusterChanged = True
                # clusterAssment有两列，第一列为对应dataSet中的点被划归到哪个簇的索引，第二列为误差
                clusterAssment[i,:] = minIndex,minDist**2

            #region 簇分配监视器
            templist = []
            for item in clusterAssment.tolist():
                templist.append(item[0])
            ElemCounter = Counter(templist)
            #endregion

            for cent in range(k):
                ptsInClust = dataSet[nonzero(clusterAssment[:,0].A==cent)[0]]  # 取出以cent为质心的所有坐标
                centroids[cent,:] = mean(ptsInClust,0)  # 对上面一步取出的坐标求平均值，作为新的质心
            print('更新后的质心为：')
            print(centroids)
        return centroids,clusterAssment

    # 改进的二分K-均值聚类算法
    def pro_biKmeans(self,dataSet,k):
        m = shape(dataSet)[0]
        clusterAssment = mat(zeros((m,2)))
        centroid0 = mean(dataSet, axis=0).tolist()[0]
        centList =[centroid0] #create a list with one centroid
        for j in range(m):#calc initial Error
            clusterAssment[j,1] = kMeansCal.distSLC(mat(centroid0), dataSet[j,:])**2
        while (len(centList) < k):
            lowestSSE = inf
            for i in range(len(centList)):
                ptsInCurrCluster = dataSet[nonzero(clusterAssment[:,0].A==i)[0],:]#get the data points currently in cluster i
                centroidMat, splitClustAss = self.pro_kMeans(ptsInCurrCluster,2)
                sseSplit = sum(splitClustAss[:,1])#compare the SSE to the currrent minimum
                sseNotSplit = sum(clusterAssment[nonzero(clusterAssment[:,0].A!=i)[0],1])
                print("sseSplit, and notSplit: ",sseSplit,sseNotSplit)
                if (sseSplit + sseNotSplit) < lowestSSE:
                    bestCentToSplit = i
                    bestNewCents = centroidMat
                    bestClustAss = splitClustAss.copy()
                    lowestSSE = sseSplit + sseNotSplit
            bestClustAss[nonzero(bestClustAss[:,0].A == 2)[0],0] = len(centList) #change 1 to 3,4, or whatever
            bestClustAss[nonzero(bestClustAss[:,0].A == 0)[0],0] = bestCentToSplit
            print('the bestCentToSplit is: ',bestCentToSplit)
            print('the len of bestClustAss is: ', len(bestClustAss))
            centList[bestCentToSplit] = bestNewCents[0,:].tolist()[0]#replace a centroid with two best centroids
            centList.append(bestNewCents[1,:].tolist()[0])
            clusterAssment[nonzero(clusterAssment[:,0].A == bestCentToSplit)[0],:]= bestClustAss#reassign new clusters, and SSE
        return mat(centList), clusterAssment

if __name__=='__main__':
    # temp = None
    # kmeans = kMeansCal(temp,temp)
    datMat = mat(kMeansCal.loadDataSet('../testSet3.txt'))
    #print(min(datMat[:,1]))
    #print(datMat)
    # print(max(datMat[0,:]))
    # print(min(datMat[1,:]))
    # print(max(datMat[1,:]))
    #print(datMat[0])
    #print(datMat[0,:])
    # ptsInClust=datMat[nonzero(datMat[:,0].A==4)[0]][:,2].getA().tolist()
    # temp_list = []
    # for m in ptsInClust:
    #     for n in m:
    #         temp_list.append(n)
    # print(temp_list)
    # ElemCounter = Counter(temp_list)
    # num =  ElemCounter.most_common(3)
    # print(num)
    # print(num[1][0])
    #a=mean([1,2,3])

    #print(kMeansCal.distSLC(matrix([123.77461422409242,41.301604181773878]),matrix([105.43235863588306,28.388416756327588])))
    #print(distEclud(matrix([datMat[0,0],datMat[0,1],datMat[0,2]]),matrix([datMat[1,0],datMat[1,1],datMat[1,2]])))
    #myCentroids,clusterAssing = kmeans.kMeans(datMat,3)
    #print(clusterAssing)
    #myCentroids,clusterAssing = biKmeans(datMat,4)


