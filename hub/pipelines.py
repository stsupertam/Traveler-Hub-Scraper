# -*- coding: utf-8 -*-
import pymongo
import csv
import logging
import os
from scrapy.conf import settings
from dictionary import *
from pythainlp.tokenize import word_tokenize
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
        with open('../dictionary/word_cut.txt', 'r', encoding='utf8') as file:
            file = file.readlines()
        longest_word = len(max(file, key=len))
        for timeline in item['timeline']:
            text = text + ' ' + timeline['detail']
            for des in timeline['description']:
                text = text + ' ' + des['activity']
        
        text = text.replace('จ.', '').replace('จังหวัด','').replace('ฯ', '').replace('อ.', '').replace('"', '')
        text = dict_word_tokenize(text, '../dictionary/word_cut.txt', 'mm')
        text = [word for word in text if word not in stopwords]
        cut_text = []
        for word in text:
            if(word in fix):
                word = fix[word]
            if(word in provinces):
                item['provinces'].append(word)
                item['region'] = provinces[word]
            if(word in tags):
                item['tags'].append(word)
            if(len(word) > longest_word):
                cut_text = cut_text + word_tokenize(word, 'deepcut')
            else:
                cut_text.append(word)

        item['text'] = cut_text
        item['provinces'] = list(set(item['provinces']))
        item['tags'] = list(set(item['tags']))

        self.collection.insert(dict(item))
        logging.info('Package %d added to MongoDB successfully', self.counter)
        return item
