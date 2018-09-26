# -*- coding: utf-8 -*-
import scrapy
from renren.items import RenrenItem


class ReSpider(scrapy.Spider):
    name = 're'
    allowed_domains = ['global.toomics.com']
    start_urls = ['https://global.toomics.com/sc/auth/layer_login']
    num = 0
    test_num = 0
    # cookies = {'ln_hurl': 'http://head.xiaonei.com/photos/0/0/men_main.gif',
    #          'ap': '967740533',
    #          'wp_fold': '0"',
    #          'jebecookies': '2ffc4a3d-8e05-4c2a-af1a-40960cdef767|||||',
    #          '"anonymid': 'jksc2aplorpv5r',
    #          't': 'aa6bb5f38255af9e32204731c306d9f63',
    #          'loginfrom': 'syshome',
    #          'id': '967743',
    #          'ln_uact': '13821529212',
    #          'JIONID': 'abcbR5rw_QRGOaLInqlyw',
    #          'Hm_lvt_966bff0a868cd407a416b4e3993b9dc8': '1535237560',
    #          'depovince': 'TJ',
    #          'first_flag': '1',
    #          'societyguester': 'aa6bb5f38255af9e32204731c306d9f63',
    #          'Hm_lvt_cdce8cda34e84469b1c8015204129522': '1535194719,1535237359,1535237549,1535237699',
    #          '_ga': 'GA1.3.1542009556.1535237372',
    #          '_de': '68D3D8C071391578E75C84E9EBB280ED',
    #          '_r01_': '1',
    #          '__utma': '151146938.1542009556.1535237372.1535237372.1535237372.1',
    #          'ick_login': '0439081a-855b-4199-a52e-e664d06cb0f8',
    #          'xnsid': 'f4bf264f',
    #          'p': '0bc16a4920f783a9f39bcdd55450a0033',
    #          '__utmz': '151146938.1535237372.1.1.utmcsr=renren.com|utmccn=(referral)|utmcmd=referral|utmcct=/967740533'}
    # cookies = {'GTOOMICScountry': 'CN', 'GTOOMICScisession': 'a%3A6%3A%7Bs%3A10%3A%22session_id%22%3Bs%3A32%3A%22bb2d1706aadfe40d39d8566f43d92f62%22%3Bs%3A10%3A%22ip_address%22%3Bs%3A11%3A%2259.67.0.183%22%3Bs%3A10%3A%22user_agent%22%3Bs%3A114%3A%22Mozilla%2F5.0+%28Windows+NT+10.0%3B+Win64%3B+x64%29+AppleWebKit%2F537.36+%28KHTML%2C+like+Gecko%29+Chrome%2F67.0.3396.87+Safari%2F537.36%22%3Bs%3A13%3A%22last_activity%22%3Bi%3A1537789357%3Bs%3A11%3A%22keep_cookie%22%3Bs%3A1%3A%221%22%3Bs%3A7%3A%22display%22%3Bs%3A1%3A%22A%22%3B%7D711a2ce177637ffd038c5781708f52b9a39f6861', 'Hm_lvt_cdce8cda34e84469b1c8015204129522': '1535463555', 'GTOOMICSpid_join': 'pid%3DdefaultPid%26subpid%3DdefaultSubPid%26channel%3DdefaultChannel', 'content_lang': 'zh_cn', 'GTOOMICSremember_id': 'a%3A2%3A%7Bs%3A7%3A%22user_id%22%3Bs%3A17%3A%221031003342%40qq.com%22%3Bs%3A3%3A%22key%22%3Bs%3A32%3A%2219a93c70774fbaacaf09952e09733914%22%3B%7D', 'GTOOMICSpidIntro': '1', 'GTOOMICSpid_last': 'pid%3DdefaultPid%26subpid%3DdefaultSubPid%26channel%3DdefaultChannel', 'GTOOMICSslave': 'sdb2', '_ga': 'GA1.2.617503066.1533299855'}

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.FormRequest(url=url, formdata={"user_id": "1031003342@qq.com", "user_pw": "yier5719", "save_user_id": "1", "keep_cookie": "1",
                                                            "returnUrl": "/sc/", "direction": "N"}, callback=self.parse)
#             yield scrapy.FormRequest(url, cookies = self.cookies, callback = self.parse_page)
# 上面的是用cookies进行登录的但是必须在settings里面更改一下设置


    def parse(self, response):
        print('开始登陆中。。。。')
        # self.num += 1
        # with open('my%s.html' % self.num, 'wb') as f:
        #     f.write(response.body)

        yield scrapy.Request(url='https://global.toomics.com/sc/webtoon/episode/toon/4651',
                             callback=self.change_link)
        print('登陆成功。。。')

    def change_link(self, response):
        for link in response.xpath("//li[@class='normal_ep ']/a/@onclick"):
            link = 'https://global.toomics.com' + link.extract().split("'")[-2]
            print(link)
            yield scrapy.Request(url=link, callback=self.content_parse)

    def content_parse(self, response):
        for each in response.xpath('//div[@class="viewer-imgs"]/div/img'):
            item = RenrenItem()
            item['url'] = each.xpath('./@data-original').extract()[0]
            # print(item['url'])
            item['number'] = each.xpath('./@id').extract()[0].split('_')[-1]  # 图片的编码数字
            item['name'] = item['url'].split('/')[-2] + '_' + item['number']    # 图片的名字有章节和图片的编号组成1_1
            yield item
