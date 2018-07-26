import scrapy
import re


class QuotesSpider2(scrapy.Spider):
    name = "quotes2"
    start_urls = [
        "http://comic.kukudm.com/comiclist/221/3007/1.htm"
    ]

    def parse(self, response):
        pattern1 = re.compile('server+.*?>')
        result1 = re.findall(pattern1,response.text)
        result1 = result1[0].split('+')[1].replace("\"","").replace("'","").replace(">","")
        img_url = "http://n5.1whour.com/" + result1
        #pattern2 = re.compile('comiclist.*?htm')
        #result2 = re.findall(pattern2,response.text)
        result2 = response.css("td > a::attr(href)").extract()[-1]
        if result2 is not None:
            next_url =  "http://comic.kukudm.com" + result2
            #print next_url
            yield response.follow(next_url, callback=self.parse)
