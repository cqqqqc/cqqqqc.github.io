def dict2txt(dict):
    file = open('dict.txt', 'w')

    # 遍历字典的元素，将每项元素的key和value分拆组成字符串，注意添加分隔符和换行符
    for k, v in dict.items():
        file.write(str(k) + ' ' + str(v) + '\n')

    # 注意关闭文件
    file.close()