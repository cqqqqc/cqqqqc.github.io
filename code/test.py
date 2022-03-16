# coding=gbk

if __name__ == "__main__":
    # 先创建并打开一个文本文件
    file = open('dict.txt', 'w')
    dict_temp={'sdfg':123.34567,'qwert':456789.23456}
    # 遍历字典的元素，将每项元素的key和value分拆组成字符串，注意添加分隔符和换行符
    for k, v in dict_temp.items():
        file.write(str(k) + ' ' + str(v) + '\n')

    # 注意关闭文件
    file.close()

    # 字典输出的项是无序的，如果想按照字典的key排序输出的话，可以按照下面的方式实现
    # for k,v in sorted(dict_temp.items()):
    # 	file.write(str(k)+' '+str(v)+'\n')
    # file.close()

    # 声明一个空字典，来保存文本文件数据
    dict_temp = {}

    # 打开文本文件
    file = open('dict.txt', 'r')

    # 遍历文本文件的每一行，strip可以移除字符串头尾指定的字符（默认为空格或换行符）或字符序列
    for line in file.readlines():
        line = line.strip()
        k = line.split(' ')[0]
        v = line.split(' ')[1]
        dict_temp[k] = float(v)

    # 依旧是关闭文件
    file.close()

    #  可以打印出来瞅瞅
    print(dict_temp)
