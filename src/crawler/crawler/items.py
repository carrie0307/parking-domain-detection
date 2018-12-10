# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class CrawlerItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    '''
    oldDomain = scrapy.Field()
    newDomain = scrapy.Field()
    url_links = scrapy.Field()
    '''

    label = scrapy.Field()
    name = scrapy.Field()
    down_link = scrapy.Field()
    apk_name = scrapy.Field()
