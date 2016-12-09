# -*- coding: utf-8 -*-
import json
import time
from scrapy.spiders import CrawlSpider
from storage import get_storage


class BaseSpider(CrawlSpider):
    """Base class for crawl_corpora spiders

    BaseSpider include some common functions and methods for spiders, which may
    simplify the code of spiders. Override the corresponding part if needed.

    Attributes:
        enable_extractor: A boolean indicating if we need to extract raw pages
        proxy_stable: A boolean indicating if we use proxy in stable pool
        extractor: The extractor we use to extract raw pages
        time_stamp: A time related variable to indicate data version
    """

    enable_extractor = True
    proxy_stable = False
    extractor = None
    time_stamp = int(time.time())

    def __init__(self, *a, **kw):
        """Init BaseSpider with storage configuration"""
        CrawlSpider.__init__(self, *a, **kw)
        self.source_name = self.get_source_name()
        self.storage = get_storage(self.source_name)

    def get_source_name(self):
        """Define the source name which the spider refers to

        Returns:
            A string named the source
        """
        return self.name

    @staticmethod
    def get_source_id(response):
        """Define a unique ID for the result according to response in one spider
            Whenever the spider starts, same results share the same ID

        Returns:
            A string named unique ID
        """
        return response.url.split('/')[-1]

    def parse_response(self, response):
        """Decide how we handle the response"""
        page_id = '%s_%s' % (self.source_name, self.get_source_id(response))
        if self.storage:
            self.storage.save(page_id, response.body)
        if self.enable_extractor:
            self.store_extractor(response)

    def store_extractor(self, response):
        try:
            result = self.extractor.parse_response(response)
        except (AttributeError, TypeError):
            return
        result_json = json.dumps(result, ensure_ascii=False, sort_keys=True)
        with open('%s_result_%s' % (self.name, self.time_stamp), 'a') as output:
            output.write(result_json + '\n')

    @staticmethod
    def process_request_headers(request):
        """Process request for detailed domain"""
        pass
