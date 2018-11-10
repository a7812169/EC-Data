import time

import os
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
	with open(a, 'wb')as f:
		f.write(res)


# ---------------------------
url = 'http://www.nmgtj.gov.cn/acmrdatashownmgpub/files_nmg_pub/html/nmgtjnj/{}/left.htm'
if __name__ == '__main__':

	for year in list(range(2014, 2017)):
		url = url.format(year)
		content = requests.get(url)
		content.encoding = content.apparent_encoding
		soup = BeautifulSoup(content.text, 'lxml')
		b = soup.ul.find_all('li', {"id": "foldheader"})
		for i in range(len(b) - 2):
			title = soup.ul.find_all('li', {"id": "foldheader"})[i + 2].get_text()
			path = '内蒙古' + '\\' + str(year) + '\\' + title
			print(path)
			c = soup.find_all('ul')[i + 3].find_all('li')
			if mkdir(path):
				for l in range(len(c)):
					file_name = c[l].get_text()
					url = 'http://www.nmgtj.gov.cn/acmrdatashownmgpub/files_nmg_pub/html/nmgtjnj/{}/'.format(year) + c[
						l].a.get('href')
					data = requests.get(url).content
					save_html(path, file_name, data, 'jpg')
	stop = time.clock()
	print('用时', start - stop)
