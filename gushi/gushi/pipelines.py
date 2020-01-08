# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

from twisted.enterprise import adbapi
from pymysql import cursors

class GushiPipeline(object):
    def __init__(self,conn):
        self.conn = conn
        self.conn.update({'cursorclass':cursors.DictCursor})
        print('=======>',self.conn)
        self.dbpool = adbapi.ConnectionPool('pymysql',**self.conn)
        self._sql = None

    @classmethod
    def from_crawler(cls,crawler): #创建对象读取配置文件
        conn_info = crawler.setting.get('DB')
        return cls(conn_info)

    @property
    def sql(self):
        if not self._sql:
            self._sql = """insert into gushi(id,name,dynasty,author,poetry) values(null,%s,%s,%s,%s)"""
            return self._sql

    def _insert_item(self,cursor,item):
        params = (
                item['name'],
                item['dynasty'],
                item['author'],
                item['poetry']
        )
        cursor.execute(self.sql,params)

    def process_item(self, item, spider):
        defer = self.dbpool.runInteraction(self,self._insert_item,item)
        defer.addErrback(self._handle_error,item,spider)
        return item

    def _handle_error(self,failue,item,spider):
        pass

    def close_spider(self,spider):
        pass