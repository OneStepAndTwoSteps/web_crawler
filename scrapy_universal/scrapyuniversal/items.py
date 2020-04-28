# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ScrapyuniversalItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass



class NewsItem(scrapy.Item):

    title = scrapy.Field()
    url   = scrapy.Field()
    text  = scrapy.Field()
    datetime  = scrapy.Field()
    source    = scrapy.Field()
    website   = scrapy.Field()





