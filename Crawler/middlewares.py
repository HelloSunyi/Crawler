# -*- coding: utf-8 -*-
import json
import urllib
from urlparse import urlparse
from settings import PROXY_SERVER


class HeadersMiddleware(object):

    @staticmethod
    def process_request(request, spider):
        spider.process_request_headers(request)


class ProxyManagerMiddleware(object):

    @staticmethod
    def process_request(request, spider):
        """Fetch proxy from pool according to download_slot"""
        if not spider.proxy_stable:
            return
        # generate download_slot
        download_slot = request.meta.get('download_slot')
        if not download_slot:
            download_slot = urlparse(request.url).netloc
        query = {'download_slot': download_slot}
        # fetch proxy from proxy_server
        try:
            raw = urllib.urlopen('%s/proxy_stable/get_proxy' % PROXY_SERVER,
                                 data=urllib.urlencode(query)).read()
        except IOError:
            return
        data = json.loads(raw)
        if data['status']:
            return
        # bind proxy and download_slot
        request.meta['proxy'] = data['proxy']
        request.meta['download_slot'] = '%s_%s' % (download_slot, data['proxy'])
