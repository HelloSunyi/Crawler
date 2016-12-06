import scrapy
from scrapy import Request

from Crawler.items import SpotItem, LvYouItem
from Crawler.pipelines import SpotPipeline, LvYouPipeline


class boya_Spider(scrapy.Spider):
    name = "spot_location"

    pipeline = set([SpotPipeline, ])

    start_urls = ['http://www.tcmap.com.cn/',
                  ]

    def start_requests(self):
        for url in self.start_urls:
            yield self.make_requests_from_url(url)

    def parse2(self, response):
        item = SpotItem()
        name1 = response.xpath("//div[@id='page_left']/div[1]/a[2]/text()").extract()
        name2 = response.xpath("//div[@id='page_left']/div[1]/a[3]/text()").extract()

        for name in response.xpath('//div[@id="page_left"]/div[9]/div[@class="list180"]/li/a/text()').extract():

            item = SpotItem()
            item['spot_name'] = name
            if len(name1) > 0:
                item['address_name1'] = name1[0]
            else:
                item['address_name1'] = ''

            if len(name2) > 0:
                item['address_name2'] = name2[0]
            else:
                item['address_name2'] = ''

            yield item



    def parse(self, response):
        print "----------------------------------------"
        urls = []
        url_prefix = 'http://www.tcmap.com.cn'
        for sel in response.xpath('//div[@id="list110"]/a/@href'):
            urls.append(url_prefix + sel.extract())

        for url in urls :
            yield Request(url=url, callback=self.parse2)


class lvyou_Spider(scrapy.Spider):
    name = "lvyou_location"

    pipeline = set([LvYouPipeline, ])

    start_urls = ['http://data.travel.china.com/travelhtml/nativelist.html',
                  ]

    def start_requests(self):
        for url in self.start_urls:
            yield self.make_requests_from_url(url)

    def parse2(self, response):
        item = LvYouItem()
        name1 = response.xpath("//div[@class='path']/em[2]/a[1]/text()").extract()[0]
        name2 = response.xpath("//div[@class='path']/em[2]/a[2]/text()").extract()[0]
        name3 = response.xpath("//div[@class='path']/em[2]/a[3]/text()").extract()[0]
        address_total = response.xpath("//div[@class='intro']/div[@class='txt']/p[5]/label/@title").extract()[0]
        spot_name = response.xpath("//div[@class='scene_tit']/text()").extract()[0]


        item = LvYouItem()
        item['spot_name'] = spot_name
        item['address_name1'] = name1
        item['address_name2'] = name2
        item['address_name3'] = name3
        item['address_total'] = address_total
        yield item


    def parse(self, response):
        print "----------------------------------------"
        urls = []
        url_prefix = 'http://data.travel.china.com'
        for sel in response.xpath('//div[@class="con"]/div/dl[@class="jdsort"]/dd/div/a/@href'):
            urls.append(url_prefix + sel.extract())

        for url in urls :
            print url
            yield Request(url=url, callback=self.parse2)
