#!/usr/bin/python3
import sys
import time
import re
import requests,json,time
from bs4 import BeautifulSoup
import json

class sina300():
    def __init__(self):
        #self.queue=Queue()
        self.info=[]
        self.json=[]
        self.proxy=''
        self.num=1
        self.url='http://vip.stock.finance.sina.com.cn/corp/view/vII_NewestComponent.php?page='+str(self.num)+'&indexid=000300'
    def get_proxy(self):
        return requests.get("http://127.0.0.1:5010/get/").json()

    def delete_proxy(self,proxy):
        requests.get("http://127.0.0.1:5010/delete/?proxy={}".format(proxy))
    def get_one_page(self,url):
        try: #proxies={'http': ip},
            headers= {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'}
            response = requests.get(url, headers=headers,timeout=3,proxies=self.proxy)
            if response.status_code == 200:
                return (response)
        except RequestException:
            print('连接失败')
       	    return None
    def get300(self):
        stock_list=[]
        for i in range(1,9):
            self.num=i
            self.url='http://vip.stock.finance.sina.com.cn/corp/view/vII_NewestComponent.php?page='+str(self.num)+'&indexid=000300'
            response=self.get_one_page(self.url)
            soup=BeautifulSoup(response.content.decode("gb2312"),"html.parser")
            trs = soup.find_all(href=re.compile("realstock"),target="_blank")
            for i in (trs):
                i1=re.findall('上证指数|深圳成指|沪深300',str(i))
                if len(i1) == 0:
                    stockcode=str(i).split(' ')[1].split('/')[5][2:8]
                    stocktype=str(i).split(' ')[1].split('/')[5][0:2]
                    stockname=str(i).split(' ')[2].split('>')[1].split('</a')[0]
                    data={"SECNAME":stockname ,"SECCODE": stockcode ,'f_kind': stocktype,"s_kind": "种植业", "t_kind": "种子生产"}
                    data1=json.dumps(data,ensure_ascii=False)
                    print(data1)

#{"SECNAME": "丰乐种业", "SECCODE": "000713", "f_kind": "农林牧渔", "s_kind": "种植业", "t_kind": "种子生产"}

                




if __name__ == '__main__':


    start_time=time.time()

    a=sina300().get300()



    print("总耗时：{}秒".format(time.time()-start_time))

