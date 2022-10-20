#!/usr/bin/python3
import json
from clickhouse_driver import Client

data={}
with open("./data.json","r") as f:
    a=f.readlines()
    for i in range(0,1):
        i1=json.loads(a[i])
#insert into stock.stock(message) values
        sql_text='truncate table stock.stock;'
        sql_text='insert into stock.stock(message) values (\'' + i1 + '\');'
        print(sql_text)
        client = Client('10.100.239.2')







