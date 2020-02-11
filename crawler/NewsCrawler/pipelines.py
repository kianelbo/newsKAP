# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.exceptions import DropItem
from termcolor import colored
import csv
import pymongo
import pprint


class NewsCrawlerDbPipeline(object):

    collection_name = 'crawled'
    stats_db_name = 'crawled_stats'

    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db
        self.seen_links = set()

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DATABASE')
        )

    def open_spider(self, spider):
        print(colored('[PIPELINE]','yellow'),'Opened')
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]
        # load seen_links set
        for a in self.db[self.collection_name].find({},{"link":1}):
            self.seen_links.add(a['link'])

    def close_spider(self, spider):
        print(colored('[PIPELINE]', 'yellow'), 'Close')
        self.client.close()

    def process_item(self, item, spider):
        # duplicate detection
        if item['link'] in self.seen_links:
            print(colored('[SKIP]', 'red'), 'duplicate item.')
            raise DropItem("Duplicate item.")
        else:
            self.seen_links.add(item['link'])

        print(colored('[ADD]', 'blue'), 'adding item to mongodb ...')
        self.db[self.collection_name].insert_one(dict(item))
        # update stats db
        self.db[self.stats_db_name].update_one({'source': item['source']}, {'$inc': {'count': 1}}, upsert=True)
        return item


class NewsCrawlerCsvPipeline(object):

    def open_spider(self, spider):
        print(colored('[PIPELINE]','yellow'),'Opened')
        self.file = open("crawled.csv","a+",encoding='utf-8')

    def close_spider(self, spider):
        print(colored('[PIPELINE]', 'yellow'), 'Close')
        self.file.close()

    def process_item(self, item, spider):
        with open("crawled.csv", "r") as f:
            csvreader = csv.reader(f, delimiter=",")
            next(csvreader, None) #skip headers
            for row in csvreader:
                if item['link'] == row[6]:
                    print(colored('[SKIP]', 'red'), 'Duplicate Item.')
                    raise DropItem("Duplicate Item.")

        print(colored('[ADD]', 'blue'), 'adding item to csv ...')

        fieldnames = ['date','title','summary','content','thumbnail','source','link','tags']
        writer = csv.DictWriter(self.file, fieldnames=fieldnames)
        if self.file.tell() == 0:
            writer.writeheader()
        writer.writerow(item)
        return item

