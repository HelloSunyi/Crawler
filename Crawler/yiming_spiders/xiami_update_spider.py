# -*- coding: utf-8 -*-
import time
from xiami_spider import *


class XiamiUpdateSpider(XiamiSpider):

    name = 'xiami_update'
    download_delay = 5
    proxy_stable = False
    rules = ()
    api_url = 'http://www.xiami.com/album/list/type/all/' \
              'year/%d/month/%d/p/pub/page/%d'

    def start_requests(self):
        year = time.localtime(self.time_stamp).tm_year
        month = time.localtime(self.time_stamp).tm_mon
        date = time.localtime(self.time_stamp).tm_mday
        yield Request(self.api_url % (year, month, 1),
                      meta={'year': year, 'month': month,
                            'date': date, 'offset': 1},
                      callback=self.get_update)

    def get_update(self, response):
        soup = BeautifulSoup(response.body)
        div_info = soup.find_all('div', class_='info')
        for div in div_info:
            p_info = div.find_all('p')
            m = re.search('(\d+)年(\d+)月(\d+)日', p_info[-1].text.encode('utf8'))
            if not m:
                continue
            if int(m.group(3)) >= response.meta['date']:
                a_info0 = p_info[1].find('a')
                a_info1 = p_info[0].find('a')
                yield Request(urlparse.urljoin(response.url, a_info0['href']),
                              meta={'album': urlparse.urljoin(response.url,
                                                              a_info1['href'])},
                              callback=self.get_info)
            else:
                break
        else:
            response.meta['offset'] += 1
            yield Request(self.api_url % (response.meta['year'],
                                          response.meta['month'],
                                          response.meta['offset']),
                          meta=response.meta,
                          callback=self.get_update)

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
        response.meta['requests'].append(response.meta['album'])
