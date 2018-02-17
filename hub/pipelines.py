# -*- coding: utf-8 -*-
import pymongo
import csv
import logging
from scrapy.conf import settings
from dictionary import *
from pythainlp.tokenize import dict_word_tokenize
from sshtunnel import SSHTunnelForwarder
from pydispatch import dispatcher
from scrapy import signals

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
        item['tags'] = []
        item['region'] = ''

        text = item['package_name'] + ' ' + item['detail']
        for timeline in item['timeline']:
            text = text + ' ' + timeline['detail']
            for des in timeline['description']:
                text = text + ' ' + des['activity']
        
        text = text.replace('จ.', '').replace('จังหวัด','').replace('ฯ', '').replace('อ.', '').replace('"', '')
        text = dict_word_tokenize(text, 'dictionary/word_cut.txt', 'mm')
        text = [word for word in text if word not in stopwords]
        text = list(set(text))
        for word in text:
            if(word in fix):
                word = fix[word]
            if(word in provinces):
                item['provinces'].append(word)
                item['region'] = provinces[word]
            if(word in tags):
                item['tags'].append(word)
        item['text'] = ' '.join(text)
        item['provinces'] = list(set(item['provinces']))
        item['tags'] = list(set(item['tags']))

        self.collection.insert(dict(item))
        logging.info('Package %d added to MongoDB successfully', self.counter)
        #if(signals.engine_stopped()):
        #    server.close()
        return item
