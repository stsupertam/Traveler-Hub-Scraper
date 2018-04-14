# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class Package(scrapy.Item):
    package_name = scrapy.Field() 
    url = scrapy.Field()
    travel_duration = scrapy.Field()
    travel_date = scrapy.Field()
    start_travel_date = scrapy.Field()
    end_travel_date = scrapy.Field()
    price = scrapy.Field()
    human_price = scrapy.Field()
    image_urls = scrapy.Field()
    images = scrapy.Field()
    company = scrapy.Field()
    logo = scrapy.Field()
    detail = scrapy.Field()
    timeline = scrapy.Field()
    region = scrapy.Field()
    provinces = scrapy.Field()
    timeline = scrapy.Field()
    tags = scrapy.Field()
    text = scrapy.Field()
    travel_types = scrapy.Field()