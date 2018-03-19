# -*- coding: utf-8 -*-
import re
import scrapy
import datetime
from scrapy import Selector
from hub.items import Package


class TourtookteeSpider(scrapy.Spider):
    name = 'tourtooktee'
    allowed_domains = ['tourtooktee.com']
    #start_urls = ['http://www.tourtooktee.com/programtour.php?cate=%E0%B8%A0%E0%B8%B2%E0%B8%A2%E0%B9%83%E0%B8%99%E0%B8%9B%E0%B8%A3%E0%B8%B0%E0%B9%80%E0%B8%97%E0%B8%A8']
    start_urls = ['http://www.tourtooktee.com/%E0%B8%97%E0%B8%B1%E0%B8%A7%E0%B8%A3%E0%B9%8C/incnx-02-%E0%B8%AD%E0%B8%B4%E0%B8%99%E0%B8%97%E0%B8%99%E0%B8%99%E0%B8%97%E0%B9%8C-%E0%B8%9B%E0%B8%B2%E0%B8%A2-%E0%B8%AD%E0%B8%A5%E0%B8%B1%E0%B8%87%E0%B8%81%E0%B8%B2%E0%B8%A3%E0%B8%93%E0%B9%8C%E0%B8%87%E0%B8%B2%E0%B8%99%E0%B8%A3%E0%B8%B2%E0%B8%8A%E0%B8%9E%E0%B8%A4%E0%B8%81%E0%B8%A9%E0%B9%8C']
    package_urls = []
    #start_urls = ['https://www.tourtooktee.co.th/%E0%B8%97%E0%B8%B1%E0%B8%A7%E0%B8%A3%E0%B9%8C%E0%B9%83%E0%B8%99%E0%B8%9B%E0%B8%A3%E0%B8%B0%E0%B9%80%E0%B8%97%E0%B8%A8/%E0%B9%83%E0%B8%95%E0%B9%89/%E0%B9%80%E0%B8%95%E0%B9%87%E0%B8%A1%E0%B8%AD%E0%B8%B4%E0%B9%88%E0%B8%A1%E0%B8%81%E0%B8%B1%E0%B8%9A%E0%B8%A1%E0%B8%B1%E0%B8%A5%E0%B8%94%E0%B8%B5%E0%B8%9F%E0%B8%AA%E0%B9%8C%E0%B9%80%E0%B8%A1%E0%B8%B7%E0%B8%AD%E0%B8%87%E0%B9%84%E0%B8%97%E0%B8%A2-%E0%B8%95%E0%B8%B0%E0%B8%A3%E0%B8%B8%E0%B9%80%E0%B8%95%E0%B8%B2-%E0%B8%AB%E0%B8%A5%E0%B8%B5%E0%B9%80%E0%B8%9B%E0%B9%8A%E0%B8%B0-%E0%B8%AB%E0%B8%B2%E0%B8%94%E0%B9%83%E0%B8%AB%E0%B8%8D%E0%B9%88/207']
    #package_urls = ['https://www.tourtooktee.co.th/%E0%B8%97%E0%B8%B1%E0%B8%A7%E0%B8%A3%E0%B9%8C%E0%B9%83%E0%B8%99%E0%B8%9B%E0%B8%A3%E0%B8%B0%E0%B9%80%E0%B8%97%E0%B8%A8/%E0%B9%83%E0%B8%95%E0%B9%89/%E0%B9%80%E0%B8%95%E0%B9%87%E0%B8%A1%E0%B8%AD%E0%B8%B4%E0%B9%88%E0%B8%A1%E0%B8%81%E0%B8%B1%E0%B8%9A%E0%B8%A1%E0%B8%B1%E0%B8%A5%E0%B8%94%E0%B8%B5%E0%B8%9F%E0%B8%AA%E0%B9%8C%E0%B9%80%E0%B8%A1%E0%B8%B7%E0%B8%AD%E0%B8%87%E0%B9%84%E0%B8%97%E0%B8%A2-%E0%B8%95%E0%B8%B0%E0%B8%A3%E0%B8%B8%E0%B9%80%E0%B8%95%E0%B8%B2-%E0%B8%AB%E0%B8%A5%E0%B8%B5%E0%B9%80%E0%B8%9B%E0%B9%8A%E0%B8%B0-%E0%B8%AB%E0%B8%B2%E0%B8%94%E0%B9%83%E0%B8%AB%E0%B8%8D%E0%B9%88/207']
    page_urls = []
    page = 0
    total_package = 0
    total_page = 0

    def parse(self, response):
        package = create_package(response)
        yield package

    #def parse(self, response):
    #    current_page = 'http://www.tourtooktee.com/programtour.php?pn=10&cate=ภายในประเทศ&page='
    #    page = response.xpath('//*[@id="pagination"]/a[3]/@title').extract_first()
    #    self.total_page = int(re.findall(r'\d', page)[0])
    #    for i in range(self.total_page):
    #        self.page_urls.append(current_page + str(i + 1))
    #    for href in self.page_urls:
    #        yield response.follow(href, callback=self.get_package_url)
    #    print(self.page_urls)
    #    
    #def get_package_url(self, response):
    #    self.page += 1
    #    #packages_url = response.x[]
    #    #package_urls = response.xpath('//*[@id="tour_list_wrapper"]/div[1]/div[2]/p/a/@href').extract()
    #    #package_urls = response.xpath('//*[@id="tour_list_wrapper"]/div[@class="txt grid_7"]/h2/a/@href').extract()
    #    package_urls = response.xpath('//div[@class="txt grid_7"]/h2/a/@href').extract()
    #    for url in package_urls:
    #        url = f'http://www.{self.name}.com{url[1:]}'
    #        self.package_urls.append(url)
    #    if(self.page == self.total_page):
    #        for href in self.package_urls:
    #            yield response.follow(href, callback=self.get_package)

    #def get_package(self, response):
    #    self.total_package += 1
    #    package = create_package(response)
    #    yield package

