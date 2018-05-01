# -*- coding: utf-8 -*-
import re
import scrapy
import datetime
import urllib 
from scrapy import Selector
from hub.items import Package


class TTTSpider(scrapy.Spider):
    name = 'ttt'
    allowed_domains = ['thai.tourismthailand.org']
    start_urls = ['https://thai.tourismthailand.org/%E0%B9%82%E0%B8%9B%E0%B8%A3%E0%B9%82%E0%B8%A1%E0%B8%8A%E0%B8%B1%E0%B9%88%E0%B8%99/%E0%B8%97%E0%B8%B1%E0%B8%A7%E0%B8%A3%E0%B9%8C%E0%B9%81%E0%B8%A5%E0%B8%B0%E0%B9%81%E0%B8%9E%E0%B9%87%E0%B8%81%E0%B9%80%E0%B8%81%E0%B8%88%E0%B8%97%E0%B9%88%E0%B8%AD%E0%B8%87%E0%B9%80%E0%B8%97%E0%B8%B5%E0%B9%88%E0%B8%A2%E0%B8%A7?page=1']
    # start_urls = ['https://thai.tourismthailand.org/%E0%B9%82%E0%B8%9B%E0%B8%A3%E0%B9%82%E0%B8%A1%E0%B8%8A%E0%B8%B1%E0%B9%88%E0%B8%99/%E0%B8%97%E0%B8%B1%E0%B8%A7%E0%B8%A3%E0%B9%8C%E0%B9%81%E0%B8%A5%E0%B8%B0%E0%B9%81%E0%B8%9E%E0%B9%87%E0%B8%81%E0%B9%80%E0%B8%81%E0%B8%88%E0%B8%97%E0%B9%88%E0%B8%AD%E0%B8%87%E0%B9%80%E0%B8%97%E0%B8%B5%E0%B9%88%E0%B8%A2%E0%B8%A7/%E0%B8%AA%E0%B8%B5%E0%B8%AA%E0%B8%B1%E0%B8%99%E0%B8%95%E0%B8%B0%E0%B8%A7%E0%B8%B1%E0%B8%99%E0%B8%AD%E0%B8%AD%E0%B8%81%E2%80%93%E0%B9%80%E0%B8%81%E0%B8%B2%E0%B8%B0%E0%B8%AA%E0%B8%B5%E0%B8%8A%E0%B8%B1%E0%B8%87%E2%80%93%E0%B9%80%E0%B8%81%E0%B8%B2%E0%B8%B0%E0%B9%80%E0%B8%AA%E0%B8%A1%E0%B9%87%E0%B8%94%E2%80%93%E0%B9%80%E0%B8%81%E0%B8%B2%E0%B8%B0%E0%B8%8A%E0%B9%89%E0%B8%B2%E0%B8%87%E2%80%93%E0%B8%9E%E0%B8%B1%E0%B8%97%E0%B8%A2%E0%B8%B2%E2%80%93%E0%B8%A3%E0%B8%B0%E0%B8%A2%E0%B8%AD%E0%B8%87%E2%80%93%E0%B8%88%E0%B8%B1%E0%B8%99%E0%B8%97%E0%B8%9A%E0%B8%B8%E0%B8%A3%E0%B8%B5%E2%80%93%E0%B8%95%E0%B8%A3%E0%B8%B2%E0%B8%94-4-%E0%B8%A7%E0%B8%B1%E0%B8%99-3-%E0%B8%84%E0%B8%B7%E0%B8%99--217']
    package_urls = []
    page_urls = []
    page = 0
    total_package = 0
    total_page = 0

    #def parse(self, response):
    #    package = create_package(response)
    #    yield package

    def parse(self, response):
        current_page = 'https://thai.tourismthailand.org/โปรโมชั่น/ทัวร์และแพ็กเกจท่องเที่ยว?page='
        page = response.xpath('///ul[@class="pagination"]/li[11]/a/@href').extract_first()
        page = re.search('page=(.*)', page).group(1)
        self.total_page = int(page)
        for i in range(self.total_page):
            self.page_urls.append(current_page + str(i + 1))
        for href in self.page_urls:
            yield response.follow(href, callback=self.get_package_url)
        
    def get_package_url(self, response):
        self.page += 1
        package_urls = response.xpath('//div[@class="col-sm-6"]//div[@class="text"]//@href').extract()
        for url in package_urls:
            if url.find('cat_id') == -1:
                self.package_urls.append(url)
        if(self.page == self.total_page):
            for href in self.package_urls:
                yield response.follow(href, callback=self.get_package)

    def get_package(self, response):
       self.total_package += 1
       print('Processing Package: ' + str(self.total_package))
       package = create_package(response)
       yield package

def process_timeline(response):
    text = response.xpath('//div[@class="tab_container"]/div').extract()
    return timeline

def getInfo(response):
    info = []
    temp = response.xpath('//div[@class="col-md-9"]/div[1]//text()').extract()
    for item in temp:
        item = item.replace('\t', '')
        item = item.replace('\n', '')
        if item != '':
            info.append(item)
    return info

def getPrice(price):
    price = price.split('-')[0]
    try:
        price = price[:price.index('.')]
    except ValueError:
        print('Price text doesnt contain \'.\'')
    if len(re.findall(r'\d', price)) > 0:
        price = int(''.join(re.findall(r'\d', price.split('-')[0])))
    return price

def getDetail(response):
    detail = response.xpath('//*[@id="tab-reviews"]/div/p/text()').extract()
    detail2 = response.xpath('//div[@class="col-md-3"]/p//text()').extract()
    temp = []
    for item in detail:
        item = item.strip()
        if item != '':
            temp.append(item)
    temp2 = []
    for item in detail2:
        item = item.replace(',', '').replace(':', '')
        item = item.strip()
        if item != '' and item != 'หมวดหมู่':
            temp2.append(item)

    temp[0] = temp[0] + ' '+ ' '.join(temp2)
    return temp[0]

def getTimeline(response):
    timeline = response.xpath('//div[@class="tab-part"]/p//text()').extract()
    temp = []
    for item in timeline:
        item = item.strip()
        if item != '':
            temp.append(item)
    try:
        timeline = []
        temp = temp[temp.index('กำหนดการเดินทาง :') + 1:-2]
        day = 1
        for i in range(0, len(temp), 2):
            item = {
                'day': day,
                'detail': temp[i],
                'description': [{
                        'time': '',
                        'activity': temp[i-1]
                    }
                ]
            }
            timeline.append(item)
            day += 1
    except ValueError:
        print('Error no index')
    return timeline

def create_package(response):
    info = getInfo(response)
    package_name = response.xpath('//span[@class="h2 text-center"]/text()').extract_first()
    image = response.xpath('//div[@class="overview-photo"]//a/@href').extract()
    url = urllib.parse.unquote(response.request.url)

    package = Package()
    package['timeline'] = getTimeline(response)
    package['detail'] = getDetail(response)
    package['price'] = getPrice(info[1])
    package['image_urls'] = image
    package['company'] = 'ททท'
    package['logo'] = '/images/image-1525183855295.jpg'
    package['package_name'] = package_name
    package['url'] = response.request.url
    package['travel_date'] = 'N/A'

    if(len(info) > 3):
        package['travel_duration'] = info[3]
    if isinstance(package['price'], int): 
        package['human_price'] = '{:,}'.format(package['price'])
    else: 
        del package['price']
        package['human_price'] = 'N/A'

    return package

