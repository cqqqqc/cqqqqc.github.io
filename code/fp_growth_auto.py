# coding=gbk

import json
from collections import Counter
import numpy as np

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

class treeNode:
    # """FP�����ඨ��"""
    def __init__(self, nameValue, numOccur, parentNode):
        self.name = nameValue  # ��Žڵ������
        self.count = numOccur  # ����ֵ
        self.nodeLink = None  # �����������Ƶ�Ԫ����
        self.parent = parentNode  # ָ��ǰ�ڵ�ĸ��ڵ�
        self.children = {}  # ��ǰ�ڵ���ӽڵ�

    def inc(self, numOccur):
        # """��count�������Ӹ���ֵ"""
        self.count += numOccur

    def displayFPTree(self, ind=1):
        # """�������ı���ʽ��ʾ����"""
        print("  " * ind, self.name, "  ", self.count)
        for child in self.children.values():
            child.displayFPTree(ind + 1)


def get_order_dict_N(_dict, N):
    result = Counter(_dict).most_common(N)
    d = {}
    for k, v in result:
        d[k] = v
    return d


# ����trace�о���ĳ��list���з��������
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
    abnormalNum= len(abnormalTrace)
    print('������abnormalNum:', abnormalNum)
    # �õ������Ϻ���ļ�
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


# FP����������
def createTree(dataSet, minsup=1):
    print('----------------------------------------------------------------')
    # """����FP����������������ݼ�dataSet���ֵ�����"""
    # �����ݼ����е�һ��ɨ�裬ͳ��ÿ��Ԫ������ֵ�Ƶ�ʣ����������ͷָ�����
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
    # ȥ��ͷָ����г��ִ���С����С֧�ֶ���ֵ����
    for item in list(headerTable.keys()):
        if headerTable[item] < minsup:
            del (headerTable[item])
    freqItemSet = set(headerTable.keys())  # ��ȡƵ����
    print('createTree����ֵheaderTable:')
    print(headerTable)
    # ���û��Ԫ��������Ҫ�����˳�
    if len(freqItemSet) == 0:
        return None, None

    # ��ͷָ��������չ���Ա���Ա������ֵ��ָ��ÿ�����͵�һ��Ԫ�����ָ��
    for item in headerTable:
        temp=[headerTable[item], None]
        headerTable[item] = temp
    # ����ֻ�����ռ��ϵĸ��ڵ�
    retTree = treeNode('Null Set', 1, None)
    # �����ݼ����еڶ���ɨ�裬����FP��
    for trans, count in dataSet.items():
        localD = {}
        # �Ը�����й���
        for item in trans:
            if item in freqItemSet:  # ������Ƶ����
                localD[item] = headerTable[item][0]
        # �Ը���������򣬰�Ԫ�ص�Ƶ��������,�����Ԫ����Ƶ����ͬ����ĸ˳������
        if len(localD) > 0:
            # ord() ��������һ���ַ�������Ϊ1���ַ�������Ϊ���������ض�Ӧ��ʮ����ASCII��ֵ�����磺ord('a') ����97  ord('b') ����98
            # ����������� -ord(p[0]) ��Ϊ int(p[0])
            orderedItems = [v[0] for v in sorted(localD.items(), key=lambda p: p[1], reverse=True)]
            updateTree(orderedItems, retTree, headerTable, count)
    print('createTree����ֵheaderTable:')
    print(headerTable)
    return retTree, headerTable


def updateTree(items, inTree, headerTable, count):
    # """����FP������FP������"""
    # �ж���е�һ��Ԫ�����Ƿ���Ϊ�ӽڵ���ڣ�������ڣ����¸�Ԫ����ļ���
    if items[0] in inTree.children:
        inTree.children[items[0]].inc(count)
    else:  # �����ڣ��򴴽��µĽڵ㣬����Ϊ�ӽڵ���ӵ�����
        inTree.children[items[0]] = treeNode(items[0], count, inTree)
        # ����ͷָ�����ָ���µĽڵ�
        if headerTable[items[0]][1] == None:
            headerTable[items[0]][1] = inTree.children[items[0]]
        else:
            updateHeadera(headerTable[items[0]][1], inTree.children[items[0]])
    # ���ϵ�����������ÿ�ε��û�ȥ���б��е�һ��Ԫ��
    if len(items) > 1:
        updateTree(items[1:], inTree.children[items[0]], headerTable, count)


def updateHeadera(nodeToTest, targetNode):
    # """ȷ���ڵ�����ָ�����и�Ԫ�����ÿһ��ʵ��"""
    # ��ͷָ����nodeLink��ʼ��һֱ����nodeLinkֱ����������ĩβ
    while (nodeToTest.nodeLink != None):
        nodeToTest = nodeToTest.nodeLink
    nodeToTest.nodeLink = targetNode


# �����Ը���Ԫ�����β������·������
def ascendTree(leafNode, prefixPath):
    if leafNode.parent != None:
        prefixPath.append(leafNode.name)
        ascendTree(leafNode.parent, prefixPath)


# �Զ���֧�ֶ�
def findPrefixPath(treeNode):
    condPats = {}
    while treeNode != None:
        prefixPath = []
        ascendTree(treeNode, prefixPath)  # ��������������
        if len(prefixPath) > 1:
            # ǰ׺·����Ӧ�ļ���ֵ
            # print('prefixPath[1:]:')
            # print(prefixPath[1:])
            support = is_all_in_sum(abnormalTraceVertex, prefixPath[1:])
            treeNode.count = support/abnormalNum
            condPats[frozenset(prefixPath[1:])] = treeNode.count
        treeNode = treeNode.nodeLink
    return condPats


# �ݹ����Ƶ�����mineTree
def mineTree(inTree, headerTable, minsup, preFix, freqItemList):
    # ��ͷָ���ĵͶ˿�ʼ
    # headerTable.items():����[('z', [5, None]����('r', [3,None]]��ʽ�����԰�p[1][0]����
    print('mineTree:headerTable:',headerTable)
    print('headerTable.items:', headerTable.items())
    bigL = [v[0] for v in sorted(headerTable.items(), key=lambda p: p[1][0])]

    for basePat in bigL:
        newFreqSet = preFix.copy()
        newFreqSet.add(basePat)  # set���͵���add�������
        freqItemList.append(newFreqSet)
        # ������ģʽ���й�������FP��
        condPattBase = findPrefixPath(headerTable[basePat][1])
        myCondTree, myHead = createTree(condPattBase, minsup)
        # �ھ�����FP��
        if myHead != None:
            print('conditional tree for :', newFreqSet)
            myCondTree.displayFPTree()
            mineTree(myCondTree, myHead, minsup, newFreqSet, freqItemList)


def createInitSet(dataSet):
    retDict = {}
    for trans in dataSet:
        retDict[frozenset(trans)] = is_all_in_sum(abnormalTraceVertex,trans)/abnormalNum
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
    sorted_freq_JI = sorted(freq_JI.items(), key=lambda d: d[1], reverse=True)
    return sorted_freq_JI


if __name__ == "__main__":
    initTraceData()
    print('abnormalNum:',abnormalNum)
    print('traceNum:', traceNum)
    dataSet = abnormalTraceVertex
    print('abnormalTraceVertex:',len(abnormalTraceVertex))
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
    k = min(100,len(sorted_freq_JI))
    top_k_freq = get_order_dict_N(sorted_freq_JI, k)
