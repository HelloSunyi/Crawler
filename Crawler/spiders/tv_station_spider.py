import scrapy

from Crawler.items import StationItem
from Crawler.pipelines import StationPipeline


class baishi_Spider(scrapy.Spider):
    name = "baishi_station"

    pipeline = set([StationPipeline, ])

    start_urls = ['http://www.baitv.com/program/all.html',]

    def start_requests(self):
        for url in self.start_urls:
            yield self.make_requests_from_url(url)

    def parse(self, response):
        for sel in response.xpath('//section[@class="all-channels"]/div/ul/li/a/text()'):
            print sel.extract()
            item = StationItem()
            item['station_name'] = sel.extract()
            yield item
