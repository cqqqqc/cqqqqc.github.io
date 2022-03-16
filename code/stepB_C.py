# coding=gbk
import json
from collections import Counter

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
# 这是id:[所有的点名称]
abnormalTraceVertexDict = {}
# 这是id:{"vertexs":{},"edges":{}}
abnormalTraceInfo = {}
service_set_degree = {}
# 某一个频繁集的所有服务的入度出度
freq_in_and_out = {}


class treeNode:
    # """FP树的类定义"""
    def __init__(self, nameValue, numOccur, parentNode):
        self.name = nameValue  # 存放节点的名字
        self.count = numOccur  # 计数值
        self.nodeLink = None  # 用于链接相似的元素项
        self.parent = parentNode  # 指向当前节点的父节点
        self.children = {}  # 当前节点的子节点

    def inc(self, numOccur):
        # """对count变量增加给定值"""
        self.count += numOccur

    def displayFPTree(self, ind=1):
        # """将树以文本形式显示出来"""
        print("  " * ind, self.name, "  ", self.count)
        for child in self.children.values():
            child.displayFPTree(ind + 1)


def get_order_dict_N(_dict, N):
    result = Counter(_dict).most_common(N)
    print('result:',result)
    d = {}
    for k in result:
        d[k[0][0]] = k[0][1]
    # for k, v in result:
    #     print('k:',k)
    #     print('v:',v)
    #     d[k] = v
    return d


# 所有trace中经过某个list所有服务的数量
def is_all_in_sum(traceList, prefixList):
    all_in_num = 0
    for trace in traceList:
        # print('trace')
        # print(trace)
        is_all_in = True
        for prefix in prefixList:
            # print('prefix')
            # print(prefix)
            if prefix not in trace:
                is_all_in = False
                break
        if is_all_in == True:
            all_in_num += 1
    return all_in_num


def initTraceData():
    for ln in open('abnormalTrace.txt', 'rt'):
        abnormalTrace.extend(ln.strip().split(' '))
    global abnormalNum
    abnormalNum = len(abnormalTrace)
    print('函数内abnormalNum:', abnormalNum)
    # 拿到出故障后的文件
    # path = 'D:\\practical\\OneOperation\\chaos.json'
    path = '/home/yanghong/practical/OneOperation/chaos.json'
    f = open(path)
    data = json.load(f)
    global traceNum
    traceNum = len(data)
    for traceId, value in data.items():
        vertexs = value['vertexs']
        vertexInfo = []
        vertexSize = len(vertexs)
        for i in range(1, vertexSize):
            vertexInfo.append(vertexs[str(i)][0])
            # vertexInfo.append(vertexs[str(i)][1])
        traceVertex.append(vertexInfo)
        if traceId in abnormalTrace:
            abnormalTraceVertex.append(vertexInfo)
    f.close()


# FP树构建函数
def createTree(dataSet, minsup=1):
    print('----------------------------------------------------------------')
    # """构建FP树，其中输入的数据集dataSet是字典类型"""
    # 对数据集进行第一次扫描，统计每个元素项出现的频率，将结果存在头指针表中
    headerTable = {}
    # print('dataset:')
    # print(dataSet)
    for trans in dataSet:
        print('trans:')
        print(trans)
        for item in trans:
            print('item:')
            print(item)
            headerTable[item] = dataSet[trans]
            # headerTable[item] = headerTable.get(item, 0) + dataSet[trans]
    print('headerTable:')
    print(headerTable)
    # 去掉头指针表中出现次数小于最小支持度阈值的项
    for item in list(headerTable.keys()):
        if headerTable[item] < minsup:
            del (headerTable[item])
    freqItemSet = set(headerTable.keys())  # 获取频繁项
    print('createTree返回值headerTable:')
    print(headerTable)
    # 如果没有元素项满足要求，则退出
    if len(freqItemSet) == 0:
        return None, None

    # 对头指针表进行扩展，以便可以保存计数值和指向每种类型第一个元素项的指针
    for item in headerTable:
        temp = [headerTable[item], None]
        headerTable[item] = temp
    # 创建只包含空集合的根节点
    retTree = treeNode('Null Set', 1, None)
    # 对数据集进行第二次扫描，构建FP树
    for trans, count in dataSet.items():
        localD = {}
        # 对该项集进行过滤
        for item in trans:
            if item in freqItemSet:  # 仅考虑频繁项
                localD[item] = headerTable[item][0]
        # 对该项集进行排序，按元素的频率来排序,如果两元素在频次相同按字母顺序排序
        if len(localD) > 0:
            # ord() 函数是以一个字符（长度为1的字符串）作为参数，返回对应的十进制ASCII数值，比如：ord('a') 返回97  ord('b') 返回98
            # 如果都是数字 -ord(p[0]) 改为 int(p[0])
            orderedItems = [v[0] for v in sorted(localD.items(), key=lambda p: p[1], reverse=True)]
            updateTree(orderedItems, retTree, headerTable, count)
    print('createTree返回值headerTable:')
    print(headerTable)
    return retTree, headerTable


