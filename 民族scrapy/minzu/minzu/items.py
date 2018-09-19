# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html
import scrapy
class Minzu_ningxia_Item(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    year=scrapy.Field()
    type_name=scrapy.Field()
    file_name=scrapy.Field()
    url=scrapy.Field()
    city_name=scrapy.Field()