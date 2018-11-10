# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import os
from .spiders.public import mkdir
import requests
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
            f.write(requests.get(url, headers).content)
    else:
        with open(path, "w", encoding='utf-8')as f:
            # print(item['url'])
            f.write(requests.get(url,headers).text)


class MinzuPipeline(object):
    def process_item(self, item, spider):
        # path=os.getcwd()+"\\"+item['city_name']+"\\"+item['year']+"\\"+item['type_name']
        # file_name_path=path+"\\"+item['file_name']+"."+item['content_type']
        # mkdir(path)
        # print('正在下载',file_name_path)
        # url=item['url']
        # content_type=item['content_type']
        # downld(file_name_path,url,content_type)
        return item
