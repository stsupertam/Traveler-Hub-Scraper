# -*- coding: utf-8 -*-
import re
import scrapy


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
            text = response.xpath('//div[@class="eight columns  "]/div//text()').extract()
            data = create_package(text)
            yield data
            # extract all strong tag
            #response.xpath('//span/text()').extract()
        for href in self.package_url:
            yield response.follow(href, callback=self.parse)

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

def create_package(text):
    text = [item for item in text if not re.match('\n.*|\r\n.*| .*|เดินทาง', item)]
    data = {
        'package_name': '',
        'travel_duration': 0,
        'travel_date': '',
        'start_travel_date': '',
        'price': 0,
        'human_price': '' 
    }
    data['package_name'] = text[0]
    if re.search(r'\d', text[1]):
        data['travel_duration'] = int(re.search(r'\d', text[1])[0])
    if re.search(r'\d.*', text[2]):
        data['travel_date'] = re.search(r'\d.*', text[2])[0]
        data['start_travel_date'] = process_date(data['travel_date'])
    if(re.findall(r'\d', text[3])):
        data['price'] = int(''.join(re.findall(r'\d', text[3])))
        data['human_price'] = re.search(r'\d.*', text[3])[0]
  
    return data
