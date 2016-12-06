import scrapy
import time

from scrapyjs.request import SplashRequest

from Crawler.items import FoodItem
from Crawler.pipelines import FoodPipeline


class meishichina_Spider(scrapy.Spider):
    name = "meishichina_lingshi_food"

    pipeline = set([FoodPipeline, ])

    start_urls = []
    for i in range(1, 125):
        url = 'http://home.meishichina.com/recipe/lingshi/list-' + str(i) + '.html'
        start_urls.append(url)

    def start_requests(self):
        for url in self.start_urls:
            yield self.make_requests_from_url(url)

    def parse(self, response):
        for sel in response.xpath('//div[@class="detail"]/h2/a/text()'):
            item = FoodItem()
            item['food_name'] = sel.extract()
            yield item


class meishi_Spider(scrapy.Spider):
    name = "meishi_food"
    allowed_domains = ["meishij.net"]

    pipeline = set([FoodPipeline, ])

    start_urls = []
    for i in range(2, 56):
        url = 'http://www.meishij.net/chufang/diy/guowaicaipu1/aozhou/?&page=' + str(i)
        start_urls.append(url)

    def start_requests(self):
        for url in self.start_urls:
            yield self.make_requests_from_url(url)

    def parse(self, response):

        for sel in response.xpath('//div[@class="c1"]/strong/text()'):
            item = FoodItem()
            item['food_name'] = sel.extract()
            yield item

class xinshipu_Spider(scrapy.Spider):
    name = "xinshipu_food"

    pipeline = set([FoodPipeline, ])

    start_urls = []
    for i in range(1, 47):
        url = 'http://www.xinshipu.com/caipu/17844/?page=' + str(i)
        start_urls.append(url)


    def start_requests(self):
        for url in self.start_urls:
            yield self.make_requests_from_url(url)

    def parse(self, response):
        for sel in response.xpath('//div[@class="h-pw-w"]/p/text()'):
            item = FoodItem()
            item['food_name'] = sel.extract()
            yield item
