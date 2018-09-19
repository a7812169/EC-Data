# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import os
from .spiders.public import mkdir
import requests
class MinzuPipeline(object):
    def process_item(self, item, spider):
        path=os.getcwd()+"\\"+item['city_name']+"\\"+item['year']+"\\"+item['type_name']
        file_name_path=path+"\\"+item['file_name']+".html"
        mkdir(path)
        with open(file_name_path,"wb")as f:
            f.write(requests.get(item['url']).content)
        return item
