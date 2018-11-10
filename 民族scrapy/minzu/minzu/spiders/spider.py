# This package will contain the spiders of your Scrapy project
#
# Please refer to the documentation for information on how to create and manage
# your spiders.
import os
import random
import re

import requests
import yaml
from bs4 import BeautifulSoup
from pymongo import MongoClient
from scrapy import Request
from scrapy import Spider
from .public import mkdir
from ..items import Minzu_ningxia_Item


class spider_ningxia(Spider):
	cilient=MongoClient('127.0.0.1',27017)
	user_agent_list = [
		"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1" 
		"Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11",
		"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",
		"Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",
		"Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1",
		"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5",
		"Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5",
		"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
		"Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
		"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
		"Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
		"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
		"Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
		"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
		"Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
		"Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3",
		"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
		"Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24"
	]
	name = "minzu"
	def config_init(self):
		self.read_configuration_file(self.crawler.settings["config_name"])
	def read_configuration_file(self, config_file_name):
		config_file = os.path.dirname(os.path.realpath(__file__)) + os.sep.join(
			("", "configFiles", "")) + config_file_name + ".yaml"
		f = open(config_file, encoding='utf8')
		args = yaml.load(f)
		for arg in args:
			self.__setattr__(arg,args[arg])
	def start_requests(self):
		self.config_init()
		ua = random.choice(self.user_agent_list)  # 随机抽取User-Agent
		headers = {
			'Accept-Encoding': 'gzip, deflate, sdch, br',
			'Accept-Language': 'zh-CN,zh;q=0.8',
			'Connection': 'keep-alive',
			'Referer': 'https://gupiao.baidu.com/',
			'User-Agent': ua
		}

		for url in self.start_url:
			yield Request(url=url,callback=self.parse,headers=headers,meta={"name":self.city_name,"year":re.search(r'\d{4}',url).group(),"file_name":self.start_url[url]},dont_filter=True)
	def parse(self, response):
		"""
		:param response:
		:return:
		# year = scrapy.Field()
		# file_name = scrapy.Field()
		# url = scrapy.Field()
		"""
		meta=response.meta
		year=meta['year']
		city_name=meta['name']
		item=Minzu_ningxia_Item()
		item['year'] = year
		item['city_name']=city_name
		print('正在执行',year,city_name)
		data=requests.get(response.url)
		data.encoding=data.apparent_encoding

		soup = BeautifulSoup(data.text,'lxml')
		a = soup.find_all(text=re.compile('.*?篇'))
		print(a)
		for i in range(len(a)):
			type_name = a[i].replace('\n','').replace("\r",'')
			print('正在下载'+type_name)
			pattern = self.type_pattern.format(i + 1)
			k = soup.find_all('a', {'href': re.compile(pattern)})
			for l in range(len(k)):
				row_file_name = k[l].get_text().replace("\n", "").replace("\t","")
				file_name=re.sub(r'[a-zA-Z]',"",row_file_name)
				downld_url = self.common_download.replace('..','') + k[l].get('href').replace('..','')
				item['type_name']=type_name
				item['file_name']=file_name
				item['url']=downld_url
				item['content_type']=self.content_type
				path = os.getcwd() + "/" + item['city_name'] + "/" + item['year'] + "/" + item['type_name']
				print(path)
				file_name_path = path + "/" + item['file_name'] + "." + item['content_type']
				mkdir(path)
				print('正在下载', file_name_path)
				db_result=insert_db(self.cilient,city_name,type_name,file_name,downld_url,self.content_type)
				if db_result==None:
					continue
				url = item['url']
				content_type = item['content_type']
				downld(file_name_path, url, content_type)
				yield item
def downld(path,url,content_type):
	headers = {
        'Accept-Encoding': 'gzip, deflate, sdch, br',
        'Accept-Language': 'zh-CN,zh;q=0.8',
        'Connection': 'keep-alive',
        'Referer': 'https://gupiao.baidu.com/',
        'User-Agent': "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1"
    }
	if content_type== 'jpg':
		with open(path, "wb")as f:
			# print(url,headers)
			# print(requests.get(url, headers))
			f.write(requests.get(url, headers).content)
	else:
		with open(path, "w", encoding='utf-8')as f:
			# print(item['url'])
			f.write(requests.get(url,headers).text)
def insert_db(cilient,tabel_name,type_name,file_name,downld_url,content_type):
	db=cilient.test
	collection=db[tabel_name]
	data={
		'type_name' : type_name,
	'file_name' : file_name,
	'url' :downld_url,
	'content_type' : content_type,
	}
	if collection.find_one({'url':downld_url}):
		print('已经下载过，跳过')
		return None
	if collection.insert(data):
		print('插入数据库成功')
		return True