def updateTree(items, inTree, headerTable, count):
    # """更新FP树，让FP树生长"""
    # 判断项集中第一个元素项是否作为子节点存在，如果存在，更新该元素项的计数
    if items[0] in inTree.children:
        inTree.children[items[0]].inc(count)
    else:  # 不存在，则创建新的节点，并作为子节点添加到树中
        inTree.children[items[0]] = treeNode(items[0], count, inTree)
        # 更新头指针表，以指向新的节点
        if headerTable[items[0]][1] == None:
            headerTable[items[0]][1] = inTree.children[items[0]]
        else:
            updateHeadera(headerTable[items[0]][1], inTree.children[items[0]])
    # 不断调用自身函数，每次调用会去掉列表中第一个元素
    if len(items) > 1:
        updateTree(items[1:], inTree.children[items[0]], headerTable, count)


def updateHeadera(nodeToTest, targetNode):
    # """确保节点链接指向树中该元素项的每一个实例"""
    # 从头指针表的nodeLink开始，一直沿着nodeLink直到到达链表末尾
    while (nodeToTest.nodeLink != None):
        nodeToTest = nodeToTest.nodeLink
    nodeToTest.nodeLink = targetNode


# 发现以给定元素项结尾的所有路径函数
def ascendTree(leafNode, prefixPath):
    if leafNode.parent != None:
        prefixPath.append(leafNode.name)
        ascendTree(leafNode.parent, prefixPath)


# 自定义支持度
def findPrefixPath(treeNode):
    condPats = {}
    while treeNode != None:
        prefixPath = []
        ascendTree(treeNode, prefixPath)  # 迭代上溯整棵树
        if len(prefixPath) > 1:
            # 前缀路径对应的计数值
            # print('prefixPath[1:]:')
            # print(prefixPath[1:])
            support = is_all_in_sum(abnormalTraceVertex, prefixPath[1:])
            treeNode.count = support / abnormalNum
            condPats[frozenset(prefixPath[1:])] = treeNode.count
        treeNode = treeNode.nodeLink
    return condPats


# 递归查找频繁项集的mineTree
def mineTree(inTree, headerTable, minsup, preFix, freqItemList):
    # 从头指针表的低端开始
    # headerTable.items():类似[('z', [5, None]），('r', [3,None]]格式，所以按p[1][0]排序
    print('mineTree:headerTable:', headerTable)
    print('headerTable.items:', headerTable.items())
    bigL = [v[0] for v in sorted(headerTable.items(), key=lambda p: p[1][0])]

    for basePat in bigL:
        newFreqSet = preFix.copy()
        newFreqSet.add(basePat)  # set类型的用add方法添加
        freqItemList.append(newFreqSet)
        # 从条件模式基中构建条件FP树
        condPattBase = findPrefixPath(headerTable[basePat][1])
        myCondTree, myHead = createTree(condPattBase, minsup)
        # 挖掘条件FP树
        if myHead != None:
            print('conditional tree for :', newFreqSet)
            myCondTree.displayFPTree()
            mineTree(myCondTree, myHead, minsup, newFreqSet, freqItemList)


def createInitSet(dataSet):
    retDict = {}
    for trans in dataSet:
        retDict[frozenset(trans)] = is_all_in_sum(abnormalTraceVertex, trans) / abnormalNum
        # retDict[frozenset(trans)] = 1
    return retDict


