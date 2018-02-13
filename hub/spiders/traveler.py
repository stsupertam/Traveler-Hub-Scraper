# -*- coding: utf-8 -*-
import re
import scrapy
from scrapy import Selector
from hub.items import Package


class TravelerSpider(scrapy.Spider):
    name = 'traveler'
    allowed_domains = ['noomsaotours.co.th']
    start_urls = ['https://www.noomsaotours.co.th/ทัวร์ในประเทศ']
    package_urls = []
    #start_urls = ['https://www.noomsaotours.co.th/%E0%B8%97%E0%B8%B1%E0%B8%A7%E0%B8%A3%E0%B9%8C%E0%B9%83%E0%B8%99%E0%B8%9B%E0%B8%A3%E0%B8%B0%E0%B9%80%E0%B8%97%E0%B8%A8/%E0%B9%83%E0%B8%95%E0%B9%89/%E0%B9%80%E0%B8%95%E0%B9%87%E0%B8%A1%E0%B8%AD%E0%B8%B4%E0%B9%88%E0%B8%A1%E0%B8%81%E0%B8%B1%E0%B8%9A%E0%B8%A1%E0%B8%B1%E0%B8%A5%E0%B8%94%E0%B8%B5%E0%B8%9F%E0%B8%AA%E0%B9%8C%E0%B9%80%E0%B8%A1%E0%B8%B7%E0%B8%AD%E0%B8%87%E0%B9%84%E0%B8%97%E0%B8%A2-%E0%B8%95%E0%B8%B0%E0%B8%A3%E0%B8%B8%E0%B9%80%E0%B8%95%E0%B8%B2-%E0%B8%AB%E0%B8%A5%E0%B8%B5%E0%B9%80%E0%B8%9B%E0%B9%8A%E0%B8%B0-%E0%B8%AB%E0%B8%B2%E0%B8%94%E0%B9%83%E0%B8%AB%E0%B8%8D%E0%B9%88/207']
    #package_urls = ['https://www.noomsaotours.co.th/%E0%B8%97%E0%B8%B1%E0%B8%A7%E0%B8%A3%E0%B9%8C%E0%B9%83%E0%B8%99%E0%B8%9B%E0%B8%A3%E0%B8%B0%E0%B9%80%E0%B8%97%E0%B8%A8/%E0%B9%83%E0%B8%95%E0%B9%89/%E0%B9%80%E0%B8%95%E0%B9%87%E0%B8%A1%E0%B8%AD%E0%B8%B4%E0%B9%88%E0%B8%A1%E0%B8%81%E0%B8%B1%E0%B8%9A%E0%B8%A1%E0%B8%B1%E0%B8%A5%E0%B8%94%E0%B8%B5%E0%B8%9F%E0%B8%AA%E0%B9%8C%E0%B9%80%E0%B8%A1%E0%B8%B7%E0%B8%AD%E0%B8%87%E0%B9%84%E0%B8%97%E0%B8%A2-%E0%B8%95%E0%B8%B0%E0%B8%A3%E0%B8%B8%E0%B9%80%E0%B8%95%E0%B8%B2-%E0%B8%AB%E0%B8%A5%E0%B8%B5%E0%B9%80%E0%B8%9B%E0%B9%8A%E0%B8%B0-%E0%B8%AB%E0%B8%B2%E0%B8%94%E0%B9%83%E0%B8%AB%E0%B8%8D%E0%B9%88/207']
    counter = 0

    def parse(self, response):
        if not self.package_urls:
            self.package_urls = response.xpath('//div[@class="tour_des_first1"]/div/a/@href').extract()
        else:
            self.counter += 1
            #print('Processing Package: ' + str(self.counter))
            package = create_package(response)
            yield package
        for href in self.package_urls:
            yield response.follow(href, callback=self.parse)

def process_date(date_text):
    th_month = [
        'ม.ค.', 'ก.พ.', 'มี.ค.',
        'เม.ย', 'พ.ค.', 'มิ.ย.',
        'ก.ค.', 'ส.ค.', 'ก.ย.',
        'ต.ค.', 'พ.ย.', 'ธ.ค.'
    ]
    start_date = ''
    end_date = ''
    month = ''
    year = ''
    travel_date = {'start': '', 'end': ''}
    if re.findall(r'\d\d', date_text):
        temp = re.findall(r'\d\d', date_text)
        start_date = temp[0]
        end_date = temp[1]
        year = str(int('25' + temp[2]) - 543) 
    if re.findall('[\u0E01-\u0E2E].\.[\u0E00-\u0E07].', date_text):
        month = th_month.index(re.findall('[\u0E01-\u0E47].\.[\u0E00-\u0E47].', date_text)[0])+1
    if(start_date and month and year):
        if(start_date > end_date):
            travel_date['start'] = '%s-%s-%s' % (start_date, str(month - 1), year)
        else:
            travel_date['start'] = '%s-%s-%s' % (start_date, str(month), year)
        travel_date['end'] = '%s-%s-%s' % (end_date, str(month), year)
    return travel_date

def process_detail(text):
    text = text[4:]
    text = ''.join(text)
    return text

def process_timeline(response):
    text = response.xpath('//ul[@class="lhs"]/li').extract()
    timeline = []
    for day, li in enumerate(text):
        sel = Selector(text=li)
        detail = sel.xpath('.//span/text()').extract()[0]
        if 'เงื่อนไข' not in detail and 'อัตราค่าบริการ' not in detail:
            temp = {}
            temp['day'] = day + 1
            temp['detail'] = detail
            temp['description'] = []

            sel = sel.xpath('.//table/tbody/tr/td').extract()
            temp2 = {}
            temp_idx = 0
            for idx, row in enumerate(sel):
                temp_idx = idx
                selP = Selector(text=row).xpath('//p[@class="MsoNormal"]//text()').extract()
                selP = ''.join(selP)
                if temp_idx % 2 == 0:
                    if idx != 0:
                        #description.append(temp)
                        temp['description'].append(temp2)
                        temp2 = {}
                    temp2['time'] = selP
                else:
                    temp2['activity'] = selP
            #description.append(temp)
            timeline.append(temp)
            #timeline['description'].append(description)
    return timeline

def create_package(response):
    text = response.xpath('//div[@class="eight columns  "]/div//text()').extract()
    text = [item for item in text if not re.match('\n.*|\r\n.*| .*|เดินทาง', item)]
    package = Package()
    package['image'] = response.xpath('//div[@class="slide"]/img/@src').extract_first()
    package['company'] = 'noomsaotours'
    package['logo'] = 'https://www.picz.in.th/images/2018/01/26/logoab.jpg'
    package['package_name'] = text[0] or ''
    package['url'] = response.request.url
    if re.search(r'\d', text[1]):
        package['travel_duration'] = int(re.search(r'\d', text[1])[0]) or ''
    if re.search(r'\d.*', text[2]):
        package['travel_date'] = re.search(r'\d.*', text[2])[0]
        travel_date = process_date(package['travel_date'])
        package['start_travel_date'] = travel_date['start']
        package['end_travel_date'] = travel_date['end']
    if(re.findall(r'\d', text[3])):
        package['price'] = int(''.join(re.findall(r'\d', text[3]))) or 0
        package['human_price'] = re.search(r'\d.*', text[3])[0] or ''
    package['detail'] = process_detail(text) 
    package['timeline'] = process_timeline(response)

    return package
