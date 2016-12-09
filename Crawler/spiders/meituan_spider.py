import codecs

import scrapy
from scrapy import Request

from Crawler.items import LocationItem, MeiTuanItem
from Crawler.pipelines import LocationPipeline


class shenzhou_Spider(scrapy.Spider):
    name = "meituan_location"

    pipeline = set([LocationPipeline, ])



    start_urls = ['http://www.meituan.com/index/changecity',]

    def start_requests(self):
        for url in self.start_urls:
            yield self.make_requests_from_url(url)

    def parse2(self, response):
        print "--------"
        for url in response.xpath("//div[@class='filter-section-wrapper']/div[2]/div/ul/li[@class='item']/a/@href").extract():
            print url
            item = LocationItem()
            item['location_name'] = url
            yield item
            #yield Request(url=url, callback=self.parse3)


    def parse3(self, response):

        city_name = response.xpath("//div[@class='city-info']/h2/a/text()").extract()[0]
        area_name = response.xpath("//div[@class='filter-breadcrumb']/span[5]/span/text()").extract()[0].strip()[3:]

        for name in response.xpath("//div[@class='filter-section-wrapper']/div[@data-component='filter-geo']/div/div[2]/ul/li[@class='item']/a/text()").extract():
            item = MeiTuanItem()
            item['city_name'] = city_name
            item['area_name'] = area_name
            item['landmark_name'] = name
            yield item

        for name in response.xpath("//div[@class='filter-section-wrapper']/div[@data-component='filter-geo']/div/div[2]/div/ul/li[@class='item']/a/text()").extract():
            item = MeiTuanItem()
            item['city_name'] = city_name
            item['area_name'] = area_name
            item['landmark_name'] = name
            yield item



    def parse(self, response):
        for url in response.xpath('//ol[@class="hasallcity"]/li/p/span[2]/a[@class="isonline"]/@href').extract():
            url = url + '/category/meishi'
            item = LocationItem()
            item['location_name'] = url
            yield item
            #yield Request(url=url, callback=self.parse2)

