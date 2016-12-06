import scrapy
from scrapy import Request

from Crawler.items import SubwayItem, LvYouItem
from Crawler.pipelines import SubwayPipeline


class lvyou_Spider(scrapy.Spider):
    name = "subway_route"

    pipeline = set([SubwayPipeline, ])

    start_urls = ['http://ditie.mapbar.com/',
                  ]

    def start_requests(self):
        for url in self.start_urls:
            yield self.make_requests_from_url(url)


    def parse3(self, response):
        print "--------------------"
        item = LvYouItem()
        city_name = response.xpath("//div[@class='city']/h1/text()").extract()[0]
        subway_name = response.xpath("//div[@class='ditie_line clear']/h1/text()").extract()[0]
        path_name = ''
        for name in response.xpath("//div[@class='routemap']/ul/li/a/text()").extract():
            if path_name == '' :
                path_name = name
            else:
                path_name = path_name + "->" + name

        print city_name
        item = SubwayItem()
        item['city_name'] = city_name
        item['subway_name'] = subway_name
        item['path_name'] = path_name

        return item


    def parse2(self, response):
        for url in response.xpath('//div[@class="ditie_news ditie_color"]/p/a/@href').extract():
            yield Request(url=url, callback=self.parse3)


    def parse(self, response):
        print "-----------------------------------"
        #print response.body
        for sel in response.xpath('//div[@class="ditie_city"]/a/@href'):
            #print sel.extract()
            yield Request(url=sel.extract(), callback=self.parse2)

        for sel in response.xpath('//div[@class="ditie_city acolor"]/a/@href'):
            print sel.extract()
            yield Request(url=sel.extract(), callback=self.parse2)


