from NewsCrawler.spiders.GenericSpider import GenericSpider
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from scrapy.signalmanager import dispatcher

import pymongo
from termcolor import colored
from twisted.internet import reactor
from twisted.internet.task import deferLater

url_priority = [
    ['https://www.yjc.ir/fa/rss/allnews', 'https://www.yjc.ir', 30],
    ['https://www.irna.ir/rss', 'https://www.irna.ir', 180],
    ['https://www.isna.ir/rss', 'https://www.isna.ir', 180],
    ['https://www.mehrnews.com/rss', 'https://www.mehrnews.com', 180],
    ['https://www.khabaronline.ir/rss', 'https://www.khabaronline.ir', 180],
    ['https://www.mashreghnews.ir/rss', 'https://www.mashreghnews.ir', 180],
    ['https://www.irinn.ir/fa/rss/allnews', 'https://www.irinn.ir', 60]
]
current = 0

prj_settings = get_project_settings()
prj_settings.update({
    'LOG_ENABLED': 'False'
})

# init connection to db for stats monitoring
mongo_uri = prj_settings.get('MONGO_URI'),
mongo_db = prj_settings.get('MONGO_DATABASE')
client = pymongo.MongoClient(mongo_uri)
db = client[mongo_db]
stats_db_name = 'crawled_stats'

# reset stats
for url_a in url_priority:
    db[stats_db_name].update_one({'source': url_a[1]}, {'$set': {'count': 0}})


def sleep(self, *args, seconds):
    """Non blocking sleep callback"""
    return deferLater(reactor, seconds, lambda: None)


def update_priority(self, *args, url):
    crawled_count = db[stats_db_name].find_one({'source': url})['count']
    print(colored('[FRONTIER]', 'magenta'), f"updating weights for {url} (crawled count: {crawled_count})")
    if crawled_count > 1:
        for url_a in url_priority:
            if url_a[1] == url:
                url_a[2] -= 1
    elif crawled_count == 0:
        for url_a in url_priority:
            if url_a[1] == url:
                url_a[2] += 1
    # reset stat
    db[stats_db_name].update_one({'source': url}, {'$set': {'count': 0}})


process = CrawlerProcess(prj_settings)


def _crawl(result, spider, source_url):
    print(colored('[FRONTIER]', 'magenta'), f"Crawl Started: {source_url}")

    crawl_url = ''
    wait = 0
    for url_a in url_priority:
        if url_a[1] == source_url:
            crawl_url = url_a[0]
            wait = url_a[2]

    deferred = process.crawl(spider, start_urls=[crawl_url])
    deferred.addCallback(lambda results:
                         print(colored('[FRONTIER]', 'magenta'), f"crawler for {source_url} will wait for {wait} seconds..."))
    deferred.addCallback(update_priority, url=source_url)
    deferred.addCallback(sleep, seconds=wait)
    deferred.addCallback(_crawl, spider, source_url)
    return deferred


for url_a in url_priority:
    _crawl(None, GenericSpider, url_a[1])

process.start()
