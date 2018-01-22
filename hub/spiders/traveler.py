# -*- coding: utf-8 -*-
from urllib.parse import quote
import scrapy


class TravelerSpider(scrapy.Spider):
    name = 'traveler'
    allowed_domains = ['noomsaotours.co.th']
    start_urls = ['https://www.noomsaotours.co.th/%E0%B8%97%E0%B8%B1%E0%B8%A7%E0%B8%A3%E0%B9%8C%E0%B9%83%E0%B8%99%E0%B8%9B%E0%B8%A3%E0%B8%B0%E0%B9%80%E0%B8%97%E0%B8%A8/']
    package_url = []
    counter = 0

    def parse(self, response):
        if not self.package_url:
            self.package_url = response.xpath('//div[@class="tour_des_first1"]/div/a/@href').extract()
        else:
            self.counter += 1
            print(self.counter)
            print(response.xpath('//div[@class="eight columns  "]/div/h1/text()').extract_first())

        for href in self.package_url:
            yield response.follow(href, callback=self.parse)
