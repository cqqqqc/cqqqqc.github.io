# coding=gbk

import json

abnormalTrace = []
for ln in open('abnormalTrace.txt', 'rt'):
    abnormalTrace.extend(ln.strip().split(' '))
abnormalNum=len(abnormalTrace)

traceVertex=[]
path = 'D:\\practical\\preprocessedNew\\normal.json'
f = open(path)
data = json.load(f)
for traceId, value in data.items():
    vertexs = value['vertexs']
    vertexInfo=[]
    vertexSize=len(vertexs)
    for i in range(1,vertexSize):
        vertexInfo.append(vertexs[str(i)][1])
    traceVertex.append(vertexInfo)
f.close()

#所有trace中经过某个list所有服务的数量
def is_all_in_sum(prefixList):
    all_in_num=0
    for trace in traceVertex:
        is_all_in = True
        for prefix in prefixList:
            if trace.find(prefix) == -1:
                is_all_in = False
                break
        if is_all_in==True:
            all_in_num+=1
    return all_in_num




