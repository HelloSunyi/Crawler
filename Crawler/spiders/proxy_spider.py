import scrapy

from Crawler.items import ProxyItem
from Crawler.pipelines import ProxyPipeline


class proxy_Spider(scrapy.Spider):
    name = "proxy_spider"
    allowed_domains = ["kuaidaili.com"]

    pipeline = set([ProxyPipeline, ])

    start_urls = []
    for i in range(2, 50):
        url = 'http://www.kuaidaili.com/free/inha/' + str(i) + '/'
        start_urls.append(url)

    def start_requests(self):
        for url in self.start_urls:
            yield self.make_requests_from_url(url)

    def parse(self, response):

        ips = response.xpath('//td[@data-title="IP"]/text()')
        ports = response.xpath('//td[@data-title="PORT"]/text()')

        for (ip,port) in zip(ips, ports):
            item = ProxyItem()
            item['ip'] = ip.extract()
            item['port'] = port.extract()
            yield item