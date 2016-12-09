# -*- coding: utf-8 -*-
import json
import re
from scrapy.http import Request
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule
from base_spider import BaseSpider
from ..extractors import iqiyi_show_extractor


class IqiyiShowSpider(BaseSpider):

    name = 'iqiyi_show'
    extractor = iqiyi_show_extractor
    download_delay = 0.1
    start_urls = ["http://www.iqiyi.com/lib/zongyi/,,_11_1.html"]
    rules = (
        # Find zongyi indexes for all categories
        Rule(LinkExtractor(allow=(
            'http://www.iqiyi.com/lib/zongyi/[^,]*,[^,]*,[^,]*_11_\d+.html',
        ))),
        # Find zongyi pages
        Rule(LinkExtractor(allow=('http://www.iqiyi.com/lib/m_\d+.html',)),
             callback='get_series')
    )
    api_vote = 'http://up.video.iqiyi.com/ugc-updown/quud.do?dataid=%s&type=%s'

    def get_series(self, response):
        try:
            result = self.extractor.parse_response(response)
        except (AttributeError, TypeError):
            return
        raw_info = {
            'html': response.body,
            'vote': '',
        }
        source_id = self.get_source_id(response)
        yield Request(self.api_vote % (result.pop('up_down_id'),
                                       result.pop('up_down_type')),
                      meta={'source_id': source_id,
                            'raw_info': raw_info,
                            'result': result},
                      callback=self.get_vote)

    def get_vote(self, response):
        """Get vote information"""
        try:
            response.meta['result'].update(
                self.extractor.parse_response_vote(response))
        except ValueError:
            return
        response.meta['raw_info']['vote'] = response.body
        self.save(response.meta['source_id'],
                  response.meta['raw_info'],
                  response.meta['result'])

    def save(self, source_id, raw_info, result):
        raw_json = json.dumps(raw_info, ensure_ascii=False, sort_keys=True)
        page_id = '%s_%s' % (self.get_source_name(), source_id)
        if self.storage:
            self.storage.save(page_id, raw_json)
        result_json = json.dumps(result, ensure_ascii=False, sort_keys=True)
        with open('%s_result_%s' % (self.name, self.time_stamp), 'a') as output:
            output.write(result_json + '\n')

    @staticmethod
    def get_source_name():
        return 'iqiyi'

    @staticmethod
    def get_source_id(response):
        m = re.search('m_(\d+)', response.url)
        return m.group(1)
