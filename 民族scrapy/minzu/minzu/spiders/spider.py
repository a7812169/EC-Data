# This package will contain the spiders of your Scrapy project
#
# Please refer to the documentation for information on how to create and manage
# your spiders.
import yaml
import os
from selenium import webdriver
from scrapy import Spider
import re
from bs4 import BeautifulSoup
from .public import *
from scrapy import Request
from ..items import Minzu_ningxia_Item
class spider_ningxia(Spider):

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
		for url in self.start_url:
			yield Request(url=url,callback=self.parse,meta={"name":self.city_name,"year":re.search(r'\d{4}',url).group(),"file_name":self.start_url[url]},dont_filter=True)
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
		if self.if_frame==True:
			page_source=selunim_run(response.url,self.frame_name)
			soup = BeautifulSoup(page_source, 'lxml')
			a = soup.find_all(text=re.compile('.*?篇'))
			print(a)
			# ningxia/year/title/file_name.html
			for i in range(len(a)):
				type_name = a[i].replace("\n","").replace(" ","")
				print(type_name)
				pattern = self.type_pattern.format(i + 1)
				k = soup.find_all('a', {'href': re.compile(pattern)})
				for l in range(len(k)):
					row_file_name = k[l].get_text().replace("\n", "").replace("\t","")
					file_name=re.sub(r'[a-zA-Z]',"",row_file_name)
					downld_url = re.search(r'(.*)/',response.url).group(0) + k[l].get('href')
					item['type_name']=type_name
					item['file_name']=file_name
					item['url']=downld_url
					yield item
