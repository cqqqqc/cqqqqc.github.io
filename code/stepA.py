# coding=gbk
import json
import numpy as np
import math

# ����ÿһ��trace�����еĽڵ���Ϣ����һ���ֵ䣬key��traceId��value���ֵ䣬��ÿһ����Ŷ�Ӧ�Ľڵ�ķ������ͷ���
traceVertexInfo = {}
# �������еķ���ԣ���������ÿһ�Ե���Ӧʱ��
servicePairData = {}
# ���еķ���ԣ���Ӧ��ƽ��ֵ�ͷ���
calcPairData = {}
abnormalTrace=[]
delta_fs=0.1

# path='D:\\practical\\preprocessedNew\\abnormal.json'
def get_traceVertexInfo(path):
    # �ȼ�����ʷ���ݣ��õ�before����
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
    # ���key��traceId
    for traceId, value in data.items():
        edges = value['edges']
        vertexs = value['vertexs']
        # ���key�ǳ�����ı�ţ�value������������Ϣ���������ϵ���Ϣ�ļ���
        for key, value in edges.items():
            if key != '0':
                startOperation = vertexs[key][1]
            else:
                startOperation = 'start'
            # value��һ��list�ͣ�ÿһ��Ԫ�ض���һ���ֵ�
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
        # ���ܻ����0/0�����
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
    # ���key��traceId
    for traceId, value in data.items():
        edges = value['edges']
        vertexs = value['vertexs']
        abnormal=False
        # ���key�ǳ�����ı�ţ�value������������Ϣ���������ϵ���Ϣ�ļ���
        for key, value in edges.items():
            if key != '0':
                startOperation = vertexs[key][1]
            else:
                startOperation = 'start'
            # value��һ��list�ͣ�ÿһ��Ԫ�ض���һ���ֵ䣬list��ÿһ��Ԫ�ض���һ���ߵ���Ϣ
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
                #������ֹ���֮����쳣���
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
                        # ����traceֻҪ��һ�����ö����쳣��ô�Ͱ�����trace����Ϊ���쳣
                        break
                    else:
                        continue
            if abnormal==True:
                break
        # break;

    f.close()

if __name__ == "__main__":
    # ������������
    normalpath='/home/yanghong/practical/OneOperation/normal.json'
    get_traceVertexInfo(normalpath)
    # print(traceVertexInfo)
    get_servicePairData(normalpath)
    # file = open('dict.txt', 'w')
    # for k, v in servicePairData.items():
    #     file.write(str(k) + ' ' + str(v) + '\n')
    # file.close()
    calc_PairData()

    # �����쳣����
    abnormalpath = '/home/yanghong/practical/OneOperation/chaos.json'
    get_abnormalTrace(abnormalpath)
    file = open('abnormalTrace.txt', 'w')
    for trace in abnormalTrace:
        file.write(trace + '\n')
    file.close()