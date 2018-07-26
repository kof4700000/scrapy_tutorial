# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import mysql.connector
from scrapy.conf import settings
from scrapy.pipelines.images import ImagesPipeline
from .items import comicCategory

class ScrapyTutorialPipeline(object):

    def open_spider(self, spider):
        self.conn = mysql.connector.connect(user='comic', password='123456', database='comic', )
        self.cursor = self.conn.cursor()
        #self.client = pymongo.MongoClient(self.mongo_uri)
        #self.db = self.client[self.mongo_db]

    def close_spider(self, spider):
        self.cursor.close()
        self.conn.close()

    def process_item(self, item, spider):
        name = item['name']
        print("*" * 10)
        print(name)
        insert_sql = 'insert into test(name) VALUES (%s)'
        self.cursor.execute("insert into test(name) values('%s')" %(name))
        #self.cursor.execute(insert_sql, name)
        self.conn.commit() 
        return item

class TestPipeline(object):
    def __init__(self, user, pwd, database):
        self.db_user = user
        self.db_pwd = pwd
        self.database = database

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            user = settings['MYSQL_USER'],
            pwd = settings['MYSQL_PWD'],
            database = settings['MYSQL_DATABASE'],
            #mongo_uri=crawler.settings.get('MONGO_URI'),
            #mongo_db=crawler.settings.get('MONGO_DATABASE', 'items')
        )

    def open_spider(self, spider):
        self.conn = mysql.connector.connect(user=self.db_user,
                                            password=self.db_pwd, 
                                            database=self.database)
        self.cursor = self.conn.cursor()

    def close_spider(self, spider):
        self.cursor.close()
        self.conn.close()

    def process_item(self, item, spider):
        name = item['name']
        insert_sql = 'insert into test(name) VALUES (%s)'
        self.cursor.execute("insert into test(name) values('%s')" %(name))
        self.conn.commit() 
        return item

class ComicPipeline(object):
    def __init__(self, user, pwd, database):
        self.db_user = user
        self.db_pwd = pwd
        self.database = database

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            user = settings['MYSQL_USER'],
            pwd = settings['MYSQL_PWD'],
            database = settings['MYSQL_DATABASE'],
        )

    def open_spider(self, spider):
        self.conn = mysql.connector.connect(user=self.db_user,
                                            password=self.db_pwd, 
                                            database=self.database)
        self.cursor = self.conn.cursor()

    def close_spider(self, spider):
        self.cursor.close()
        self.conn.close()

    def process_item(self, item, spider):
        if isinstance(item, comicCategory):
            name = item['name']
            display_name = item['display_name']
            tag = item['tag']
            author = item['author']
            summary = item['summary']
            thumbnail = item['thumbnail']
            self.cursor.execute("insert into gallery(name, display_name, tag, author, summary, thumbnail) values('%s','%s','%s','%s','%s','%s')" %(name, display_name, tag, author, summary, thumbnail))
            self.conn.commit()
            return item 
        name = item['name']
        page = item['page']
        volume = item['volume']
        volume_name = item['volume_name']
        path = item['path']
        #insert_sql = "insert into comic(title, page, volume) VALUES ('%s',)"
        self.cursor.execute("insert into image(name, page, volume, path, volume_name) values('%s','%s','%s','%s','%s')" %(name, page, volume, path, volume_name))
        self.conn.commit() 
        return item

from scrapy.pipelines.images import ImagesPipeline
from scrapy.http import Request

class ImagePipeline(ImagesPipeline):

    def item_completed(self, results, item, info):
        for ok,value in results:
            image_file_path=value['path']
            item['path']=image_file_path
        return item

class ImagePipeline2(ImagesPipeline):

    def get_media_requests(self, item, info):
        if isinstance(item, comicCategory):
            return [Request(x, meta={"type":"thumbnail","name":item['name']}) for x in item.get(self.images_urls_field, [])]
        return [Request(x, meta={"volume":item['volume'],"page":item['page'], "name":item['name']}) for x in item.get(self.images_urls_field, [])]
        
    def file_path(self, request, response=None, info=None):
        try:
            if request.meta['type'] == 'thumbnail':
                image_guid = request.meta['name']
                return 'full/%s-thumbnail.jpg' % (image_guid)
        except:
            image_guid = request.meta['name'] + '-' + str(request.meta['volume']) + '-' + str(request.meta['page'])
        return 'full/%s.jpg' % (image_guid)

    def item_completed(self, results, item, info):
        for ok,value in results:
            if isinstance(value, dict):
                image_file_path=value['path']
                if isinstance(item, comicCategory):
                    item['thumbnail']=image_file_path
                else:
                    item['path']=image_file_path
        return item

