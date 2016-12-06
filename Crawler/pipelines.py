# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import codecs
import functools




class StationPipeline(object):
    def __init__(self):
        self.file = codecs.open("baishi.txt", 'w', encoding ='utf-8')

    def close(self, spider):
        self.file.close()

    #@check_spider_pipeline
    def process_item(self, item, spider):

        name = item['station_name'].strip()
        clean_name = ''
        for j in name.splitlines():
            j = j.rstrip()
            clean_name = clean_name + j
        self.file.writelines(clean_name + "\n")
        return item


class LvYouPipeline(object):
    def __init__(self):
        self.file = codecs.open('lvyou_location.txt', 'w', encoding='utf-8')

    def close(self, spider):
        self.file.close()

    # @check_spider_pipeline
    def process_item(self, item, spider):
        self.file.writelines(item['spot_name'] + " " + item['address_name1'] + " " + item['address_name2'] + " " + item[
            'address_name3'] + " " + item['address_total'] + "\n")


class SubwayPipeline(object):
    def __init__(self):
        self.file = codecs.open('subway_route.txt', 'w', encoding='utf-8')

    def close(self, spider):
        self.file.close()

    # @check_spider_pipeline
    def process_item(self, item, spider):
        self.file.writelines(item['city_name'] + " " + item['subway_name'] + " " + item['path_name'] + "\n")



class SpotPipeline(object):
    def __init__(self):
        self.file = codecs.open('spot_location.txt', 'w', encoding ='utf-8')

    def close(self, spider):
        self.file.close()

    #@check_spider_pipeline
    def process_item(self, item, spider):

        self.file.writelines(item['spot_name'] + " " + item['address_name1'] + " " + item['address_name2'] + "\n")
        return item

class LocationPipeline(object):
    def __init__(self):
        self.file = codecs.open('boya_location.txt', 'w', encoding ='utf-8')

    def close(self, spider):
        self.file.close()

    #@check_spider_pipeline
    def process_item(self, item, spider):

        self.file.writelines(item['title_name1'].strip() + " " + item['title_name2'].strip() + " " + item['title_name3'].strip() + " " + item['title_name4'] + "\n")
        return item

class MeiTuanPipeline(object):
    def __init__(self):
        self.file = codecs.open('meituan_location.txt', 'w', encoding ='utf-8')

    def close(self, spider):
        self.file.close()

    #@check_spider_pipeline
    def process_item(self, item, spider):

        self.file.writelines(item['landmark_name'] + " " + item['area_name'] + " " + item['city_name'] + "\n")
        return item

class ShenZhouPipeline(object):
    def __init__(self):
        self.file = codecs.open('shenzhou_location.txt', 'w', encoding ='utf-8')

    def close(self, spider):
        self.file.close()

    #@check_spider_pipeline
    def process_item(self, item, spider):

        #name = item['location_name'].strip()

        self.file.writelines(item['store_name'].strip() + " " + item['city_name'] + ' ' + item['area_name'] + ' ' + item['address_name'] + "\n")
        return item


class ProxyPipeline(object):
    def __init__(self):
        self.file = codecs.open('proxy.txt', 'w', encoding ='utf-8')

    def close(self, spider):
        self.file.close()

    #@check_spider_pipeline
    def process_item(self, item, spider):

        ip = item['ip'].strip()
        port = item['port'].strip()

        self.file.writelines(ip + ":" + port + "\n")
        return item


class FoodPipeline(object):
    def __init__(self):
        self.file = codecs.open("xinshipu.txt", 'w', encoding ='utf-8')

    def close(self, spider):
        self.file.close()

    #@check_spider_pipeline
    def process_item(self, item, spider):

        name = item['food_name'].strip()
        clean_name = ''
        for j in name.splitlines():
            j = j.rstrip()
            clean_name = clean_name + j
        self.file.writelines(clean_name + "\n")
        return item



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