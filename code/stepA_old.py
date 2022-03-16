# coding=gbk
import json

#����ÿһ��trace�����еĽڵ���Ϣ����һ���ֵ䣬key��traceId��value���ֵ䣬��ÿһ����Ŷ�Ӧ�Ľڵ�ķ������ͷ���
traceVertexInfo={}
#����ÿһ��trace���еķ���ԣ���������ÿһ�Ե���Ӧʱ��
servicePair={}
#���еķ���
operations=['start']
#���еĵ��ö�
invocationPair=[]
#ÿһ�Ե��öԵ���������
pairData={}

#path='D:\\practical\\preprocessedNew\\abnormal.json'
def get_traceVertexInfo(path):
    #�ȼ�����ʷ���ݣ��õ�before����
    f = open(path)
    data = json.load(f)
    for key, value in data.items():
        traceVertexInfo[key] = value['vertexs']
        # print(traceVertexInfo)
        # break;
    f.close()

def get_servicePair(path):
    f = open(path)
    data = json.load(f)
    #���key��traceId
    for traceId, value in data.items():
        edges = value['edges']
        pairs=[]
        data=[]
        # ���key�ǳ�����ı�ţ�value������������Ϣ���������ϵ���Ϣ�ļ���
        for key, value in edges.items():
            startId=int(key)
            #value��һ��list�ͣ�ÿһ��Ԫ�ض���һ���ֵ�
            for i in range(len(value)):
                vertexInfo=value[i]
                vertexId=vertexInfo['vertexId']
                responseDuration=vertexInfo['responseDuration']
                pairs.append([startId,vertexId])
                data.append(responseDuration)
        servicePairInfo={'pairs':pairs,'data':data}
        servicePair[traceId]=servicePairInfo
        # print(servicePair)
        # break;

    f.close()

def get_servicePairData(path):
    f = open(path)
    data = json.load(f)
    #���key��traceId
    for traceId, value in data.items():
        edges = value['edges']
        vertexs=value['vertexs']
        pairs=[]
        data=[]
        # ���key�ǳ�����ı�ţ�value������������Ϣ���������ϵ���Ϣ�ļ���
        for key, value in edges.items():
            if key!='0' :
                startIndex=operations.find(vertexs[key][2])
                if startIndex==-1:
                    operations.append(vertexs[key][2])
                startIndex = operations.find(vertexs[key][2])
            else:
                startIndex=0
            #value��һ��list�ͣ�ÿһ��Ԫ�ض���һ���ֵ�
            for i in range(len(value)):
                vertexInfo=value[i]
                vertexId=str(vertexInfo['vertexId'])
                if vertexId != '0':
                    endIndex = operations.find(vertexs[vertexId][2])
                    if endIndex==-1:
                        operations.append(vertexs[vertexId][2])
                    endIndex = operations.find(vertexs[vertexId][2])
                else:
                    endIndex = 0
                responseDuration=vertexInfo['responseDuration']
                startToEnd=str(startIndex)+'-'+str(endIndex)
                if invocationPair.find(startToEnd)==-1:
                    invocationPair.append(startToEnd)
                servicePair[startToEnd].append(responseDuration)
        servicePairInfo={'pairs':pairs,'data':data}
        servicePair[traceId]=servicePairInfo
        # print(servicePair)
        # break;

    f.close()

if __name__=="__main__":
    path = 'D:\\practical\\preprocessedNew\\abnormal.json'
    # get_traceVertexInfo(path)
    # print(traceVertexInfo)
    get_servicePair(path)
    print(servicePair)
