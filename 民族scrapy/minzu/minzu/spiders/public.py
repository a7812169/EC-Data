""""公用函数"""
from bs4 import BeautifulSoup
import requests
from selenium import webdriver
def mkdir(path):
	"""建文件夹"""
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
def selunim_run(url,frame_name):
	driver = webdriver.Chrome()
	driver.get(url)
	driver.switch_to.frame(frame_name)
	page_source = driver.page_source
	return page_source