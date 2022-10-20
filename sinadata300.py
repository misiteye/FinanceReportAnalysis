#!/usr/bin/python3
import sys
import time
import re
import requests,json,time
from bs4 import BeautifulSoup


class sinadata300():
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
    def req(self,ninfo):
        try:
            info=json.loads(ninfo)
            scode=info["SECCODE"]
            year=info["year"]
            data_=info

            url0='http://money.finance.sina.com.cn/corp/go.php/vFD_BalanceSheet/stockid/{}/ctrl/{}/displaytype/4.phtml'.format(scode,year)
            url1='http://money.finance.sina.com.cn/corp/go.php/vFD_ProfitStatement/stockid/{}/ctrl/{}/displaytype/4.phtml'.format(scode,year)
            url2='http://money.finance.sina.com.cn/corp/go.php/vFD_CashFlow/stockid/{}/ctrl/{}/displaytype/4.phtml'.format(scode,year)
            url_list=[]
            url_list.extend([url0,url1,url2])
            #url_list.extend([url0])
            for url in url_list:
                data_year={}
                tname=url.split('_')[1].split('/')[0].lower()
                #print(tname)
                response=self.get_one_page(url)
                soup=BeautifulSoup(response.content.decode("gb2312"),"html.parser")
                trs = soup.select("tbody tr")
                for tr in trs:
                    soup1=BeautifulSoup(str(tr),"html.parser")
                    tds=soup1.find_all('td',limit=2)
                    stock_name=''
                    stock_alias=''
                    stock_value=''
                    for td in tds:
                        td1 = re.match('.*href=.*',str(td))
                        if td1:
                            stock_name=td.text
                            stock_alias=td1.group(0).split(';')[1].split('=')[1].split('&amp')[0].lower()
                        else:
                            stock_value=td.text.replace('--','0.00')
                    if len(stock_name) > 0:
                        data_year[stock_alias]=float(stock_value.replace(',',''))
                data_[tname]=data_year

            self.json.append(json.dumps(data_,ensure_ascii=False))
            
        except TimeoutError:
            print("超时")
        except Exception as e:
            print("其他错误:")
            print(e)
            print(info["SECNAME"], info["year"])
    def scheduler(self):
        year_list=[2014,2015,2016,2017,2018,2019,2020,2021,2022]
        #year_list=[2022,2021]
        #year_list=[2021]
        with open("./stockCode.txt") as f:
            lines=f.readlines()


        for line in lines:
            info=json.loads(line)
            for year in year_list:
                info["year"]=year
                self.info=json.dumps(info)
                self.req(self.info)


        self.write_json()



    def write_json(self):
        try:
            for j in self.json:
                with open('./data.json', 'a') as f:
                    json.dump(j, f)
                    f.write('\n')
        except Exception as e :
            print("写入出错！！")
            print(e)
            pass
if __name__ == '__main__':


    start_time=time.time()

    X = sinadata300()
    X.scheduler()


    print("总耗时：{}秒".format(time.time()-start_time))

