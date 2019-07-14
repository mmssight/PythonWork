#coding=utf-8

from bs4 import BeautifulSoup
import urllib.request   as request
import requests
import urllib
import re
import time
import os
import json


os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.UTF8'
class database:
    def __init__(self,chose):
        self.conn_url={
            'mysql':{'user':'root',
                     'host':'192.168.1.106',
                     'pw':'root',
                     'port':3306,
                     'db':'myself',
                     'charset':'utf8'
                     }
        }
        self.base={
            '1':'mysql',
            '2':'oracle'
        }
        self.chose=chose
        self.conn=None
        self.cur=None
    def mysql(self):
        """连接mysql数据库"""
        try:
            self.conn = pymysql.connect(user=self.conn_url['mysql']['user'],host=self.conn_url['mysql']['host'],passwd=self.conn_url['mysql']['pw'],port=self.conn_url['mysql']['port'],db=self.conn_url['mysql']['db'],charset=self.conn_url['mysql']['charset'])
            self.cur = self.conn.cursor()
            return self.cur
        except Exception as e:
            print('mysql_connect:%s'%e)
    def excute_sql(self,sql):
        try:
            if self.base['%s'%self.chose] == 'mysql':
                cursor=self.mysql()
            else:
                print('连接错误')
                return
            cursor.execute(sql)
            re = cursor.fetchall()
            #print(re)
            #print(self.cur.fetchone())
            return re
        except Exception as e:
            print('excute:%s'%e)
            self.conn.rollback()
        finally:
            if self.base['%s'%self.chose] == 'mysql':
                self.conn.commit()
                self.conn.close()
            else :
                return False
