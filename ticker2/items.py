# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class Ticker2Item(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    link = scrapy.Field()
    datex = scrapy.Field()
    title = scrapy.Field()
    content = scrapy.Field()
    polarity = scrapy.Field()
