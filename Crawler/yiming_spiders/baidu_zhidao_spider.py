# -*- coding: utf-8 -*-
import json
import re
from scrapy.http import Request
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule
from base_spider import BaseSpider
from ..extractors import baidu_zhidao_extractor


class BaiduZhidaoSpider(BaseSpider):

    name = 'baidu_zhidao'
    extractor = baidu_zhidao_extractor
    download_delay = 0.1
    start_urls = ['https://zhidao.baidu.com']
    api_user = 'https://zhidao.baidu.com/q?ct=24&cm=18&tn=uiframework&un=%s'
    api_answers = 'http://zhidao.baidu.com/mobile/replies/?' \
                  'pn=%d&rn=10&sample=1&qid=%s&sort='
    rules = (
        # Find question list
        Rule(LinkExtractor(allow=('list\?\w+', ))),
        # Find user list
        Rule(LinkExtractor(allow=('misc/rank', ))),
        # Find team list
        Rule(LinkExtractor(allow=('uteam', ))),
        # Find user info
        Rule(LinkExtractor(allow=('p/[^?]+\?from=zhidao', )),
             process_links='process_user_links'),
        # Find user answer list
        Rule(LinkExtractor(allow=('usercard/answer', ))),
        # Find question
        Rule(LinkExtractor(allow=('question/\d+', ),
                           allow_domains='zhidao.baidu.com'),
             process_links='process_question_links',
             callback='get_question'),
    )
    cookies = ''
    user_agent_wap = 'Mozilla/5.0 (iPhone; CPU iPhone OS 8_0_2 like ' \
                     'Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) ' \
                     'Version/8.0 Mobile/12A366 Safari/600.1.4'
    user_agent_web = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) ' \
                     'AppleWebKit/537.36 (KHTML, like Gecko) ' \
                     'Chrome/51.0.2704.103 Safari/537.36'

    def get_question(self, response):
        """Get basic information of questions.

            Continue to get answers if needed. If not, store these information
        """
        try:
            result = self.extractor.parse_response(response)
        except (AttributeError, TypeError):
            return
        # Get reply amount
        m = re.search('replyNum:"(\d+)"', response.body)
        if not m:
            return
        raw_info = {
            'query': response.body,
            'answers': [],
        }
        reply_num = int(m.group(1))
        source_id = self.get_source_id(response)
        if reply_num:
            yield Request(self.api_answers % (0, source_id),
                          meta={'raw_info': raw_info,
                                'result': result,
                                'offset': 0,
                                'reply_num': reply_num,
                                'source_id': source_id},
                          callback=self.get_answers)
        else:
            self.save(source_id, raw_info, result)

    def get_answers(self, response):
        """Get all answers of one question.

            One page contains ten answers. If any answer remains, change the
            offset to get next ten answers. If not, store all these information
        """
        response.meta['raw_info']['answers'].append(response.body)
        response.meta['result']['answers'].extend(
            self.extractor.parse_response_answer(response))
        response.meta['offset'] += 10
        if response.meta['reply_num'] > response.meta['offset']:
            yield Request(self.api_answers % (response.meta['offset'],
                                              response.meta['source_id']),
                          meta=response.meta,
                          callback=self.get_answers)
        else:
            self.save(response.meta['source_id'],
                      response.meta['raw_info'],
                      response.meta['result'])

    def save(self, source_id, raw_info, result):
        raw_json = json.dumps(raw_info, ensure_ascii=False, sort_keys=True)
        page_id = '%s_%s' % (self.get_source_name(), source_id)
        self.storage.save(page_id, raw_json)
        result_json = json.dumps(result, ensure_ascii=False, sort_keys=True)
        with open('%s_result_%s' % (self.name, self.time_stamp), 'a') as output:
            output.write(result_json + '\n')

    @staticmethod
    def get_source_id(response):
        m = re.search('question/(\d+)', response.url)
        return m.group(1)

    def process_user_links(self, links):
        """Process Links for user pages

            Change default user info page to the corresponding baidu_zhidao page
        """
        for link in links:
            m = re.search('p/([^?]+)', link.url)
            if not m:
                continue
            link.url = self.api_user % m.group(1)
        return links

    @staticmethod
    def process_question_links(links):
        """Process links for question pages

            Change https to http can avoid page redirecting, and empty sort
            parameter can get all the answers of one question
        """
        for link in links:
            link.url = link.url.replace('https:', 'http:')
            if '?' in link.url:
                link.url += '&sort='
            else:
                link.url += '?sort='
        return links

    def process_request_headers(self, request):
        """Process request to get web pages for index and wap pages for questions

            Baidu_zhidao change the page contents automatically according to
            User-Agent. Wap user-agent can avoid image-replace-character issue.
            Web user-agent can provide adequate indexes.
        """
        if re.search('question/\d+', request.url) or \
                re.search('qid=\d+', request.url):
            request.headers['User-Agent'] = self.user_agent_wap
        else:
            request.headers['User-Agent'] = self.user_agent_web
