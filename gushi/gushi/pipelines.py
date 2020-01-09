# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

from gushi.MysqlUtil import MysqlUtil
import traceback
import logging

class GushiPipeline(object):
    pool = None

    def __init__(self):
        pass

    def open_spider(self,spider):
        self.pool = MysqlUtil()

    def process_item(self, item, spider):
        try:
            #查询是否存在
            # sql_select = """select count(1) from gushi
            #                 where name = %(poety_name)s   
            #              """
            # params_select = {'poety_name':item['name']}
            # flag = self.pool.get_count(sql_select,params_select)
            # if flag > 0:
            #     logging.info('记录已经存在:[%s][%s]', item['name'], item['author'])
            #     return

            sql_insert = """
                        insert into gushi(id,name,dynasty,author,poetry) 
                        values (%(id)s,%(name)s,%(dynasty)s,%(author)s,%(poetry)s)
                        """
            params = {
                    'id':'111','name':item['name'],'dynasty':item['dynasty'],
                    'author':item['author'],'poetry':str(item['poetry'])
            }
            self.pool.insert_one(sql_insert,params)
            ### 不要忘记提交了
            self.pool.end("commit")
        except Exception as err:
            logging.error('发生异常：[%s]',err)
            traceback.print_exc(err)
            self.pool.end("rollback")

    def close_spider(self,spider):
        pass