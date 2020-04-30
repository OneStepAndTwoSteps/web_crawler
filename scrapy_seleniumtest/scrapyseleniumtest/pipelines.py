# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


import pymysql

class MysqlPipeline(object):
    def __init__(self,host,database,user,passwd,port):
        self.host = host
        self.database = database
        self.user = user
        self.passwd = passwd
        self.port = port

    @classmethod
    def from_crawler(cls,crawler):
        return cls(host=crawler.settings.get('MYSQL_HOST'),
            database=crawler.settings.get('MYSQL_DATABASE'),
            user=crawler.settings.get('MYSQL_USER'),
            passwd=crawler.settings.get('MYSQL_PASSWORD'),
            port=crawler.settings.get('MYSQL_PORT'),)

    def open_spider(self,spider):   # 默认需要的参数 spider
        self.db = pymysql.connect(self.host,self.user,self.passwd,self.database,charset='utf8',port=self.port) # utf8 不是utf-8
        self.cursor = self.db.cursor()

    def close_spider(self,spider):
        self.db.close()
    
    def process_item(self,item,spider):
        
        data = dict(item)
        keys = ', '.join(data.keys())
        values = ', '.join(['%s'] * len(data))
        sql = 'insert into %s (%s) values (%s)' % (item.table, keys, values) 
        self.cursor.execute(sql, tuple(data.values()))
        self.db.commit()

        return item



