# -*- coding: utf-8 -*-
import scrapy
# from scrapy.spiders import Rule
# from scrapy.linkextractors import LinkExtractor
from mySpider.items import MyspiderItem
from scrapy_splash import SplashRequest


class JiayuanSpider(scrapy.Spider):
    name = 'jiayuan'
    allowed_domains = ['jiayuan.com']

    url = 'http://search.jiayuan.com/v2/index.php?key=&sex=f&key=&stc=1:35,2:20.28,6:1,23:1&sn=default&sv=1&p='
    a = 1
    url2 = '&f=select&listStyle=bigPhoto&pri_uid=0&jsversion=v5'
    # start_urls = [url + str(a) + url2]
    # start_urls = ['http://www.jiayuan.com/102138385?fxly=search_v2']
    # url3 = url + str(a) + url2
    # url3 = 'http://search.jiayuan.com/v2/index.php?key=&sex=f&stc=1:35,2:20.28,23:1,6:1&sn=default&sv=1&p=2&pt=229&ft=off&f=select&mt=d'

    def start_requests(self):
        for linx in range(1, 10):
            url3 = self.url + str(linx) + self.url2
            print("加载第------" + str(linx) + "-------页数据")
            yield SplashRequest(url3, callback=self.splash_parse, args={'images':0})

    def splash_parse(self, response):
        print("加载大类页面提取个人主页URL并放入下载器:")
        links = response.xpath("//li[@style='z-index: 1;']//div[@class='user_name']/a/@href").extract()
        for link in links:
            yield scrapy.Request(link, callback=self.parse)
        # contenlink = LinkExtractor(allow=(r'jiayuan.com/\d+?fxly=search_v2'))
        # rules = [Rule(contenlink, )]

    def parse(self, response):
        item = MyspiderItem()
        # item['img_name'] = response.xpath("//td//img/@_src").extract()[0][-4:5]
        item['name'] = response.xpath('//div[@class="member_layer_con yh"]/h4/text()').extract()[0]
        # 自我介绍
        item['js'] = response.xpath("//div[@class='js_text']/text()").extract()[0]
        # 兴趣爱好
        # item['list'] = response.xpath("//div[@class='list_a fn-clear']").extract()[0]
        # 要求
        item['yq'] = response.xpath("//div[@class='bg_white mt15'][2]//ul[@class='js_list fn-clear']/li[@class='fn-clear']/div/text()").extract()
        # 生活方式
        item['shfs'] = response.xpath("//div[@class='content_705']/div[6]/div/ul/li/div/em/text()").extract()
        # 工作学习
        item['gzxx'] = response.xpath("//div[@class='content_705']/div[8]/div/ul/li/div/em/text()").extract()
        # 图片
        item['img'] = response.xpath("//td//img/@_src").extract()
        print("加载个人主页并提取数据:-------------:" + str(item['name']))
        # print("*-*" * 10)
        # print(item['name'])
        # print(item['js'])
        # print(item['list'])
        # print(item['yq'])
        # print(item['shfs'])
        # print(item['gzxx'])
        # print(item['img'])
        yield item



