# coding=gbk
import json

#这是每一条trace的所有的节点信息，是一个字典，key是traceId，value是字典，是每一个编号对应的节点的服务名和方法
traceVertexInfo={}
#这是每一条trace所有的服务对，还包括了每一对的响应时间
servicePair={}
#所有的方法
operations=['start']
#所有的调用对
invocationPair=[]
#每一对调用对的所有数据
pairData={}

#path='D:\\practical\\preprocessedNew\\abnormal.json'
def get_traceVertexInfo(path):
    #先计算历史数据，得到before数据
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
    #这个key是traceId
    for traceId, value in data.items():
        edges = value['edges']
        pairs=[]
        data=[]
        # 这个key是出发点的编号，value是所有入点的信息和这条边上的信息的集合
        for key, value in edges.items():
            startId=int(key)
            #value是一个list型，每一个元素都是一个字典
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
    #这个key是traceId
    for traceId, value in data.items():
        edges = value['edges']
        vertexs=value['vertexs']
        pairs=[]
        data=[]
        # 这个key是出发点的编号，value是所有入点的信息和这条边上的信息的集合
        for key, value in edges.items():
            if key!='0' :
                startIndex=operations.find(vertexs[key][2])
                if startIndex==-1:
                    operations.append(vertexs[key][2])
                startIndex = operations.find(vertexs[key][2])
            else:
                startIndex=0
            #value是一个list型，每一个元素都是一个字典
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
