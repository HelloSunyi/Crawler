# -*- coding: utf-8 -*-
import json
import re
import urlparse
from bs4 import BeautifulSoup
from scrapy import signals
from scrapy.http import Request
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule
from scrapy.xlib.pydispatch import dispatcher
from base_spider import BaseSpider
from ..extractors import xiami_extractor


class XiamiSpider(BaseSpider):

    name = 'xiami'
    extractor = xiami_extractor
    download_delay = 0.1
    proxy_stable = True
    start_urls = ['http://www.xiami.com/']
    allowed_domains = [
        'www.xiami.com',
        'i.xiami.com',
    ]
    rules = (
        # Find some available indexes
        Rule(LinkExtractor(allow=('com/chart', 'com/genre', 'com/zone', ))),
        # Find collect pages
        Rule(LinkExtractor(allow=('com/collect$', 'com/collect/\d+', ))),
        # Find artist indexes
        Rule(LinkExtractor(allow=('artist/index', 'artist/tag', ))),
        # Find artist pages
        Rule(LinkExtractor(allow=('com/artist/\w+$', 'search/find/artist', )),
             process_request='store_artists'),
    )
    set_artist = set()
    api_count = 'http://www.xiami.com/count/getplaycount?id=%s&type=song'

    def __init__(self):
        super(XiamiSpider, self).__init__()
        dispatcher.connect(self.spider_idle, signals.spider_idle)

    def store_artists(self, request):
        """Store artist urls into set rather than send requests"""
        if request.url not in self.set_artist:
            with open('xiami_artist_%s' % self.time_stamp, 'a') as output:
                output.write(request.url + '\n')
            self.set_artist.add(request.url)
        return None

    def spider_idle(self):
        """Send 10 requests of artist when request queue is empty in order to
        limit memory consumption"""
        count = 10
        while self.set_artist and count:
            count -= 1
            url = self.set_artist.pop()
            request = Request(url, dont_filter=True, callback=self.get_info)
            self.crawler.engine.crawl(request, self)

    def get_info(self, response):
        """Find callback function for different urls"""
        try:
            if re.search('artist/\d+', response.url) or \
                    re.search('i\.xiami\.com/[^/]+$', response.url):
                self.get_artist(response)
            elif re.search('album/\d+', response.url):
                self.get_albums(response)
            elif re.search('song/\d+', response.url):
                self.get_songs(response)
            elif 'count/getplaycount' in response.url:
                self.get_count(response)
            else:
                self.get_pages(response)
        except (AttributeError, TypeError):
            return
        request = self.gen_info(response)
        if not request:
            self.save(response.meta['source_id'],
                      response.meta['raw_info'],
                      response.meta['result'])
        else:
            yield request

    def get_artist(self, response):
        result = self.extractor.parse_response(response)
        raw_info = {
            'html': response.body,
            'albums': [],
        }
        source_id = self.get_source_id(response)
        if 'redirect_urls' in response.meta:
            response.meta.pop('redirect_times')
            response.meta.pop('redirect_ttl')
            response.meta.pop('redirect_urls')
        response.meta.update({'requests': [],
                              'raw_info': raw_info,
                              'result': result,
                              'source_id': source_id})
        soup = BeautifulSoup(response.body)
        album_info = soup.find('div', id='artist_album')
        if album_info:
            a_info = album_info.find('a', class_='more')
            response.meta['requests'].append(urlparse.urljoin(response.url,
                                                              a_info['href']))

    @staticmethod
    def get_pages(response):
        soup = BeautifulSoup(response.body)
        div_info = soup.find('div', class_='albumBlock_list')
        p_info = div_info.find_all('p', class_='cover')
        for p in p_info:
            if p.find('span', class_='pubbing'):
                continue
            response.meta['requests'].append(urlparse.urljoin(response.url,
                                                              p.a['href']))
        a_info = soup.find('a', class_='p_redirect_l')
        if a_info:
            response.meta['requests'].append(urlparse.urljoin(response.url,
                                                              a_info['href']))

    def get_albums(self, response):
        raw_info = {
            'html': response.body,
            'songs': [],
        }
        response.meta['raw_info']['albums'].append(raw_info)
        response.meta['result']['albums'].append(
            self.extractor.parse_response_album(response))
        soup = BeautifulSoup(response.body)
        td_info = soup.find_all('td', class_='song_name')
        for td in td_info:
            response.meta['requests'].append(urlparse.urljoin(response.url,
                                                              td.a['href']))

    def get_songs(self, response):
        response.meta['raw_info']['albums'][-1]['songs'].append(response.body)
        response.meta['result']['albums'][-1]['songs'].append(
            self.extractor.parse_response_song(response))
        m = re.search('song/(\d+)', response.url)
        response.meta['requests'].append(self.api_count % m.group(1))

    @staticmethod
    def get_count(response):
        data = json.loads(response.body)
        response.meta['result']['albums'][-1]['songs'][-1][
            'song_played'] = data['plays']

    def gen_info(self, response):
        if not response.meta['requests']:
            return None
        url = response.meta['requests'].pop()
        request = Request(url, meta=response.meta, callback=self.get_info)
        if re.search('song/\d+', url):
            self.download_delay = 1
            request.meta['download_slot'] = 'song'
        return request

    def save(self, source_id, raw_info, result):
        raw_json = json.dumps(raw_info, ensure_ascii=False, sort_keys=True)
        page_id = '%s_%s' % (self.get_source_name(), source_id)
        if self.storage:
            self.storage.save(page_id, raw_json)
        result_json = json.dumps(result, ensure_ascii=False, sort_keys=True)
        with open('%s_result_%s' % (self.name, self.time_stamp), 'a') as output:
            output.write(result_json + '\n')

    @staticmethod
    def get_source_id(response):
        m = re.search("id = '(\d+)'", response.body)
        return m.group(1)

    @staticmethod
    def process_request_headers(request):
        """Process request to get 200 response for xiami

            Xiami checks User-Agent in headers. Keep referer empty can keep
            away from login operation.
        """
        request.headers.setdefault('User-Agent',
                                   'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) '
                                   'AppleWebKit/537.36 (KHTML, like Gecko) '
                                   'Chrome/51.0.2704.103 Safari/537.36')
        if 'redirect_urls' not in request.meta:
            request.headers['Referer'] = None