def calc_sup_and_con(freqItems):
    for item in freqItems:
        item_in_ab = is_all_in_sum(abnormalTraceVertex, list(item))
        item_in_all = is_all_in_sum(traceVertex, list(item))
        support = item_in_ab / abnormalNum
        confidence = item_in_ab / item_in_all
        H_sup_con = 2 * item_in_ab / (abnormalNum + item_in_all)
        JI = H_sup_con / (2 - H_sup_con)
        freq_JI[frozenset(item)] = JI
    print('freq_JI:',freq_JI)
    sorted_freq_JI = sorted(freq_JI.items(), key=lambda d: d[1], reverse=True)
    print('sorted_freq_JI:',sorted_freq_JI)
    # for item in sorted_freq_JI:
    #     print('item[0]:',item[0],type(item[0]))
    #     print('item[1]:',item[1],type(item[1]))
    return sorted_freq_JI


def initTraceDataC():
    # for ln in open('abnormalTrace.txt', 'rt'):
    #     abnormalTrace.extend(ln.strip().split(' '))
    # 拿到出故障后的文件
    path = '/home/yanghong/practical/OneOperation/chaos.json'
    f = open(path)
    data = json.load(f)
    for traceId, value in data.items():
        if traceId not in abnormalTrace:
            continue
        edges = value['edges']
        vertexs = value['vertexs']
        abnormalTraceInfo[traceId] = {"vertexs": vertexs, "edges": edges}
        vertexInfo = []
        vertexSize = len(vertexs)
        for i in range(1, vertexSize):
            vertexInfo.append(vertexs[str(i)][0])
        abnormalTraceVertexDict[traceId] = vertexInfo


# 一个频繁集在某一条trace中的入度出度
def calc_in_and_out(traceId, prefixList):
    traceInfo = abnormalTraceInfo[traceId]
    edges = traceInfo['edges']
    vertexs = traceInfo['vertexs']
    # 出度为-，入度为+
    for startId, edgeInfo in edges.items():
        edgeNum = len(edgeInfo)
        if startId in freq_in_and_out:
            freq_in_and_out[startId] -= edgeNum
        else:
            freq_in_and_out[startId] = (-1) * edgeNum
        for i in range(edgeNum):
            index = str(edgeInfo[i]['vertexId'])
            if index in freq_in_and_out:
                freq_in_and_out[index] += 1
            else:
                freq_in_and_out[index] = 1
    result = 0
    for key, value in freq_in_and_out.items():
        if key not in vertexs:
            continue
        vertex_name = vertexs[key][0]
        if vertex_name not in prefixList:
            continue
        result += value
    return result


# 求一个频繁集的内值
def get_in_and_out_degree(traceVertexDict, prefixList):
    in_set_degree_num = 0
    for traceId, vertex in traceVertexDict.items():
        is_all_in = True
        for prefix in prefixList:
            if prefix not in vertex:
                is_all_in = False
                break
        if is_all_in == False:
            continue
        # 计算prefixList中的每个服务在这一条trace中的入度出度和
        in_set_degree = calc_in_and_out(traceId, prefixList)
        in_set_degree_num += in_set_degree
    JI = top_k_freq[frozenset(prefixList)]
    # JI = top_k_freq[prefixList]
    service_set_degree[frozenset(prefixList)] = JI * in_set_degree_num
    # service_set_degree[prefixList] = JI * in_set_degree_num


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
    print('sorted_freq_JI:', sorted_freq_JI)
    # 通过JI降序排序，取top-k集。默认情况下，将k设置为100
    k = min(100, len(sorted_freq_JI))
    top_k_freq = get_order_dict_N(sorted_freq_JI, k)

    initTraceDataC()
    print('top_k_freq:', top_k_freq)
    for frq in top_k_freq.keys():
        freq_in_and_out.clear()
        get_in_and_out_degree(abnormalTraceVertexDict, list(frq))
    sorted_service_set_degree = sorted(service_set_degree.items(), key=lambda d: d[1], reverse=True)
    # 输出最可疑的微服务集和它的分数
    root_cause_dict = get_order_dict_N(sorted_service_set_degree, 1)
    print('最终结果，最后得到的可疑集以及它的分数：',root_cause_dict)
