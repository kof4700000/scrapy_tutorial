# -*- coding: utf-8 -*-
import scrapy
from scrapy_tutorial.items import comicCategory

class HomeSpider(scrapy.Spider):
    name = 'home'
    allowed_domains = ["comic.kukudm.com/"]
    start_urls = [
        "http://comic.kukudm.com/comictype/3_1.htm"
    ]
    custom_settings = {
    #'FEED_EXPORT_ENCIDING':'utf-8',
        'ITEM_PIPELINES':{
        'scrapy_tutorial.pipelines.TestPipeline': 300,
        }
    }

    def parse(self, response):
        for comic_front in response.css("#comicmain > dd > a:nth-child(2)::text").extract():
            item = comicCategory()
            item['name'] = comic_front 
            yield item
        #result2 = response.css("td > a::attr(href)").extract()[-1]
        #if result2 is not None:
        #    next_url =  "http://comic.kukudm.com" + result2
        #    yield response.follow(next_url, callback=self.parse)

