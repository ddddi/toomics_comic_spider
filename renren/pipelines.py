# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
# import json
# import codecs
from scrapy.utils.project import get_project_settings
from scrapy.pipelines.images import ImagesPipeline
import scrapy
import os


# class RenrenPipeline(object):
#     def __init__(self):
#         self.file = codecs.open('wanman.json', 'wb', encoding='utf-8')
#
#     def process_item(self, item, spider):
#         text = json.dumps(dict(item), ensure_ascii=False) + '\n'
#         # 这里面如果在json的文本里面有中文，或者不是英文f的语言，必须加上ensure_sccii=False，  将其转换成unicode万国格式
#         self.file.write(text)
#         return item
#
#     def close_spider(self, spider):
#         self.file.close()
#         # spider (Spider 对象) – 被关闭的spider
#         # 可选实现，当spider被关闭时，这个方法被调用

class ImagesPipeline(ImagesPipeline):
    IMAGES_STORE = get_project_settings().get('IMAGES_STORE')   # 初始化保存图片的地址
    path = get_project_settings().get("IMAGES_STORE")
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.26 Safari/537.36 Core/1.63.5733.400 QQBrowser/10.2.2050.400',

        'Referer': 'https://global.toomics.com'}

    def get_media_requests(self, item, info):
        images_url = item['url']
        yield scrapy.Request(url=images_url, headers=self.headers)

    def item_completed(self, result, item, info):
        image_path = [x['path'] for ok, x in result if ok]
        chapter = item['url'].split('/')[-2]  #
        print(chapter)
        if int(chapter) < 10:
            self.IMAGES_STORE = self.path + '/' + '0' + chapter  # 生成对应章节的文件夹的路径
        else:
            self.IMAGES_STORE = self.path + '/' + chapter  # 生成对应章节的文件夹的路径
        if not os.path.exists(self.IMAGES_STORE):
            os.makedirs(self.IMAGES_STORE)
        if int(item['number']) < 10:
            os.rename(self.path + '/' + image_path[0], self.IMAGES_STORE + '/' + '00' + str(int(item['number']) + 1) + '.jpg')
        elif int(item['number']) < 100:
            os.rename(self.path + '/' + image_path[0], self.IMAGES_STORE + '/' + '0' + str(int(item['number']) + 1) + '.jpg')
        else:
            os.rename(self.path + '/' + image_path[0], self.IMAGES_STORE + '/' + str(int(item['number']) + 1) + '.jpg')