# -*- coding: utf-8 -*-
import scrapy
from bs4 import BeautifulSoup
from termcolor import colored


class GenericSpider(scrapy.Spider):
    name = 'generic'
    allowed_domains = ['yjc.ir','irna.ir','isna.ir','mehrnews.com','khabaronline.ir','mashreghnews.ir','irinn.ir']
    start_urls = [
        'https://www.yjc.ir/fa/rss/allnews',
        'https://www.irna.ir/rss',
        'https://www.isna.ir/rss',
        'https://www.mehrnews.com/rss',
        'https://www.khabaronline.ir/rss',
        'https://www.mashreghnews.ir/rss',
        'https://www.irinn.ir/fa/rss/allnews'
    ]

    def parse(self, response):
        posts = response.xpath('//channel/item')
        source = response.xpath('//channel/link/text()').extract_first()
        print(colored('[SPIDER]','green'),f"{response.url}: there are {len(posts.extract())} news links in RSS feed.")
        for post in posts:
            date = post.xpath('pubDate/text()').extract_first()
            title = post.xpath('title/text()').extract_first()
            summary = post.xpath('description/text()').extract_first()
            thumbnail = post.xpath('enclosure/@url').extract_first()
            link = post.xpath('link/text()').extract_first()
            iy = {
                'date': date,
                'title': title,
                'summary': summary,
                'content': '',
                'thumbnail': thumbnail,
                'source': source,
                'link': link,
                'tags': [],
            }
            yield scrapy.Request(link, callback=self.parse_news_page, cb_kwargs=dict(initial_yield = iy))

    def parse_news_page(self, response, initial_yield):
        print(colored('[SPIDER]', 'green'), f"Crawled {response.url[:60]} ...")

        text = self.clean_html(response.xpath("//div[contains(@class, 'body')]").extract_first())
        initial_yield['content'] = text
        yield initial_yield

    def clean_html_basic(self,text):
        text = BeautifulSoup(text, features="html.parser").get_text()
        text = text.strip()
        text = text.replace(',', '')
        text = text.replace('\n', '')
        return text

    def clean_html(self,text):
        soup = BeautifulSoup(text, 'html.parser')
        text_only = soup.find_all(text=True)

        output = ''
        blacklist = [
            'script',
            'noscript',
            'img',
            'audio',
            'video'
            # there may be more elements...
        ]

        for t in text_only:
            if t.parent.name not in blacklist:
                output += f"{t} "

        output = output.replace(',', '')
        output = output.replace('\n', '')
        return output

    def clean_html_full(self,text):
        soup = BeautifulSoup(text, 'html.parser')
        text_only = soup.find_all(text=True)

        output = ''
        blacklist = [
            '[document]',
            'noscript',
            'header',
            'html',
            'meta',
            'head',
            'input',
            'script',
            'style'
            # there may be more elements...
        ]

        for t in text_only:
            if t.parent.name not in blacklist:
                output += t

        output = output.replace(',', '')
        output = output.replace('\n', '')
        return output
