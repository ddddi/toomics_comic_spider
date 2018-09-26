# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class RenrenItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    number = scrapy.Field()    # 每一章节的num数字
    url = scrapy.Field()       # 定义图片的链接
    name = scrapy.Field()      # 定义图片的名字