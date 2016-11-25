# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html
import uuid

import scrapy
import time

from Crawler.items import JokeItem
from Crawler.pipelines import HaHaPipeline, DuanZiPipeline, BieDouPipeline, PengFuPipeline, XiHaPipeline, QiuShiPipeline

class haha_Spider(scrapy.Spider):
    name = "haha_joke"
    allowed_domains = ["haha365.com"]

    pipeline = set([HaHaPipeline, ])

    start_urls = []
    for i in range(2, 500):
        url = 'http://www.haha365.com/joke/index_' + str(i) + '.htm'
        start_urls.append(url)

    def start_requests(self):
        for url in self.start_urls:
            yield self.make_requests_from_url(url)

    def parse(self, response):

        for sel in response.xpath('//div[@id="endtext"]/p'):
            item = JokeItem()
            item['joke_content'] = sel.extract()
            yield item


class duanzi_Spider(scrapy.Spider):
    name = "duanzi_joke"
    allowed_domains = ["waduanzi.com"]

    pipeline = set([DuanZiPipeline, ])

    start_urls = []
    for i in range(2, 100):
        url = 'http://www.waduanzi.com/joke/page/' + str(i)
        start_urls.append(url)

    def start_requests(self):
        for url in self.start_urls:
            yield self.make_requests_from_url(url)

    def parse(self, response):

        for sel in response.xpath('//div[@class="item-content"]/text()'):
            item = JokeItem()
            item['joke_content'] = sel.extract()
            yield item


class pengfu_Spider(scrapy.Spider):
    name = "pengfu_joke"
    allowed_domains = ["pengfu.com"]

    pipeline = set([PengFuPipeline, ])

    start_urls = []
    for i in range(2, 50):
        url = 'http://www.pengfu.com/xiaohua_' + str(i) + '.html'
        start_urls.append(url)

    def start_requests(self):
        for url in self.start_urls:
            yield self.make_requests_from_url(url)

    def parse(self, response):

        for sel in response.xpath('//div[@class="content-img clearfix pt15 relative"]/text()'):
            item = JokeItem()
            print sel
            item['joke_content'] = sel.extract()
            yield item

class biedou_Spider(scrapy.Spider):
    name = "biedou_joke"
    allowed_domains = ["beidoul.com"]

    pipeline = set([BieDouPipeline, ])

    start_urls = []
    for i in range(2, 100):
        url = 'http://www.biedoul.com/wenzi/lengxiaohua/' + str(i) + '/'
        start_urls.append(url)

    def start_requests(self):
        for url in self.start_urls:
            yield self.make_requests_from_url(url)

    def parse(self, response):

        for sel in response.xpath('//div[@class="dz-list-con"]/text()'):
            item = JokeItem()
            print sel
            item['joke_content'] = sel.extract()
            yield item

class xiha_Spider(scrapy.Spider):
    name = "xiha_joke"
    allowed_domains = ["xxhh.com"]

    pipeline = set([XiHaPipeline, ])

    start_urls = []
    for i in range(2, 500):
        url = 'http://www.xxhh.com/duanzi/page/' + str(i) + '/?l=1479728255'
        start_urls.append(url)

    def start_requests(self):
        for url in self.start_urls:
            yield self.make_requests_from_url(url)

    def parse(self, response):

        for sel in response.xpath('//div[@class="article"]/text()'):
            item = JokeItem()
            print sel
            item['joke_content'] = sel.extract()
            yield item

class qiushi_Spider(scrapy.Spider):
    name = "qiushi_joke"
    allowed_domains = ["qiushibaike.com"]
    pipeline = set([QiuShiPipeline, ])

    start_urls = []
    for i in range(2, 35):
        url = 'http://www.qiushibaike.com/text/page/' + str(i) + '/?s=4932402'
        start_urls.append(url)

    def start_requests(self):
        for url in self.start_urls:
            yield self.make_requests_from_url(url)

    def parse(self, response):

        for sel in response.xpath('//div[@class="content"]'):
            item = JokeItem()
            item['joke_content'] = sel.extract()
            yield item

    @staticmethod
    def process_request_headers(request):
        """Process request to get 200 response for dianping
            Dianping checks User-Agent in headers and _hc.v in cookies.
            Fake these parts.
        """
        request.headers.setdefault('User-Agent',
                                   'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) '
                                   'AppleWebKit/537.36 (KHTML, like Gecko) '
                                   'Chrome/51.0.2704.103 Safari/537.36')
        request.cookies.setdefault('_hc.v', '%s.%d' % (str(uuid.uuid1()),
                                                       int(time.time())))