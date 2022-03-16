# coding=gbk

import pickle

path = 'D:\\practical\\A\\microservice\\test\\admin-order_abort_1011.pkl'
# path = 'D:\\practical\\A\\API\\ticketinfo_delay_0421.pkl'
f = open(path, 'rb')
data = pickle.load(f)

print(data)
print(len(data))
