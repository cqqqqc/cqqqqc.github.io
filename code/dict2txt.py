def dict2txt(dict):
    file = open('dict.txt', 'w')

    # �����ֵ��Ԫ�أ���ÿ��Ԫ�ص�key��value�ֲ�����ַ�����ע����ӷָ����ͻ��з�
    for k, v in dict.items():
        file.write(str(k) + ' ' + str(v) + '\n')

    # ע��ر��ļ�
    file.close()