# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import codecs
import functools

class HaHaPipeline(object):
    def __init__(self):
        self.file = codecs.open('haha.txt', 'w', encoding ='utf-8')

    def close(self, spider):
        self.file.close()

    #@check_spider_pipeline
    def process_item(self, item, spider):

        joke = item['joke_content'].strip().replace("<p>", "").replace(' ', '').replace("</p>", "").replace("&nbsp;", "").replace("<br />", "").replace("&rdquo;","").replace("<br/>", "").replace("&ldquo;", "").replace('&hellip;','').replace('&mdash;','').replace('&lsquo;', '').replace('&rsquo;', '').replace('&zwj;', '').replace('<br>', '')
        clean_joke = ''
        for j in joke.splitlines():
            j = j[2:].rstrip()
            clean_joke = clean_joke + j
        self.file.writelines(clean_joke + "\n")
        return item


class QiuShiPipeline(object):
    def __init__(self):
        self.file = codecs.open('qiushi.txt', 'w', encoding ='utf-8')

    def close(self, spider):
        self.file.close()

    #@check_spider_pipeline
    def process_item(self, item, spider):
        joke = item['joke_content'].strip()
        clean_joke = ''
        self.file.writelines("dddd")
        for j in joke.splitlines():
            j = j.rstrip()
            clean_joke = clean_joke + j
        self.file.writelines(clean_joke + "\n")
        return item

class DuanZiPipeline(object):
    def __init__(self):
        self.file = codecs.open('duanzi.txt', 'w', encoding ='utf-8')

    def close(self, spider):
        self.file.close()

    #@check_spider_pipeline
    def process_item(self, item, spider):
        joke = item['joke_content'].strip()
        clean_joke = ''
        for j in joke.splitlines():
            j = j.rstrip()
            clean_joke = clean_joke + j
        self.file.writelines(clean_joke + "\n")
        return item

class BieDouPipeline(object):
    def __init__(self):
        self.file = codecs.open('biedou.txt', 'w', encoding ='utf-8')

    def close(self, spider):
        self.file.close()

    #@check_spider_pipeline
    def process_item(self, item, spider):
        joke = item['joke_content'].strip()
        clean_joke = ''
        for j in joke.splitlines():
            j = j.rstrip()
            clean_joke = clean_joke + j
        self.file.writelines(clean_joke + "\n")
        return item

class PengFuPipeline(object):
    def __init__(self):
        self.file = codecs.open('pengfu.txt', 'w', encoding ='utf-8')

    def close(self, spider):
        self.file.close()

    #@check_spider_pipeline
    def process_item(self, item, spider):
        joke = item['joke_content'].strip()
        clean_joke = ''
        for j in joke.splitlines():
            j = j.rstrip()
            clean_joke = clean_joke + j
        self.file.writelines(clean_joke + "\n")
        return item

class XiHaPipeline(object):
    def __init__(self):
        self.file = codecs.open('xiha.txt', 'w', encoding ='utf-8')

    def close(self, spider):
        self.file.close()

    #@check_spider_pipeline
    def process_item(self, item, spider):
        joke = item['joke_content'].strip()
        clean_joke = ''
        for j in joke.splitlines():
            j = j.rstrip()
            clean_joke = clean_joke + j
        self.file.writelines(clean_joke + "\n")
        return item