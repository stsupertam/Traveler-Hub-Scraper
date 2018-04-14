# -*- coding: utf-8 -*-
import pymongo
import csv
import deepcut
import logging
import os
import re
from scrapy.conf import settings
from dictionary import *
from sshtunnel import SSHTunnelForwarder
from pydispatch import dispatcher
from scrapy import signals
from scrapy.exceptions import DropItem
from scrapy.contrib.pipeline.images import ImagesPipeline
from scrapy.exceptions import DropItem
from scrapy.http import Request

class MongoDBPipeline(object):

    def __init__(self):
        if(settings['ENV'] == 'Development'):
            client = pymongo.MongoClient(
                settings['MONGODB_LOCAL'],
                settings['MONGODB_PORT']
            )
        else:
            self.server = SSHTunnelForwarder(
                settings['MONGODB_SERVER'],
                ssh_username=settings['SSH_USER'],
                ssh_password=settings['SSH_PASS'],
                remote_bind_address=('127.0.0.1', 27017)
            )
            self.server.start()
            client = pymongo.MongoClient('127.0.0.1', self.server.local_bind_port) # server.local_bind_port is assigned local port
        db = client[settings['MONGODB_DB']]
        dispatcher.connect(self.close_spider, signals.spider_closed) # NEW
        self.collection = db[settings['MONGODB_COLLECTION']]
        self.counter = 0

    def close_spider(self, spider):
        if(settings['ENV'] != 'Development'):
            self.server.close()

    def process_item(self, item, spider):
        self.counter += 1

        item['provinces'] = []
        item['travel_types'] = []
        item['tags'] = []
        item['region'] = ''

        text = item['package_name'] + ' ' + item['detail']
        for timeline in item['timeline']:
            if(timeline['detail']):
                text = text + ' ' + timeline['detail']
            for des in timeline['description']:
                if(des):
                    text = text + ' ' + des['activity']
        
        text = text.replace('จ.', '').replace('จังหวัด','').replace('ฯ', '').replace('อ.', '').replace('"', '')
        text = re.sub('[a-zA-Z0-9.^&*-=“”:\"\'-\[\]\(\)\{\}]', '', text)
        text = re.sub(' +','', text)
        text = deepcut.tokenize(text, custom_dict='dictionary/word_cut.txt')
        cut_text = []
        for word in text:
            if(word in fix):
                word = fix[word]
            if(word in provinces):
                item['provinces'].append(word)
                item['region'] = provinces[word]
            if(word in travel_types):
                item['tags'].append(word)
                if(travel_types[word] not in item['travel_types']):
                    item['travel_types'].append(travel_types[word])
            if(word not in stopwords and word.strip()):
                cut_text.append(word)

        item['text'] = list(set(cut_text))
        item['provinces'] = list(set(item['provinces']))
        item['tags'] = list(set(item['tags']))

        self.collection.insert(dict(item))
        logging.info('Package %d added to MongoDB successfully', self.counter)
        return item


class DuplicatesPipeline(object):

    def __init__(self):
        self.ids_seen = set()

    def process_item(self, item, spider):
        if item['package_name'] in self.ids_seen:
            raise DropItem("Duplicate item found: %s" % item)
        else:
            self.ids_seen.add(item['package_name'])
            return item


class MyImagesPipeline(ImagesPipeline):

    def get_media_requests(self, item, info):
        for image_url in item['image_urls']:
            yield Request(image_url)

    def item_completed(self, results, item, info):
        image_paths = []
        for ok,x in results:
            if(ok):
                image_paths.append('/images/' + x['path']) 
        if not image_paths:
            raise DropItem("Item contains no images")
        item['images'] = image_paths
        return item
