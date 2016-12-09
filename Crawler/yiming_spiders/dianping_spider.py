# -*- coding: utf-8 -*-
import time
import uuid
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule
from base_spider import BaseSpider
from ..extractors import dianping_extractor


class DianpingSpider(BaseSpider):

    name = 'dianping'
    extractor = dianping_extractor
    download_delay = 0.1
    start_urls = ['http://www.dianping.com/citylist']
    rules = (
        # Find city pages
        Rule(LinkExtractor(allow=(r'http://www.dianping.com/\w+$', ))),
        # Find food pages
        Rule(LinkExtractor(allow=('/\w+/food', ))),
        # Find shop indexes in food category
        Rule(LinkExtractor(allow=('/search/category/\d+/10/r\d+[p\d+]*$', ))),
        # Find shop details
        Rule(LinkExtractor(allow=('/shop/\d+$', )), callback='parse_response'),
    )

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
