import scrapy
from scrapy import Request
from scrapy import Selector

from Crawler.items import LocationItem
from Crawler.pipelines import LocationPipeline



class boya_Spider(scrapy.Spider):
    name = "boya_location"

    pipeline = set([LocationPipeline, ])

    start_urls = ['http://www.tcmap.com.cn',
                  ]

    def start_requests(self):
        for url in self.start_urls:
            yield self.make_requests_from_url(url)

    def parse3(self, response):
        item = LocationItem()
        name1 = response.xpath("//div[@id='page_left']/div[1]/a[2]/text()").extract()
        name2 = response.xpath("//div[@id='page_left']/div[1]/a[3]/text()").extract()
        name3 = response.xpath("//div[@id='page_left']/div[1]/a[4]/text()").extract()
        name4 = response.xpath("//div[@id='page_left']/div[1]/a[5]/text()").extract()
        if len(name1) > 0:
            item['title_name1'] = name1[0]
        else :
            item['title_name1'] = ''

        if len(name2) > 0:
            item['title_name2'] = name2[0]
        else :
            item['title_name2'] = ''

        if len(name3) > 0:
            item['title_name3'] = name3[0]
        else :
            item['title_name3'] = ''

        if len(name4) > 0:
            item['title_name4'] = name4[0]
        else :
            item['title_name4'] = ''

        yield item

    def parse2(self, response):

        prefix_url = response.url
        index = prefix_url.find('/', 25)
        prefix_url = prefix_url[0 : index+1]

        title_name1 = response.xpath('//div[@id="page_left"]/div[1]/a[2]/text()').extract()
        title_name2 = response.xpath('//div[@id="page_left"]/div[1]/a[3]/text()').extract()

        title_name3_ls = response.xpath('//div[@class="l"]/a/@href').extract()
        title_name3_l2s = response.xpath('//div[@class="l2"]/a/@href').extract()

        print "--------------------"
        print prefix_url
        if len(title_name3_ls) == 0 and len(title_name3_l2s) == 0 :
            for title_name3 in response.xpath("//div[@id='page_left']/div[5]/table/tr/td[1]/strong/a/text()").extract():
                item = LocationItem()
                item['title_name1'] = title_name1
                item['title_name2'] = title_name2
                item['title_name3'] = title_name3
                item['title_name4'] = ''
                yield item
        else :

            for title_name3_l in title_name3_ls:
                print title_name3_l
                yield Request(url=prefix_url + title_name3_l, callback=self.parse3)
            for title_name3_l2 in title_name3_l2s:
                print title_name3_l2
                yield Request(url=prefix_url + title_name3_l2, callback=self.parse3)



    def parse(self, response):
        print "----------------------------------------"
        urls = []
        url_prefix = 'http://www.tcmap.com.cn'
        for sel in response.xpath('//div[@id="list110"]/a/@href'):
            urls.append(url_prefix + sel.extract())

        for url in urls :
            yield Request(url=url, callback=self.parse2)

