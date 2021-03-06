# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ScrapyTutorialItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class comicCategory(scrapy.Item):
    name = scrapy.Field()
    display_name = scrapy.Field()
    tag = scrapy.Field()
    author = scrapy.Field()
    summary = scrapy.Field()
    thumbnail = scrapy.Field()
    image_url = scrapy.Field()

class comicItem(scrapy.Item):
    name = scrapy.Field()
    page = scrapy.Field()
    volume = scrapy.Field()
    volume_name = scrapy.Field()
    image_url = scrapy.Field()
    path = scrapy.Field()
    display_name = scrapy.Field()
    tag = scrapy.Field()
