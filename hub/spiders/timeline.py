# -*- coding: utf-8 -*-
import scrapy
from scrapy import Selector


class TimelineSpider(scrapy.Spider):
    name = 'timeline'
    allowed_domains = ['noomsaotours.co.th']
    start_urls = ['https://www.noomsaotours.co.th/%E0%B8%97%E0%B8%B1%E0%B8%A7%E0%B8%A3%E0%B9%8C%E0%B9%83%E0%B8%99%E0%B8%9B%E0%B8%A3%E0%B8%B0%E0%B9%80%E0%B8%97%E0%B8%A8/%E0%B8%81%E0%B8%A5%E0%B8%B2%E0%B8%87/%E0%B9%81%E0%B8%95%E0%B9%88%E0%B8%87%E0%B9%84%E0%B8%97%E0%B8%A2%E0%B8%99%E0%B8%B1%E0%B9%88%E0%B8%87%E0%B8%A3%E0%B8%96%E0%B9%84%E0%B8%9F%E0%B9%84%E0%B8%9B%E0%B8%87%E0%B8%B2%E0%B8%99%E0%B9%81%E0%B8%9C%E0%B9%88%E0%B8%99%E0%B8%94%E0%B8%B4%E0%B8%99%E0%B8%AA%E0%B8%A1%E0%B9%80%E0%B8%94%E0%B9%87%E0%B8%88%E0%B8%9E%E0%B8%A3%E0%B8%B0%E0%B8%99%E0%B8%B2%E0%B8%A3%E0%B8%B2%E0%B8%A2%E0%B8%93%E0%B9%8C-@-%E0%B8%A5%E0%B8%9E%E0%B8%9A%E0%B8%B8%E0%B8%A3%E0%B8%B5/208']
    #start_urls = ['https://www.noomsaotours.co.th/%E0%B8%97%E0%B8%B1%E0%B8%A7%E0%B8%A3%E0%B9%8C%E0%B9%83%E0%B8%99%E0%B8%9B%E0%B8%A3%E0%B8%B0%E0%B9%80%E0%B8%97%E0%B8%A8/%E0%B8%AD%E0%B8%B5%E0%B8%AA%E0%B8%B2%E0%B8%99/%E0%B8%9A%E0%B8%B1%E0%B8%A7%E0%B9%81%E0%B8%94%E0%B8%87%E0%B8%9E%E0%B8%B2%E0%B9%80%E0%B8%9E%E0%B8%A5%E0%B8%B4%E0%B8%99-%E0%B8%AD%E0%B8%B1%E0%B8%A8%E0%B8%88%E0%B8%A3%E0%B8%A3%E0%B8%A2%E0%B9%8C%E0%B8%98%E0%B8%A3%E0%B8%A3%E0%B8%A1%E0%B8%8A%E0%B8%B2%E0%B8%95%E0%B8%B4%E0%B8%AB%E0%B8%B4%E0%B8%99%E0%B8%AA%E0%B8%B2%E0%B8%A1%E0%B8%A7%E0%B8%B2%E0%B8%AC/215']
    counter = 0

    def parse(self, response):
        text = response.xpath('//ul[@class="lhs"]/li').extract()
        timeline = {}
        for day, li in enumerate(text):
            sel = Selector(text=li)
            detail = sel.xpath('.//span/text()').extract()[0]
            if 'เงื่อนไข' not in detail and 'อัตราค่าบริการ' not in detail:
                timeline['day'] = day + 1
                timeline['detail'] = detail 

                description = []
                sel = sel.xpath('.//table[@class="MsoTableGrid"]/tbody/tr/td | \
                                       .//table[@class="LightGrid-Accent11"]/tbody/tr/td').extract()
                temp = {}
                for idx, row in enumerate(sel):
                    selP = Selector(text=row).xpath('//p[@class="MsoNormal"]//text()').extract()
                    selP = ''.join(selP)
                    if idx % 2 == 0:
                        if idx != 0:
                            description.append(temp)
                            temp = {}
                        temp['time'] = selP
                    else:
                        temp['activity'] = selP
                description.append(temp)
                timeline['description'] = description
                print(timeline)
