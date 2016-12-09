# -*- coding: utf-8 -*-
import re
from bs4 import BeautifulSoup


def parse_response(response):
    result = {
        'albums': [],
        'artist_fans': 0,
        'artist_genre': [],
        'artist_name': [],
        'url': response.url.split('?')[0],
    }
    soup = BeautifulSoup(response.body)
    div_info = soup.find('div', id='title')
    if not div_info:
        div_info = soup.find('div', id='glory-title')
    for name in div_info.stripped_strings:
        result['artist_name'].append(name.encode('utf8').strip('()'))
    a_info = soup.find('a', href=re.compile('fans'), title=True)
    if a_info:
        result['artist_fans'] = int(a_info.contents[0])
    div_info = soup.find('div', id='artist_info')
    a_info = div_info.find_all('a', href=re.compile('genre'))
    for a in a_info:
        result['artist_genre'].append(a.text.strip().encode('utf8'))
    return result


def parse_response_album(response):
    result = {
        'album_genre': [],
        'album_name': [],
        'songs': [],
        'url': response.url.split('?')[0],
    }
    soup = BeautifulSoup(response.body)
    div_info = soup.find('div', id='title')
    b_info = div_info.find('b')
    if b_info:
        b_info.decompose()
    for name in div_info.stripped_strings:
        result['album_name'].append(name.encode('utf8').strip('()'))
    div_info = soup.find('div', id='album_info')
    a_info = div_info.find_all('a', href=re.compile('genre'))
    for a in a_info:
        result['album_genre'].append(a.text.strip().encode('utf8'))
    return result


def parse_response_song(response):
    result = {
        'song_name': [],
        'song_played': 0,
        'song_shared': 0,
        'url': response.url,
    }
    soup = BeautifulSoup(response.body)
    div_info = soup.find('div', id='title')
    a_info = div_info.h1.find('a')
    if a_info:
        a_info.decompose()
    for name in div_info.stripped_strings:
        result['song_name'].append(name.encode('utf8').strip('()'))
    result['song_name'] = div_info.h1.contents[0].strip().encode('utf8')
    div_info = soup.find('div', class_='music_counts')
    result['song_shared'] = int(div_info.ul.li.contents[0])
    return result
