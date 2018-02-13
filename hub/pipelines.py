# -*- coding: utf-8 -*-
import pymongo
import csv
import logging
from scrapy.conf import settings
from dictionary import provinces
from dictionary import tags
from pythainlp.tokenize import dict_word_tokenize
#from pythainlp.tokenize import word_tokenize

class MongoDBPipeline(object):
    def __init__(self):
        connection = pymongo.MongoClient(
            settings['MONGODB_SERVER'],
            settings['MONGODB_PORT']
        )
        db = connection[settings['MONGODB_DB']]
        self.collection = db[settings['MONGODB_COLLECTION']]
        self.counter = 0

    def process_item(self, item, spider):
        self.counter += 1

        item['provinces'] = []
        item['tags'] = []
        item['region'] = ''

        text = item['package_name'] + ' ' + item['detail']
        for timeline in item['timeline']:
            text = text + ' ' + timeline['detail']
        
        item['text'] = text
        for word in dict_word_tokenize(text, 'tag.txt', 'mm'):
            if(word == 'หาดใหญ่'):
                word = 'สงขลา'
            if(word in provinces):
                item['provinces'].append(word)
                item['region'] = provinces[word]
            if(word in tags):
                item['tags'].append(word)
        item['provinces'] = list(set(item['provinces']))
        item['tags'] = list(set(item['tags']))

        self.collection.insert(dict(item))
        logging.info('Package %d added to MongoDB successfully', self.counter)
        return item
