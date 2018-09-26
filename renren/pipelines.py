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

# 下面的这个管道文件是默认生成的管道文件
# class RenrenPipeline(object):
#     def __init__(self):                 # 这个也不是必须的函数
#         self.file = codecs.open('wanman.json', 'wb', encoding='utf-8')
#
#     def process_item(self, item, spider):     # 这个是必须的函数，必须有！
#         text = json.dumps(dict(item), ensure_ascii=False) + '\n'
#         # 这里面如果在json的文本里面有中文，或者不是英文f的语言，必须加上ensure_sccii=False，  将其转换成unicode万国格式
#         self.file.write(text)
#         return item
#
#     def close_spider(self, spider):          # 这个不是必须的一个函数，可有可无
#         self.file.close()
#         # spider (Spider 对象) – 被关闭的spider
#         # 可选实现，当spider被关闭时，这个方法被调用

# 下面的是使用的scrapy的一个内置的下载图片的内置的类，只需要拿来用就可以了，其实也可以原生的管道文件，然后用requests.get(url)也是可以用来下载图片的！
class ImagesPipeline(ImagesPipeline):
    IMAGES_STORE = get_project_settings().get('IMAGES_STORE')   # 初始化保存图片的地址，这个是在settings里面设置过的！
    path = get_project_settings().get("IMAGES_STORE")
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.26 Safari/537.36 Core/1.63.5733.400 QQBrowser/10.2.2050.400',

        'Referer': 'https://global.toomics.com'}

    def get_media_requests(self, item, info):
        images_url = item['url']
        yield scrapy.Request(url=images_url, headers=self.headers)          # 由于toomics添加了反爬虫的机制，需要加上referer，所以就加了一个headers

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
    """
        这里面及遇到了一个很困难的问题，就是由于虽然便宜scrapy是采用异步下载的机制，这就导致不能使用num自增的方式给图片命名
        后来就只只有想到了，通过链接中的img的编号提取出来用来个图片命名，虽然成功了，这个方法有一定的局限性，如果没有链接没有任何的
        数字的来和图片进行匹配的话，那就不知道该怎么做了！后面的好好的研究一下！
    
    """