class gethttmlpage(database):
    def __init__(self,chose):
        database.__init__(self,chose)  #重构
        """头文件，伪装成浏览器"""
        self.headers = {
            #'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36',
            'authority': 'search.jd.com',
            'method': 'GET',
            'path': '/s_new.php?keyword=%E6%89%8B%E6%9C%BA&enc=utf-8&qrst=1&rt=1&stop=1&vt=2&wq=%E6%89%8B%E6%9C%BA',
            'scheme': 'https',
            'referer': 'https://search.jd.com/Search?keyword=%E6%89%8B%E6%9C%BA&enc=utf-8&qrst=1&rt=1&stop=1&vt=2&wq=%E6%89%8B%E6%9C%BA&cid2=653&cid3=655&page=3&s=58&click=0',
            'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36',
            'x-requested-with': 'XMLHttpRequest',
            'Cookie': 'qrsc=3; pinId=RAGa4xMoVrs; xtest=1210.cf6b6759; ipLocation=%u5E7F%u4E1C; _jrda=5; TrackID=1aUdbc9HHS2MdEzabuYEyED1iDJaLWwBAfGBfyIHJZCLWKfWaB_KHKIMX9Vj9_2wUakxuSLAO9AFtB2U0SsAD-mXIh5rIfuDiSHSNhZcsJvg; shshshfpa=17943c91-d534-104f-a035-6e1719740bb6-1525571955; shshshfpb=2f200f7c5265e4af999b95b20d90e6618559f7251020a80ea1aee61500; cn=0; 3AB9D23F7A4B3C9B=QFOFIDQSIC7TZDQ7U4RPNYNFQN7S26SFCQQGTC3YU5UZQJZUBNPEXMX7O3R7SIRBTTJ72AXC4S3IJ46ESBLTNHD37U; ipLoc-djd=19-1607-3638-3638.608841570; __jdu=930036140; user-key=31a7628c-a9b2-44b0-8147-f10a9e597d6f; areaId=19; __jdv=122270672|direct|-|none|-|1529893590075; PCSYCityID=25; mt_xid=V2_52007VwsQU1xaVVoaSClUA2YLEAdbWk5YSk9MQAA0BBZOVQ0ADwNLGlUAZwQXVQpaAlkvShhcDHsCFU5eXENaGkIZWg5nAyJQbVhiWR9BGlUNZwoWYl1dVF0%3D; __jdc=122270672; shshshfp=72ec41b59960ea9a26956307465948f6; rkv=V0700; __jda=122270672.930036140.-.1529979524.1529984840.85; __jdb=122270672.1.930036140|85.1529984840; shshshsID=f797fbad20f4e576e9c30d1c381ecbb1_1_1529984840145'

        }
        # self.url=url


        self.urllist=[]
        self.computer={}
    def getpage(self,url):
        """getpage 获取页面属性，将源文件转换成string类型文件"""
        try:
            #print(url)
            # 创建resquestqingqui
            #req = request.Request(url=url, headers=self.headers)
            #time.sleep(0.1)
            req = requests.get(url=url, headers=self.headers)

            # 利用urloppen获得文件
            #reqpage = request.urlopen(req)
            # 获得文件内容
            #page = reqpage.read().decode('utf-8')
            page = req.text
            #print(page)
            return page

        except Exception as e:
            print('getpage:%s'%e)
    def geturl(self,url):
        try:
            page = self.getpage(url)
            soup = BeautifulSoup(page, 'html.parser')
            ietm = soup.find_all('span', class_='curr')
            type = []
            for a in ietm:
                type.append(a.get_text())
            item = ''
            for i in range(len(type) - 1):
                print(i, len(type))
                item += str(i + 1) + ':' + type[i] + ',  '
            item += str(len(type)) + ':' + type[len(type) - 1]
            self.computer.update(jd_item=item)
            url_str= soup.find_all(class_='p-name')
            for i in range(len(url_str)):
                soup_url = BeautifulSoup(str(url_str[i]), 'html.parser')
                url = soup_url.find('a')
                self.urllist.append('https:%s' % url['href'])
                time.sleep(0.1)
                self.page  = self.getpage('https:%s' % url['href'])
        except Exception as e:
            print('geturl:%s'%e)
    def get_detail(self):
        try:
            urllist = self.urllist
            for i in range(len(urllist)):
                url = urllist[i]
                self.computer.update(jd_url=url)
                page=self.getpage(url)
                jd_price = self.jd_price(url)
                self.computer.update(jd_price=jd_price)
                self.get_column(page)
        except Exception as e:
            print('get_detaill:%s'%e)

    def jd_price(self,url):
        try:
            sku = url.split('/')[-1].strip(".html")
            price_url = "https://p.3.cn/prices/mgets?skuIds=J_" + sku
            response = requests.get(price_url)
            content = response.text
            result = json.loads(content)
            record = result[0]
            return record['p']
        except Exception as e:
            print(e)

    def get_column(self,page):
        try:
            soure = BeautifulSoup(page, 'html.parser')
            name_ = soure.find_all(class_='item ellipsis')
            tip_ = soure.find_all('div', class_='sku-name')
            detail_ = soure.find_all('ul', class_='parameter2 p-parameter-list')
            name = None
            tip = None
            detail = None
            for nm in name_:
                name=nm.get_text()
            self.computer.update(jd_name=name)
            for t in tip_:
                tip=t.get_text()
            self.computer.update(jd_tip=tip)
            for d in detail_:
                detail=d.get_text().strip('\n')
            self.computer.update(jd_detail=detail)
            self.insert_date()
        except Exception as e:
            print('get_column:%s'%e)
    def insert_date(self):
        try:
            sql = "insert into jd (jd_name,jd_price,jd_item,jd_tip,jd_detail,jd_url) values(trim('%s'),'%s',trim('%s'),trim('%s'),trim('%s'),trim('%s'))"%(self.computer['jd_name'],self.computer['jd_price'],self.computer['jd_item'],self.computer['jd_tip'],self.computer['jd_detail'],self.computer['jd_url'])
            self.chose='1'

            return self.excute_sql(sql)
        except Exception as e:
            print('insert_date:%s'%e)

if __name__=='__main__':
    a=gethttmlpage('1')
    for page_num in range(1,159):
        print('正在爬取第'+str(page_num)+'页')
        url = 'https://coll.jd.com/list.html?sub=22594&page='+str(page_num)

        a.geturl(url)
        a.get_detail()

