# -*- coding: utf-8 -*-
import scrapy
from scrapy_tutorial.items import comicItem, comicCategory
import re
import os
from urlparse import urljoin

project_dir = os.path.abspath(os.path.dirname(__file__))

class TbgxSpider(scrapy.Spider):
    name = 'tbgx'
    #allowed_domains = ["comic.kukudm.com/"]
    #start_urls = [
    #    "http://comic.kukudm.com/comiclist/221/"
    #]
    custom_settings = {
        'IMAGES_URLS_FIELD' :"image_url",
        'IMAGES_STORE':os.path.join(project_dir,'images'),
        'IMAGES_EXPIRES': 90,
    #'FEED_EXPORT_ENCIDING':'utf-8',
        'ITEM_PIPELINES':{
        'scrapy_tutorial.pipelines.ComicPipeline': 300,
        'scrapy_tutorial.pipelines.ImagePipeline': 200,
        #'scrapy.pipelines.images.ImagesPipeline':200, 
        },
    }

    def get_volume(self, response):
        current_page = 0
        volumes = response.css("#comiclistn > dd > a:nth-child(1)::attr('href')").extract()
        volume_num = 0
        item = comicCategory()
        item['name'] = 'tbgx'
        item['display_name'] = response.xpath("/html/body/table[5]/tr/td[2]/table/tr[1]/td/table/tr[1]/td/text()").extract()[0]
        item['tag'] = 'funny'
        detail = response.xpath("/html/body/table[5]/tr/td[2]/table/tr[1]/td/table/tr[5]/td/text()").extract()[0].split('|')
        item['author'] = detail[0]
        item['summary'] = response.css("#ComicInfo::text").extract()[0]
        yield item
        for each in volumes:
            volume_num = volume_num + 1
            gallery = urljoin("http://comic.kukudm.com/", each)
            request = scrapy.Request(gallery, callback = self.parse)
            request.meta['volume'] = volume_num
            request.meta['current_page'] = current_page
            yield request

    def start_requests(self):
        yield scrapy.Request("http://comic.kukudm.com/comiclist/221/", self.get_volume)

    def parse(self, response):
        try:
            pattern1 = re.compile('server+.*?>')
            result1 = re.findall(pattern1,response.text)
            result1 = result1[0].split('+')[1].replace("\"","").replace("'","").replace(">","")
        except IndexError:
            pattern1 = re.compile('m201001d+.*?>')
            result1 = re.findall(pattern1,response.text)
            result1 = result1[0].split('+')[1].replace("\"","").replace("'","").replace(">","")
        assert result1
        item = comicItem()
        img_url = "http://n5.1whour.com/" + result1
        item['name'] = 'tbgx'
        current_page = response.meta['current_page']
        current_page = current_page + 1
        item['page'] = current_page
        item['volume'] = response.meta['volume']
        item['image_url'] = []
        item['image_url'].append(img_url) #image pipeline must be list
        yield item
        #pattern2 = re.compile('comiclist.*?htm')
        #result2 = re.findall(pattern2,response.text)
        result2 = response.css("td > a::attr(href)").extract()[-1]
        if result2 is not None:
            next_url =  "http://comic.kukudm.com" + result2
            yield response.follow(next_url, 
                                  callback=self.parse, 
                                  meta={'volume':response.meta['volume'],'current_page':current_page})
