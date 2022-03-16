# coding=gbk
import json
from collections import Counter
from fp_growth_auto import treeNode
from fp_growth_auto import get_order_dict_N,is_all_in_sum,initTraceData,createTree,updateTree,updateHeadera,ascendTree,findPrefixPath,mineTree,createInitSet,calc_sup_and_con
# ���е��쳣traceId
abnormalTrace = []
# ���е��쳣trace�Ķ���
abnormalTraceVertex = []
# ���е�trace�Ķ���
traceVertex = []
# ���е��쳣trace����Ŀ
abnormalNum = 0
# ����trace����Ŀ
traceNum = 0
# ����Ƶ������JI����
freq_JI = {}
top_k_freq = {}
#����id:[���еĵ�����]
abnormalTraceVertexDict={}
#����id:{"vertexs":{},"edges":{}}
abnormalTraceInfo={}
service_set_degree={}
#ĳһ��Ƶ���������з������ȳ���
freq_in_and_out={}


def initTraceDataC():
    for ln in open('abnormalTrace.txt', 'rt'):
        abnormalTrace.extend(ln.strip().split(' '))
        # �õ������Ϻ���ļ�
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

#һ��Ƶ������ĳһ��trace�е���ȳ���
def calc_in_and_out(traceId,prefixList):
    traceInfo=abnormalTraceInfo[traceId]
    edges = traceInfo['edges']
    vertexs = traceInfo['vertexs']
    #����Ϊ-�����Ϊ+
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

#��һ��Ƶ��������ֵ
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
        #����prefixList�е�ÿ����������һ��trace�е���ȳ��Ⱥ�
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
    # �κ�΢���񼯵�֧�ֵ���10%�������������ܰ�������
    minsup = 0.1
    myFPTree, myheaderTable = createTree(initSet, minsup)
    # print('������FP����')
    # myFPTree.displayFPTree()
    freqItems = []
    # print("��ʾ���е�������")
    mineTree(myFPTree, myheaderTable, minsup, set([]), freqItems)
    print('Ƶ�����\n', freqItems)
    # ����ÿһ��Ƶ�����support��confidence�Լ�JI������JI����
    sorted_freq_JI = calc_sup_and_con(freqItems)
    # ͨ��JI��������ȡtop-k����Ĭ������£���k����Ϊ100
    k = min(100, len(sorted_freq_JI))
    top_k_freq = get_order_dict_N(sorted_freq_JI, k)
    # # ���ı��ļ�
    # file = open('frequenceSet.txt', 'r')
    # # �����ı��ļ���ÿһ�У�strip�����Ƴ��ַ���ͷβָ�����ַ���Ĭ��Ϊ�ո���з������ַ�����
    # for line in file.readlines():
    #     line = line.strip()
    #     k = line.split(' ')[0]
    #     v = line.split(' ')[1]
    #     print('k:', k)
    #     print('v:', v)
    #     top_k_freq[k] = float(v)
    # # �����ǹر��ļ�
    # file.close()

    initTraceDataC()
    print('top_k_freq:',top_k_freq)
    for frq in top_k_freq:
        freq_in_and_out.clear()
        get_in_and_out_degree(abnormalTraceVertexDict,list(frq))
    sorted_service_set_degree=sorted(service_set_degree.items(), key=lambda d: d[1], reverse=True)
    #�������ɵ�΢���񼯺����ķ���
    root_cause_dict=get_order_dict_N(sorted_service_set_degree,1)
    print(root_cause_dict)