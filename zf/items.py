# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ZfItem(scrapy.Item):
    # define the fields for your item here like:
    id = scrapy.Field()
    name = scrapy.Field()
    price = scrapy.Field()
    housing_estate = scrapy.Field()
    housing_point = scrapy.Field()
    area = scrapy.Field()
    address = scrapy.Field()
    desc = scrapy.Field()
    image_urls = scrapy.Field()
    images = scrapy.Field()
    source = scrapy.Field()
    addtime = scrapy.Field()
