# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup, element


def parse_response(response):
    result = {
        'answers': [],
        'related': [],
        'url': response.url.split('?')[0],
    }
    soup = BeautifulSoup(response.body.replace('<!--', '').replace('-->', ''))
    query_info = soup.find('div', class_='question-container')
    div_info = query_info.find('div', class_='title')
    result['query_title'] = div_info.h2.get_text().strip().encode('utf8')
    div_info = query_info.find('div', class_='cont')
    if div_info:
        result['query_content'] = div_info.get_text().strip().encode('utf8')
    div_info = soup.find('div', id='p-relate-question')
    if div_info:
        a_info = div_info.find_all('a', class_='question-list')
        for a in a_info:
            for span in a.find_all('span'):
                span.decompose()
            if a.contents[0]:
                result['related'].append(a.contents[0].strip().encode('utf8'))
    return result


def parse_response_answer(response):
    result = []
    soup = BeautifulSoup(response.body)
    div_info = soup.find_all('div', class_='reply-item')
    for div in div_info:
        content_info = div.find('div', class_='full-content')
        if not content_info:
            continue
        answer_info = {}
        answer_content = []
        for child in content_info.children:
            if isinstance(child, element.Tag):
                answer_content.append(
                    child.get_text().strip().encode('utf8'))
            else:
                answer_content.append(child.strip().encode('utf8'))
        answer_info['content'] = ' '.join(answer_content)
        up_info = div.find('div', class_='enhance-sup')
        answer_info['up'] = int(up_info.get_text().strip())
        down_info = div.find('div', class_='contra-sup')
        answer_info['down'] = int(down_info.get_text().strip())
        result.append(answer_info)
    return result
