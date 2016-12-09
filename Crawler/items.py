# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


import scrapy

class JokeItem(scrapy.Item):
    joke_content = scrapy.Field()

class FoodItem(scrapy.Item):
    food_name = scrapy.Field()

class LocationItem(scrapy.Item):
    title_name1 = scrapy.Field()
    title_name2 = scrapy.Field()
    title_name3 = scrapy.Field()
    title_name4 = scrapy.Field()

class ProxyItem(scrapy.Item):
    ip = scrapy.Field()
    port = scrapy.Field()

class StationItem(scrapy.Item):
    station_name = scrapy.Field()

class ShenZhouItem(scrapy.Item):
    store_name = scrapy.Field()
    city_name = scrapy.Field()
    area_name = scrapy.Field()
    address_name = scrapy.Field()

class MeiTuanItem(scrapy.Item):
    landmark_name = scrapy.Field()
    city_name = scrapy.Field()
    area_name = scrapy.Field()

class SpotItem(scrapy.Item):
    spot_name = scrapy.Field()
    address_name1 = scrapy.Field()
    address_name2 = scrapy.Field()

class LvYouItem(scrapy.Item):
    spot_name = scrapy.Field()
    address_name1 = scrapy.Field()
    address_name2 = scrapy.Field()
    address_name3 = scrapy.Field()
    address_total = scrapy.Field()

class SubwayItem(scrapy.Item):
    subway_name = scrapy.Field()
    city_name = scrapy.Field()
    path_name = scrapy.Field()

class FootballItem(scrapy.Item):
    team_name = scrapy.Field()#0
    country = scrapy.Field()#1
    founded_time = scrapy.Field()#2
    league = scrapy.Field()#3
    coach = scrapy.Field()#4
    city = scrapy.Field()#5
    court = scrapy.Field()#6
    official_website = scrapy.Field()#7

class AnZhuoItem(scrapy.Item):
    name = scrapy.Field()
    producer = scrapy.Field()
    hot_level = scrapy.Field()
    size = scrapy.Field()
    category = scrapy.Field()
    update_time = scrapy.Field()
    firmware = scrapy.Field()
    grade = scrapy.Field()
    description = scrapy.Field()
    update_info = scrapy.Field()
