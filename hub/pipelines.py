# -*- coding: utf-8 -*-
import pymongo
import csv
from scrapy.conf import settings
from pythainlp.tokenize import word_tokenize

class MongoDBPipeline(object):
    def __init__(self):
        connection = pymongo.MongoClient(
            settings['MONGODB_SERVER'],
            settings['MONGODB_PORT']
        )
        db = connection[settings['MONGODB_DB']]
        self.collection = db[settings['MONGODB_COLLECTION']]
        self.region = []
        self.provinces = []
        with open('provinces.csv', 'r', encoding='utf8') as file:
            rows = csv.reader(file)
            for item in rows:
                self.region.append(item[0])
                self.provinces.append(item[1])



    def process_item(self, item, spider):
        item['provinces'] = []
        item['region'] = ''
        text = item['package_name'] + ' ' + item['detail']
        for timeline in item['timeline']:
            text = text + ' ' + timeline['detail']
        print(text)
        #for data in item:
        #    if(data == 'package_name'):
        #        words = word_tokenize(item[data])
        #        for word in words:
        #            if(word == 'หาดใหญ่'):
        #                word = 'สงขลา'
        #            if(word in self.provinces):
        #                item['provinces'].append(word)
        #                item['region'] = self.region[self.provinces.index(word)]
        #    if(data == 'detail'):
        #        words = word_tokenize(item[data])
        #        for word in words:
        #            if(word == 'หาดใหญ่'):
        #                word = 'สงขลา'
        #            if(word in self.provinces):
        #                item['provinces'].append(word)
        #                item['region'] = self.region[self.provinces.index(word)]
        #    if(data == 'timeline'):
        #        for timeline in item[data]:
        #            words = word_tokenize(timeline['detail'])
        #            for word in words:
        #                if(word == 'หาดใหญ่'):
        #                    word = 'สงขลา'
        #                if(word in self.provinces):
        #                    item['provinces'].append(word)
        #                    item['region'] = self.region[self.provinces.index(word)]

                    #words = word_tokenize(timeline['detail'])
                    #print('-------------------')
                    #print(words)
                    #print(timeline['detail'])

        #if valid:
        #    self.collection.insert(dict(item))
        #    log.msg("Question added to MongoDB database!",
        #            level=log.DEBUG, spider=spider)
        return item
