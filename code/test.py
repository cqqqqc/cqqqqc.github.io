# coding=gbk

if __name__ == "__main__":
    # �ȴ�������һ���ı��ļ�
    file = open('dict.txt', 'w')
    dict_temp={'sdfg':123.34567,'qwert':456789.23456}
    # �����ֵ��Ԫ�أ���ÿ��Ԫ�ص�key��value�ֲ�����ַ�����ע����ӷָ����ͻ��з�
    for k, v in dict_temp.items():
        file.write(str(k) + ' ' + str(v) + '\n')

    # ע��ر��ļ�
    file.close()

    # �ֵ��������������ģ�����밴���ֵ��key��������Ļ������԰�������ķ�ʽʵ��
    # for k,v in sorted(dict_temp.items()):
    # 	file.write(str(k)+' '+str(v)+'\n')
    # file.close()

    # ����һ�����ֵ䣬�������ı��ļ�����
    dict_temp = {}

    # ���ı��ļ�
    file = open('dict.txt', 'r')

    # �����ı��ļ���ÿһ�У�strip�����Ƴ��ַ���ͷβָ�����ַ���Ĭ��Ϊ�ո���з������ַ�����
    for line in file.readlines():
        line = line.strip()
        k = line.split(' ')[0]
        v = line.split(' ')[1]
        dict_temp[k] = float(v)

    # �����ǹر��ļ�
    file.close()

    #  ���Դ�ӡ�������
    print(dict_temp)
