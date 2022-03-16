# coding=gbk
import json
from collections import Counter
from fp_growth_auto import treeNode
from fp_growth_auto import get_order_dict_N,is_all_in_sum,initTraceData,createTree,updateTree,updateHeadera,ascendTree,findPrefixPath,mineTree,createInitSet,calc_sup_and_con
# 所有的异常traceId
abnormalTrace = []
# 所有的异常trace的顶点
abnormalTraceVertex = []
# 所有的trace的顶点
traceVertex = []
# 所有的异常trace的数目
abnormalNum = 0
# 所有trace的数目
traceNum = 0
# 所有频繁集的JI分数
freq_JI = {}
top_k_freq = {}
#这是id:[所有的点名称]
abnormalTraceVertexDict={}
#这是id:{"vertexs":{},"edges":{}}
abnormalTraceInfo={}
service_set_degree={}
#某一个频繁集的所有服务的入度出度
freq_in_and_out={}


def initTraceDataC():
    for ln in open('abnormalTrace.txt', 'rt'):
        abnormalTrace.extend(ln.strip().split(' '))
        # 拿到出故障后的文件
    path = '/home/yanghong/practical/OneOperation/chaos.json'
    f = open(path)
    data = json.load(f)
    for traceId, value in data.items():
        if traceId not in abnormalTrace:
            continue
        edges=value['edges']
        vertexs = value['vertexs']
        abnormalTraceInfo[traceId] = {"vertexs": vertexs, "edges": edges}
        vertexInfo = []
        vertexSize = len(vertexs)
        for i in range(1, vertexSize):
            vertexInfo.append(vertexs[str(i)][0])
        abnormalTraceVertexDict[traceId]=vertexInfo

#一个频繁集在某一条trace中的入度出度
def calc_in_and_out(traceId,prefixList):
    traceInfo=abnormalTraceInfo[traceId]
    edges = traceInfo['edges']
    vertexs = traceInfo['vertexs']
    #出度为-，入度为+
    for startId,edgeInfo in edges:
        edgeNum=len(edgeInfo)
        if startId in freq_in_and_out:
            freq_in_and_out[startId]-=edgeNum
        else:
            freq_in_and_out[startId] = (-1) * edgeNum
        for i in range(edgeNum):
            index=str(edgeInfo[i]['vertexId'])
            if index in freq_in_and_out:
                freq_in_and_out[index]+=1
            else:
                freq_in_and_out[index] = 1
    result =0
    for key,value in freq_in_and_out:
        vertex_name=vertexs[key][0]
        if vertex_name not in prefixList:
            continue
        result+=value
    return result

#求一个频繁集的内值
def get_in_and_out_degree(traceVertex,prefixList):
    in_set_degree_num=0
    for traceId,vertex in traceVertex:
        is_all_in = True
        for prefix in prefixList:
            if vertex.find(prefix) == -1:
                is_all_in = False
                break
        if is_all_in==False:
            continue
        #计算prefixList中的每个服务在这一条trace中的入度出度和
        in_set_degree=calc_in_and_out(traceId,prefixList)
        in_set_degree_num+=in_set_degree
    JI=top_k_freq[frozenset(prefixList)]
    service_set_degree[frozenset(prefixList)]=JI*in_set_degree_num

def get_order_dict_N(_dict, N):
    result = Counter(_dict).most_common(N)
    d = {}
    for k,v in result:
        d[k] = v
    return d

if __name__ == "__main__":
    initTraceData()
    print('abnormalNum:', abnormalNum)
    print('traceNum:', traceNum)
    dataSet = abnormalTraceVertex
    print('abnormalTraceVertex:', len(abnormalTraceVertex))
    initSet = createInitSet(dataSet)
    # 任何微服务集的支持低于10%，它几乎不可能包含根因
    minsup = 0.1
    myFPTree, myheaderTable = createTree(initSet, minsup)
    # print('构建的FP树：')
    # myFPTree.displayFPTree()
    freqItems = []
    # print("显示所有的条件树")
    mineTree(myFPTree, myheaderTable, minsup, set([]), freqItems)
    print('频繁项集：\n', freqItems)
    # 计算每一个频繁项集的support和confidence以及JI并按照JI排序
    sorted_freq_JI = calc_sup_and_con(freqItems)
    # 通过JI降序排序，取top-k集。默认情况下，将k设置为100
    k = min(100, len(sorted_freq_JI))
    top_k_freq = get_order_dict_N(sorted_freq_JI, k)
    # # 打开文本文件
    # file = open('frequenceSet.txt', 'r')
    # # 遍历文本文件的每一行，strip可以移除字符串头尾指定的字符（默认为空格或换行符）或字符序列
    # for line in file.readlines():
    #     line = line.strip()
    #     k = line.split(' ')[0]
    #     v = line.split(' ')[1]
    #     print('k:', k)
    #     print('v:', v)
    #     top_k_freq[k] = float(v)
    # # 依旧是关闭文件
    # file.close()

    initTraceDataC()
    print('top_k_freq:',top_k_freq)
    for frq in top_k_freq:
        freq_in_and_out.clear()
        get_in_and_out_degree(abnormalTraceVertexDict,list(frq))
    sorted_service_set_degree=sorted(service_set_degree.items(), key=lambda d: d[1], reverse=True)
    #输出最可疑的微服务集和它的分数
    root_cause_dict=get_order_dict_N(sorted_service_set_degree,1)
    print(root_cause_dict)