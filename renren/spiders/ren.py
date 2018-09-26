# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from renren.items import RenrenItem

"""




 弃用 弃用 弃用 弃用 弃用 弃用 弃用 弃用 弃用 






"""
# 不知道为什么使用crawlspider的模版的时候就是爬取不了，所以就放弃了，改用默认的spide模板！
class RenSpider(CrawlSpider):
    name = 'ren'
    allowed_domains = ['global.toomics.com']
    start_urls = ['https://global.toomics.com/sc/webtoon/episode/toon/4690']
    chapter_link = LinkExtractor(allow=r'/sc/webtoon/detail/code')
    content = LinkExtractor(allow=r'https://toon-g.toomics.com/upload/contents')
    rules = (
        Rule(chapter_link, process_links='change_link', follow=True, callback='parse_content'),
        # Rule(content, callback='parse_content', follow=False),
    )
    def start_requests(self):
        yield

    def change_link(self, links):
        for each in links:
            each.url = 'https://global.toomics.com' + each.url.split("'")[-2]
        return links

    def parse_content(self, response):
        for each in response:
            item = RenrenItem()
            item['url'] = each.url
            print(each)

