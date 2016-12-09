# -*- coding: utf-8 -*-
import re
from bs4 import BeautifulSoup


def parse_response(response):
    result = {
        'url': response.url,
        'menu': [],
    }
    soup = BeautifulSoup(response.body)
    meta_info = soup.find('meta', itemprop='name')
    result['name'] = meta_info['content'].strip().encode('utf8')
    script_info = soup.find('script', class_='J-panels')
    soup_script = BeautifulSoup(script_info.get_text())
    p_info = soup_script.find('p', class_='recommend-name')
    a_info = p_info.find_all(title=True)
    for a in a_info:
        result['menu'].append(a['title'].strip().encode('utf8'))
    div_info = soup.find('div', class_='breadcrumb')
    a_info = div_info.find('a', href=re.compile('g\d+'))
    result['category'] = a_info.get_text().strip().encode('utf8')
    return result
