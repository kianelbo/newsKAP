# -*- coding: utf-8 -*-
import scrapy
from bs4 import BeautifulSoup
from termcolor import colored

class FarsNewsSpider(scrapy.Spider):
    name = 'farsnews'
    allowed_domains = ['farsnews.com']
    start_urls = ['https://www.farsnews.com/rss']

    def parse(self, response):
        posts = response.xpath('//channel/item')
        print(colored('[SPIDER]','green'),f"there are {len(posts.extract())} news links in RSS feed.")
        for post in posts:
            url = post.xpath('link//text()').extract_first()
            yield scrapy.Request(url, callback=self.parse_news_page)

    def parse_news_page(self, response):
        print(colored('[SPIDER]', 'green'), f"Crawled {response.url[:60]} ...")

        date = self.clean_date(self.clean_html(response.xpath("//div[contains(@class, 'publish-time')]").extract_first()))
        title = self.clean_text(response.xpath("//div[contains(@class, 'news-data')]//span[contains(@class, 'title')]/text()").extract_first())
        summary = self.clean_text(response.xpath("//div[contains(@class, 'news-data')]//p[contains(@class, 'lead')]/text()").extract_first())
        thumbnail = response.xpath("//div[contains(@class, 'news-data')]//img/@src").extract_first()
        text = self.clean_html(response.xpath("//div[contains(@class, 'nt-body')]").extract_first())
        tags = response.xpath("//div[contains(@class, 'tags')]/a/text()").extract()
        tags_clean = []
        for t in tags:
            tags_clean.append(t.strip())
        yield {
            'date': date,
            'title': title,
            'summary': summary,
            'content': text,
            'thumbnail': thumbnail,
            'source': 'farsnews.com',
            'link': response.url,
            'tags': tags_clean,
        }

    def clean_html(self,text):
        text = BeautifulSoup(text, features="html.parser").get_text()
        text = text.strip()
        text = text.replace(',', '')
        text = text.replace('\n', '')
        return text

    def clean_text(self,text):
        text = text.strip()
        text = text.replace(',', '')
        text = text.replace('\n', '')
        text = text.replace('\xa0', '')
        return text

    def clean_date(self,text):
        text = text.strip()
        text = text.replace(',', '')
        text = text.replace('\n', '')
        text = text.replace('\xa0', '')
        return text

