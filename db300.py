#!/usr/bin/python3
import json

with open("./data.json","r") as f:
    a=f.readlines()
    for i in range(0,2):
        try:
        #print(i)
            i1=json.loads(a[i])
            i2=json.loads(i1)
        #print(i2)
            print(i2)
        except Exception as e:
            pass






