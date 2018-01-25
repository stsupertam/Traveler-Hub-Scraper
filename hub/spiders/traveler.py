# -*- coding: utf-8 -*-
import re
import scrapy
from scrapy import Selector


class TravelerSpider(scrapy.Spider):
    name = 'traveler'
    allowed_domains = ['noomsaotours.co.th']
    start_urls = ['https://www.noomsaotours.co.th/ทัวร์ในประเทศ']
    package_url = []
    counter = 0

    def parse(self, response):
        if not self.package_url:
            self.package_url = response.xpath('//div[@class="tour_des_first1"]/div/a/@href').extract()
        else:
            self.counter += 1
            print(self.counter)
            data = create_package(response)
            yield data
            # extract all strong tag
            #response.xpath('//span/text()').extract()
        for href in self.package_url:
            yield response.follow(href, callback=self.parse)
            if self.counter == 5:
                return

def process_date(date_text):
    th_month = [
        'ม.ค.', 'ก.พ.', 'มี.ค.',
        'เม.ย', 'พ.ค.', 'มิ.ย.',
        'ก.ค.', 'ส.ค.', 'ก.ย.',
        'ต.ค.', 'พ.ย.', 'ธ.ค.'
    ]
    start_date = ''
    start_month = ''
    start_year = ''
    start_travel_date = ''
    if re.search(r'\d\d', date_text):
        start_date = re.search(r'\d\d', date_text)[0]
    if re.search('[\u0E01-\u0E2E].[\u0E00-\u0E07].', date_text):
        start_month = str(th_month.index(re.search('[\u0E01-\u0E2E].[\u0E00-\u0E07].', date_text)[0])+1)
    if re.search(r'\d\d$', date_text):
        start_year = str(int('25' + re.search(r'\d\d$', date_text)[0]) - 543)
    if(start_date and start_month and start_year):
        start_travel_date = '%s-%s-%s' % (start_date, start_month, start_year)
    return start_travel_date

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

            #description = []
            sel = sel.xpath('.//table[@class="MsoTableGrid"]/tbody/tr/td | \
                             .//table[@class="LightGrid-Accent11"]/tbody/tr/td | \
                             .//table[@class="MsoTableLightGridAccent1"]/tbody/tr/td').extract()
            temp2 = {}
            for idx, row in enumerate(sel):
                selP = Selector(text=row).xpath('//p[@class="MsoNormal"]//text()').extract()
                selP = ''.join(selP)
                if idx % 2 == 0:
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
    data = {
        'package_name': '',
        'travel_duration': 0,
        'travel_date': '',
        'start_travel_date': '',
        'price': 0,
        'human_price': ''
    }
    data['image'] = response.xpath('//div[@class="slide"]/img/@src').extract_first()
    data['company_name'] = 'noomsaotours'
    data['logo'] = 'https://www.picz.in.th/images/2018/01/26/logoab.jpg'
    data['package_name'] = text[0]
    if re.search(r'\d', text[1]):
        data['travel_duration'] = int(re.search(r'\d', text[1])[0])
    if re.search(r'\d.*', text[2]):
        data['travel_date'] = re.search(r'\d.*', text[2])[0]
        data['start_travel_date'] = process_date(data['travel_date'])
    if(re.findall(r'\d', text[3])):
        data['price'] = int(''.join(re.findall(r'\d', text[3])))
        data['human_price'] = re.search(r'\d.*', text[3])[0]
    data['detail'] = process_detail(text)
    data['timeline'] = process_timeline(response)

    return data
