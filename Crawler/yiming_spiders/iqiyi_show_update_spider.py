# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
from iqiyi_show_spider import *


class IqiyiShowUpdateSpider(IqiyiShowSpider):

    name = 'iqiyi_show_update'
    rules = ()
    start_url = 'http://www.iqiyi.com/lib/zongyi/,,_4_1.html'

    def start_requests(self):
        yield Request(self.start_url, callback=self.get_index)

    def get_index(self, response):
        soup = BeautifulSoup(response.body)
        ul_info = soup.find('ul', class_='site-piclist-auto')
        a_info = ul_info.find_all('a', class_=True)
        for a in a_info:
            yield Request(a['href'], callback=self.get_series)
