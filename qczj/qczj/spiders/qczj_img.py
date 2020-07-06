# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from qczj.items import QczjItem


class QczjImgSpider(CrawlSpider):
    name = 'qczj_img'
    allowed_domains = ['autohome.com.cn']
    start_urls = ['https://www.autohome.com.cn/beijing/']

    rules = (
        Rule(LinkExtractor(allow=r'https://car.autohome.com.cn/\d+.html'),follow=False),
        Rule(LinkExtractor(allow=r'https://car.autohome.com.cn/pic/series/.+'), callback='parse_item', follow=True),

    )

    def parse_item(self, response):
        name = response.xpath("//div[@class='cartab-title']/h2/a/text()").get()
        type = response.xpath("//div[@class='uibox']/div/text()").get()
        srcs = response.xpath("//div[@class='uibox']/div[@class='uibox-con carpic-list03 border-b-solid']/ul/li/a/img/@src").getall()
        srcs = list(map(lambda x:response.urljoin(x), srcs))
        srcs = list(map(lambda x:x.replace('240x180_0_q95_c42_',''), srcs))
        item = QczjItem(name=name, type=type, image_urls=srcs)
        yield item
