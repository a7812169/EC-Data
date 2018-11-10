import os
import re
import time

import requests
from bs4 import BeautifulSoup

start = time.clock()


def mkdir(path):
	# 引入模块
	import os
	# 去除首位空格
	path = path.strip()
	# 去除尾部 \ 符号
	path = path.rstrip("\\")
	# 判断路径是否存在
	# 存在     True
	# 不存在   False
	isExists = os.path.exists(path)
	# 判断结果
	if not isExists:
		# 如果不存在则创建目录
		# 创建目录操作函数
		os.makedirs(path)
		print(path + ' 创建成功')
		return True
	else:
		# 如果目录存在则不创建，并提示目录已存在
		print(path + ' 目录已存在')
		return False


def make_soup(url):
	data = requests.get(url)
	data.encoding = 'utf-8'
	data = data.text
	soup = BeautifulSoup(data, 'lxml')
	return soup


def save_html(name, file_name, res, type):
	a = os.getcwd() + '/' + name + '/' + file_name + '.' + type
	print(a)
	with open(a, 'wb')as f:
		f.write(res)


address = 'http://www.xjtj.gov.cn/sjcx/tjnj_3415/'
soup = make_soup(address)
a = soup.find("div", {"class": "xzdwLeftsidebar"})
b = a.find_all('li')
if __name__ == '__main__':
	for i in b:
		next_url = i.a.attrs['totarget']
		name = i.a.get_text()
		name = '新疆自治区' + '/' + name
		soup = make_soup(next_url)
		mkdir(name)
		c = soup.find('ul', {"class": "rightlist tjnj_bg"}).find_all('li')
		for l in c:
			title = l.a.get_text()
			link = re.search(r'http.*?l', l.a.attrs['href']).group()
			data = requests.get(link)
			data.encoding = 'utf-8'
			data = data.content
			save_html(name, title, data, 'html')
