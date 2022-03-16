# coding=gbk
import json
import numpy as np
import math

# 这是每一条trace的所有的节点信息，是一个字典，key是traceId，value是字典，是每一个编号对应的节点的服务名和方法
traceVertexInfo = {}
# 这是所有的服务对，还包括了每一对的响应时间
servicePairData = {}
# 所有的服务对，对应的平均值和方差
calcPairData = {}
abnormalTrace=[]
delta_fs=0.1

# path='D:\\practical\\preprocessedNew\\abnormal.json'
def get_traceVertexInfo(path):
    # 先计算历史数据，得到before数据
    f = open(path)
    data = json.load(f)
    for key, value in data.items():
        data={'vertexs':value['vertexs'],'edges':value['edges']}
        traceVertexInfo[key] = data
        # break;
    f.close()


def get_servicePairData(path):
    f = open(path)
    data = json.load(f)
    # 这个key是traceId
    for traceId, value in data.items():
        edges = value['edges']
        vertexs = value['vertexs']
        # 这个key是出发点的编号，value是所有入点的信息和这条边上的信息的集合
        for key, value in edges.items():
            if key != '0':
                startOperation = vertexs[key][1]
            else:
                startOperation = 'start'
            # value是一个list型，每一个元素都是一个字典
            for i in range(len(value)):
                vertexInfo = value[i]
                vertexId = str(vertexInfo['vertexId'])
                # print(vertexId)
                if vertexId != '0':
                    endOperation = vertexs[vertexId][1]
                else:
                    endOperation = 'start'
                responseDuration = vertexInfo['responseDuration']
                startToEnd = str(startOperation) + '------' + str(endOperation)
                # print(startToEnd)
                if startToEnd in servicePairData:
                    servicePairData[startToEnd].append(responseDuration)
                else:
                    servicePairData[startToEnd] = [responseDuration]
        # break;

    f.close()

def calc_PairData():
    for key, value in servicePairData.items():
        mean = np.mean(value)
        var = np.var(value)
        np_value = np.array(value)
        # 可能会出现0/0的情况
        if var ==0 :
            np_value_process=np.zeros(len(value))
        else:
            np_value_process = np.divide(abs(np_value - mean), var)
        severity = np_value_process.tolist()
        severity_mean = np.mean(severity)
        data = {'mean': mean, 'var': var, 'severity_mean': severity_mean}
        calcPairData[key] = data
    # print(calcPairData)


def get_abnormalTrace(path):
    f = open(path)
    data = json.load(f)
    # 这个key是traceId
    for traceId, value in data.items():
        edges = value['edges']
        vertexs = value['vertexs']
        abnormal=False
        # 这个key是出发点的编号，value是所有入点的信息和这条边上的信息的集合
        for key, value in edges.items():
            if key != '0':
                startOperation = vertexs[key][1]
            else:
                startOperation = 'start'
            # value是一个list型，每一个元素都是一个字典，list中每一个元素都是一条边的信息
            for i in range(len(value)):
                vertexInfo = value[i]
                vertexId = str(vertexInfo['vertexId'])
                # print(vertexId)
                if vertexId != '0':
                    endOperation = vertexs[vertexId][1]
                else:
                    endOperation = 'start'
                responseDuration = vertexInfo['responseDuration']
                startToEnd = str(startOperation) + '------' + str(endOperation)
                #计算出现故障之后的异常情况
                if startToEnd in calcPairData:
                    data=calcPairData[startToEnd]
                    mean=data['mean']
                    var=data['var']
                    severity=data['severity_mean']
                    if var==0:
                        s=0
                    else:
                        s=np.divide(abs(responseDuration - mean), var)
                    # if s-severity>delta_fs*severity:
                    if s>1:
                        abnormalTrace.append(traceId)
                        abnormal=True
                        # 这条trace只要有一个调用对是异常那么就把整条trace都认为是异常
                        break
                    else:
                        continue
            if abnormal==True:
                break
        # break;

    f.close()

if __name__ == "__main__":
    # 对于正常数据
    normalpath='/home/yanghong/practical/OneOperation/normal.json'
    get_traceVertexInfo(normalpath)
    # print(traceVertexInfo)
    get_servicePairData(normalpath)
    # file = open('dict.txt', 'w')
    # for k, v in servicePairData.items():
    #     file.write(str(k) + ' ' + str(v) + '\n')
    # file.close()
    calc_PairData()

    # 对于异常数据
    abnormalpath = '/home/yanghong/practical/OneOperation/chaos.json'
    get_abnormalTrace(abnormalpath)
    file = open('abnormalTrace.txt', 'w')
    for trace in abnormalTrace:
        file.write(trace + '\n')
    file.close()