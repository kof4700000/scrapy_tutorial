# -*- coding: utf-8 -*-
import scrapy
from scrapy_tutorial.items import comicItem, comicCategory
import re
import os
from urlparse import urljoin

project_dir = os.path.abspath(os.path.dirname(__file__))

class TbgxSpider(scrapy.Spider):
    name = 'test'
    log_file = '/var/myproject/scrapy_tutorial/' + name + '.log'
    begin_url = "http://comic.kukudm.com/comiclist/2416/index.htm"
    #allowed_domains = ["comic.kukudm.com/"]
    custom_settings = {
        'IMAGES_URLS_FIELD' :"image_url",
        'IMAGES_STORE':os.path.join(project_dir,'images'),
        'IMAGES_EXPIRES': 90,
    #'FEED_EXPORT_ENCIDING':'utf-8',
        'ITEM_PIPELINES':{
        'scrapy_tutorial.pipelines.ComicPipeline': 300,
        'scrapy_tutorial.pipelines.ImagePipeline2': 200,
        #'scrapy.pipelines.images.ImagesPipeline':200, 
        },
        'LOG_FILE':log_file
    }

    def start_requests(self):
        yield scrapy.Request(self.begin_url, self.get_volume)

    def get_volume(self, response):
        current_page = 0
        volume_href = response.css("#comiclistn > dd > a:nth-child(1)::attr('href')").extract()
        volume_name = response.css("#comiclistn > dd > a:nth-child(1)::text").extract()
        volumes = zip(volume_href, volume_name)
        volume_num = 0
        item = comicCategory()
        item['name'] = self.name
        item['display_name'] = response.xpath("/html/body/table[5]/tr/td[2]/table/tr[1]/td/table/tr[1]/td/text()").extract()[0]
        item['tag'] = 'funny'
        detail = response.xpath("/html/body/table[5]/tr/td[2]/table/tr[1]/td/table/tr[5]/td/text()").extract()[0].split('|')
        item['author'] = detail[0]
        img_url = response.css('td > table > tr:nth-child(2) > td > img::attr(src)').extract()
        item['image_url'] = img_url
        item['summary'] = response.css("#ComicInfo::text").extract()[0]
        #if check_repeating(self.name):
        #    return
        yield item
        for each in volumes:
            volume_num = volume_num + 1
            gallery = urljoin("http://comic.kukudm.com/", each[0])
            request = scrapy.Request(gallery, callback = self.parse)
            request.meta['volume_name'] = each[1]
            request.meta['volume'] = volume_num
            request.meta['current_page'] = current_page
            yield request

    def parse(self, response):
        compile_array = ['server\+.*?>','m[0-9]{6}d\+.*?>','k[0-9]{4}k\+.*?>']
        for each in compile_array:
            pattern1 = re.compile(each)
            result1 = re.findall(pattern1,response.text)
            if result1 != []:
                result1 = result1[0].split('+')[1].replace("\"","").replace("'","").replace(">","")
                break
            #pattern1 = re.compile('m201001d+.*?>')
            #pattern1 = re.compile('m201304d+.*?>')
            #result1 = re.findall(pattern1,response.text)
            #result1 = result1[0].split('+')[1].replace("\"","").replace("'","").replace(">","")
        assert result1
        item = comicItem()
        img_url = "http://n5.1whour.com/" + result1
        item['name'] = self.name
        current_page = response.meta['current_page']
        current_page = current_page + 1
        item['page'] = current_page
        item['volume'] = response.meta['volume']
        item['volume_name'] = response.meta['volume_name']
        item['image_url'] = []
        item['image_url'].append(img_url) #image pipeline must be list
        yield item
        #pattern2 = re.compile('comiclist.*?htm')
        #result2 = re.findall(pattern2,response.text)
        result2 = response.css("td > a::attr(href)").extract()[-1]
        if result2 is not None:
            next_url =  "http://comic.kukudm.com" + result2
            self.logger.info('Crawling %s', next_url)
            yield response.follow(next_url, 
                                  callback=self.parse, 
                                  meta={'volume':response.meta['volume'],
                                        'current_page':current_page,
                                        'volume_name':response.meta['volume_name']})
    @staticmethod
    def close(spider, reason):
        #pwd = os.getcwd()
        os.system('mv /var/myproject/scrapy_tutorial/scrapy_tutorial/spiders/images/full/* /var/myproject/scrapy_tutorial/scrapy_tutorial/spiders/images/test')
        closed = getattr(spider, 'closed', None)
        if callable(closed):
            return closed(reason)

