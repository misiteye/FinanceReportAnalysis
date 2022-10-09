#coding=utf-8
import sys
reload(sys)
import time
sys.setdefaultencoding('utf-8')
import requests,json,time
from bs4 import BeautifulSoup
from methods import Queue
#from multiprocessing import get_context
#from multiprocessing.queues import Queue
from concurrent.futures import ThreadPoolExecutor

class Xinalang():
    def __init__(self):
        self.queue=Queue()
        self.info=[]
        self.json=[]


    def req(self,ninfo):
        try:
            info=json.loads(ninfo)
            scode=info["SECCODE"]
            year=info["year"]

            #print(scode,year)
            data_=info

            url0='http://money.finance.sina.com.cn/corp/go.php/vFD_BalanceSheet/stockid/{}/ctrl/{}/displaytype/4.phtml'.format(scode,year)
            url1='http://money.finance.sina.com.cn/corp/go.php/vFD_ProfitStatement/stockid/{}/ctrl/{}/displaytype/4.phtml'.format(scode,year)
            url2='http://money.finance.sina.com.cn/corp/go.php/vFD_CashFlow/stockid/{}/ctrl/{}/displaytype/4.phtml'.format(scode,year)
            #print(url0)
            url_list=[]
            url_list.extend([url0,url1,url2])
            data_year=[]
            for url in url_list:
                headers={}
                response=requests.get(url,headers=headers,timeout=5)
                #soup=BeautifulSoup(response.content.decode("gb2312"),"html5lib")
                soup=BeautifulSoup(response.content.decode("gb2312"),"lxml",)
                #print(soup)
                '''报表日期'''
                trs = soup.select("tbody tr")

                #print(trs)
                data={}
                for tr in trs:
                    #print(tr)
                    tds=tr.select("td")
                    if tds != []:
                        #print(tr)
                        #decode('unicode-escape')
                        #tds1=str(tds).decode('unicode-escape')
                        try:
                            value = tds[1].text
                            if value == "--":
                                value = "0.00"
                            data[tds[0].text] = value
                        except:
                            pass
                data_year.append(str(data).decode('unicode-escape'))

            data_["data"]=data_year
            #print(info["SECNAME"],info["year"])
            self.json.append(json.dumps(data_))
        except TimeoutError:
            print("超时")
            self.info.append(ninfo)
        except:
            print("其他错误")
            print("其他错误")
            info = json.loads(ninfo)
            print(info["SECNAME"], info["year"])

    def scheduler(self):
        year_list=[2014,2015,2016,2017,2018,2019,2020,2021,2022]
        #year_list=[2014]
        with open("./stockCode.txt") as f:
            lines=f.readlines()

        for line in lines:

            print(line)
            info=json.loads(line)
            #print(info)
            for year in year_list:
                #print(year)
                info["year"]=year
                info_str=json.dumps(info)

                #print(json.loads(info_str))

                self.queue.put(info_str)

        pool=ThreadPoolExecutor(max_workers=8)
        while self.queue.qsize()>0:
            pool.submit(self.req, self.queue.get())
        pool.shutdown()

        #print("剩下："+str(len(self.info)))
        ##print(len(self.info))

        while len(self.info)>0:

            self.req(self.info.pop())

        self.write_json()

    def write_json(self):
        try:
            for j in self.json:
                #print(j.decode('unicode-escape'))
                with open('./data.json', 'a') as f:
                    json.dump(j.decode('unicode-escape'), f,ensure_ascii=False)
        except:
            print("写入出错！！")
            pass



if __name__ == '__main__':


    start_time=time.time()

    X = Xinalang()
    X.scheduler()

    print("总耗时：{}秒".format(time.time()-start_time))