def process_timeline(response):
    text = response.xpath('//div[@class="tab_container"]/div').extract()
    timeline = []
    for day, div in enumerate(text):
        div = div.replace('\n', '').replace('\xa0', '')
        sel = Selector(text=div)
        detail = sel.xpath('.//span/text()').extract()[0].strip()
        temp = {}
        temp['day'] = day + 1
        temp['detail'] = detail
        temp['description'] = []

        sel = sel.xpath('.//table/tbody/tr/td').extract()
        temp2 = {}
        temp_idx = 0
        for idx, row in enumerate(sel):
            temp_idx = idx
            selP = Selector(text=row).xpath('//text()').extract()
            selP = ''.join(selP).strip()
            if temp_idx % 2 == 0:
                if idx != 0:
                    #description.append(temp)
                    temp['description'].append(temp2)
                    temp2 = {}
                temp2['time'] = selP
            else:
                temp2['activity'] = selP
        temp['description'].append(temp2)
        timeline.append(temp)
    return timeline

def create_package(response):
    price = response.xpath('//*[@id="programtour_each_inner"]/p[3]/text()').extract_first()
    detail =  response.xpath('//*[@id="programtour_each_inner"]/p[2]/text()').extract_first()
    #travel_date = response.xpath('//*[@id="programtour_each_inner"]/p[4]/text()').extract_first()

    package = Package()
    package['detail'] = detail.replace(':\r\n', '').lstrip()
    package['image'] = response.xpath('//*[@id="programtour_each_inner"]/div[3]/img/@src').extract_first()
    package['company'] = 'tourtooktee'
    package['logo'] = 'http://supertam.xyz:5000/images/image-1521468799332.jpg'
    package['package_name'] = response.request.url.split('/')[-1] or ''
    package['url'] = response.request.url
    package['price'] = int(''.join(re.findall(r'\d', price.split('-')[0])))
    package['human_price'] = price.replace(': ', '') or 'N/A'
    package['travel_duration'] = 'N/A'
    package['timeline'] = process_timeline(response)

    return package
