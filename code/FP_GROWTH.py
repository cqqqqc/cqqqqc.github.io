# coding=gbk

import random
class treeNode:
    # """FP�����ඨ��"""
    def __init__(self,nameValue,numOccur,parentNode):
        self.name = nameValue  # ��Žڵ������
        self.count = numOccur  # ����ֵ
        self.nodeLink = None   # �����������Ƶ�Ԫ����
        self.parent = parentNode  # ָ��ǰ�ڵ�ĸ��ڵ�
        self.children = {}   # ��ǰ�ڵ���ӽڵ�

    def inc(self,numOccur):
        # """��count�������Ӹ���ֵ"""
        self.count += numOccur

    def displayFPTree(self,ind=1):
        # """�������ı���ʽ��ʾ����"""
        print("  "*ind,self.name,"  ",self.count)
        for child in self.children.values():
            child.displayFPTree(ind+1)

# FP����������
def createTree(dataSet,minsup=1):
    print('----------------------------------------------------------------')
    # """����FP����������������ݼ�dataSet���ֵ�����"""
    # �����ݼ����е�һ��ɨ�裬ͳ��ÿ��Ԫ������ֵ�Ƶ�ʣ����������ͷָ�����
    headerTable = {}
    for trans in dataSet:
        print('trans:',trans)
        for item in trans:
            print('item:',item)
            print('headerTable.get(item,0)',headerTable.get(item,0))
            print('dataSet[trans]',dataSet[trans])
            headerTable[item] = headerTable.get(item,0) + dataSet[trans]
    print('headerTable:',headerTable)
    # ȥ��ͷָ����г��ִ���С����С֧�ֶ���ֵ����
    for item in list(headerTable.keys()):
        if headerTable[item] < minsup:
            del (headerTable[item])
    freqItemSet = set(headerTable.keys())  # ��ȡƵ����
    # ���û��Ԫ��������Ҫ�����˳�
    if len(freqItemSet) == 0:
        return None,None

    # ��ͷָ��������չ���Ա���Ա������ֵ��ָ��ÿ�����͵�һ��Ԫ�����ָ��
    for item in headerTable:
        headerTable[item] = [headerTable[item], None]
    # ����ֻ�����ռ��ϵĸ��ڵ�
    retTree = treeNode('Null Set', 1, None)
    # �����ݼ����еڶ���ɨ�裬����FP��
    for trans,count in dataSet.items():
        localD = {}
        # �Ը�����й���
        for item in trans:
            if item in freqItemSet: # ������Ƶ����
                localD[item] = headerTable[item][0]
        # �Ը���������򣬰�Ԫ�ص�Ƶ��������,�����Ԫ����Ƶ����ͬ����ĸ˳������
        if len(localD) > 0:
            # ord() ��������һ���ַ�������Ϊ1���ַ�������Ϊ���������ض�Ӧ��ʮ����ASCII��ֵ�����磺ord('a') ����97  ord('b') ����98
            # ����������� -ord(p[0]) ��Ϊ int(p[0])
            orderedItems = [v[0] for v in sorted(localD.items(), key=lambda p: p[1], reverse=True)]
            # orderedItems = [v[0] for v in sorted(localD.items(), key=lambda p: (p[1], -ord(p[0])), reverse=True)]
            updateTree(orderedItems,retTree,headerTable,count)
    return retTree,headerTable


def updateTree(items,inTree,headerTable,count):
    # """����FP������FP������"""
    # �ж���е�һ��Ԫ�����Ƿ���Ϊ�ӽڵ���ڣ�������ڣ����¸�Ԫ����ļ���
    if items[0] in inTree.children:
        inTree.children[items[0]].inc(count)
    else:  # �����ڣ��򴴽��µĽڵ㣬����Ϊ�ӽڵ���ӵ�����
        inTree.children[items[0]] = treeNode(items[0],count,inTree)
        # ����ͷָ�����ָ���µĽڵ�
        if headerTable[items[0]][1] == None:
            headerTable[items[0]][1] = inTree.children[items[0]]
        else:
            updateHeadera(headerTable[items[0]][1], inTree.children[items[0]])
    # ���ϵ�����������ÿ�ε��û�ȥ���б��е�һ��Ԫ��
    if len(items) > 1:
        updateTree(items[1:],inTree.children[items[0]],headerTable,count)

def updateHeadera(nodeToTest,targetNode):
    # """ȷ���ڵ�����ָ�����и�Ԫ�����ÿһ��ʵ��"""
    # ��ͷָ����nodeLink��ʼ��һֱ����nodeLinkֱ����������ĩβ
    while (nodeToTest.nodeLink != None):
        nodeToTest = nodeToTest.nodeLink
    nodeToTest.nodeLink = targetNode

# �����Ը���Ԫ�����β������·������
def ascendTree(leafNode,prefixPath):
    if leafNode.parent != None:
        prefixPath.append(leafNode.name)
        ascendTree(leafNode.parent,prefixPath)

def findPrefixPath(treeNode):
    condPats = {}
    while treeNode != None:
        prefixPath = []
        ascendTree(treeNode,prefixPath)  # ��������������
        if len(prefixPath) > 1:
            # ǰ׺·����Ӧ�ļ���ֵ
            support=random.randint(2,100)
            treeNode.count=support
            condPats[frozenset(prefixPath[1:])] = treeNode.count
        treeNode = treeNode.nodeLink
    return condPats

# �ݹ����Ƶ�����mineTree
def mineTree(inTree,headerTable,minsup,preFix,freqItemList):
    # ��ͷָ���ĵͶ˿�ʼ
    # headerTable.items():����[('z', [5, None]����('r', [3,None]]��ʽ�����԰�p[1][0]����
    bigL = [v[0] for v in sorted(headerTable.items(),key=lambda p:p[1][0])]
    print('*********************************************************')
    print("headerTable:")
    print(headerTable)
    for basePat in bigL:
        newFreqSet = preFix.copy()
        newFreqSet.add(basePat)  # set���͵���add�������
        freqItemList.append(newFreqSet)
        # ������ģʽ���й�������FP��
        condPattBase = findPrefixPath(headerTable[basePat][1])
        myCondTree, myHead = createTree(condPattBase,minsup)
        # �ھ�����FP��
        if myHead != None:
            print('conditional tree for :',newFreqSet)
            myCondTree.displayFPTree()
            mineTree(myCondTree,myHead,minsup,newFreqSet,freqItemList)

# �����ݺ����ݰ�װ��
def loadData():
    simpDat = [['rq','z','h','j','p'],
               ['z','y','x','w','v','u','t','s'],
               ['z'],
               ['rq','x','n','o','s'],
               ['y','rq','x','z','q','t','p'],
               ['y','z','x','e','q','s','t','m']]
    return simpDat

def createInitSet(dataSet):
    retDict = {}
    for trans in dataSet:
        retDict[frozenset(trans)] =1
    return retDict

if __name__ == "__main__":
    dataSet = loadData()
    initSet = createInitSet(dataSet)
    minsup=3
    myFPTree,myheaderTable = createTree(initSet, minsup)
    print('������FP����')
    myFPTree.displayFPTree()
    freqItems = []
    print("��ʾ���е�������")
    mineTree(myFPTree,myheaderTable,minsup,set([]),freqItems)
    print('Ƶ�����\n',freqItems)
    #[list{set},{}]
    print(type(freqItems[0]))