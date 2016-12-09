# -*- coding: utf-8 -*-
import json
import re
from bs4 import BeautifulSoup


def parse_response(response):
    result = {
        'cast': {},
        'director': [],
        'region': [],
        'tags': [],
        'url': response.url,
    }
    soup = BeautifulSoup(response.body)
    result_info = soup.find('div', class_='result_detail')
    h1_info = result_info.find('h1', class_='main_title')
    a_info = h1_info.find('a')
    result['title_main'] = a_info.text.strip().encode('utf8')
    h3_info = result_info.find('h3', class_='sub_title')
    result['title_sub'] = h3_info.text.strip().encode('utf8')
    em_info = result_info.find('em', rseat='alias')
    result['title_alias'] = em_info.text.split(
        u'：', 1)[-1].strip().encode('utf8')
    div_info = result_info.find('div', class_='score_num_new')
    span_info = div_info.find('span', class_='unit')
    if span_info:
        span_info.decompose()
    result['score'] = float(''.join(div_info.stripped_strings))
    em_info = result_info.find('em', rseat='导演')
    a_info = em_info.find_all('a', title=True)
    for a in a_info:
        result['director'].append(a.text.strip().encode('utf8'))
    div_info = soup.find_all('div', class_='mod-media_body')
    for div in div_info:
        a_info = div.find('a')
        em_info = div.find('em', class_=False)
        result['cast'][a_info.text.strip().encode('utf8')] = \
            em_info.text.strip().encode('utf8')
    em_info = result_info.find('em', rseat='地区')
    a_info = em_info.find_all('a', title=True)
    for a in a_info:
        result['region'].append(a.text.strip().encode('utf8'))
    div_info = result_info.find('div', class_='look_point')
    a_info = div_info.find_all('a', title=True)
    for a in a_info:
        result['tags'].append(a.text.strip().encode('utf8'))
    em_info = result_info.find('em', rseat='总集数')
    if not em_info:
        em_info = result_info.find('em', rseat='更新集数')
    result['episode'] = int(re.search('(\d+)', em_info.text).group(1))
    div_info = soup.find('div', id='upDownWrap')
    result['up_down_id'] = div_info['data-upanddown-albumid']
    if div_info['data-upanddown-site'] == 'iqiyi':
        result['up_down_type'] = 1  # iqiyi origin
    else:
        result['up_down_type'] = 4  # other sources
    return result


def parse_response_vote(response):
    result = {}
    data = json.loads(response.body.split('(')[1].split(')')[0])
    result['up'] = data['data']['up']
    result['down'] = data['data']['down']
    return result
