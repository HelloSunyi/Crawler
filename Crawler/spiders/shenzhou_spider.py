import scrapy
from scrapy import Request

from Crawler.items import ShenZhouItem
from Crawler.pipelines import ShenZhouPipeline


class shenzhou_Spider(scrapy.Spider):
    name = "shenzhou_location"

    pipeline = set([ShenZhouPipeline, ])

    start_urls = ['http://service.zuche.com/',]

    def start_requests(self):
        for url in self.start_urls:
            yield self.make_requests_from_url(url)

    def parse2(self, response):

        for url in response.xpath("//ul[@class='depUlClass']/li/dl/dd/a/@href").extract():
            yield Request(url=url, callback=self.parse3)


    def parse3(self, response):
        store_name = response.xpath("//h3[@class='pt10 f14']/text()").extract()[0]
        city_name = response.xpath("//p[@class='bold rentCity']/span/text()").extract()[0]
        area_name = response.xpath("//p[@class='bold rentCity']/a[@class='colorBlue']/text()").extract()[0]
        address_name = response.xpath("//div[@class='addressInfo']/text()").extract()[2]

        city_name = city_name[0:len(city_name)-2]
        item = ShenZhouItem()
        item['store_name'] = store_name
        item['city_name'] = city_name
        item['area_name'] = area_name
        item['address_name'] = address_name
        return item


    def parse(self, response):
        for url in response.xpath('//dl[@class="citySort"]/dd/a/@href').extract():
            yield Request(url=url, callback=self.parse2)


