import scrapy
import time
from scrapy import Request

from Crawler.items import AnZhuoItem
from Crawler.pipelines import AnZhuoPipeline


class anzhuo_Spider(scrapy.Spider):
    name = "anzhuo_app"

    pipeline = set([AnZhuoPipeline, ])

    start_urls = []

    for i in range(1, 51) :
        url = 'http://apk.hiapk.com/apps/Social?sort=5&pi=' + str(i)
        start_urls.append(url)

    def start_requests(self):
        for url in self.start_urls:
            yield self.make_requests_from_url(url)


    def parse2(self, response):
        time.sleep(3)
        name = response.xpath("//div[@id='appSoftName']/text()").extract()
        producer = response.xpath("//div[@class='code_box_border']/div[@class='line_content'][1]/span[2]/text()").extract()
        hot_level = response.xpath("//div[@class='code_box_border']/div[@class='line_content'][2]/span[2]/text()").extract()
        size = response.xpath("//div[@class='code_box_border']/div[@class='line_content'][3]/span[2]/text()").extract()

        category = response.xpath("//div[@class='code_box_border']/div[@class='line_content'][4]/span[2]/a/span/text()").extract()
        update_time = response.xpath("//div[@class='code_box_border']/div[@class='line_content'][7]/span[2]/text()").extract()

        firmware = response.xpath("//div[@class='code_box_border']/div[@class='line_content'][6]/span[2]/text()").extract()

        description = response.xpath("//pre[@id='softIntroduce']/text()").extract()
        update_info = response.xpath("//div[@id='softImprint']/div[2]/pre/text()").extract()
        grade = response.xpath("//div[@class='star_num']/text()").extract()

        item = AnZhuoItem()
        if len(name) > 0 :
            item['name'] = name[0].strip()
        else :
            item['name'] = ''

        if len(producer) > 0 :
            item['producer'] = producer[0].strip()
        else :
            item['producer'] = ''

        if len(hot_level) > 0 :
            item['hot_level'] = hot_level[0].strip()
        else :
            item['hot_level'] = ''

        if len(size) > 0 :
            item['size'] = size[0].strip()
        else :
            item['size'] = ''

        if len(category) > 0 :
            item['category'] = category[0].strip()
        else :
            item['category'] = ''

        if len(update_time) > 0 :
            item['update_time'] = update_time[0].strip()
        else :
            item['update_time'] = ''

        if len(firmware) > 0 :
            item['firmware'] = firmware[0].strip()
        else :
            item['firmware'] = ''

        if len(description) > 0 :
            item['description'] = description[0].strip()
        else :
            item['description'] = ''

        if len(update_info) > 0 :
            item['update_info'] = update_info[0].strip()
        else :
            item['update_info'] = ''

        if len(grade) > 0 :
            item['grade'] = grade[0].strip()
        else :
            item['grade'] = ''

        return item


    def parse(self, response):

        url_prefix = 'http://apk.hiapk.com'
        for url in response.xpath('//dl[@class="list_content"]/dt/span[1]/a/@href').extract():
            print url
            time.sleep(3)
            yield Request(url = url_prefix + url, callback = self.parse2)


