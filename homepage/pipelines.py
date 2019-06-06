# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

from pymysql import *

from homepage.settings import MYSQL_HOST, MYSQL_PORT, MYSQL_DB, MYSQL_USER, MYSQL_PASSWORD, MYSQL_CHARSET


class HomepagePipeline(object):
    def __init__(self):
        self.conn = connect(host=MYSQL_HOST, db=MYSQL_DB, port=MYSQL_PORT, user=MYSQL_USER,
                            password=MYSQL_PASSWORD, charset=MYSQL_CHARSET
                            )
        self.cs1 = self.conn.cursor()

    def process_item(self, item, spider):
        if spider.name == 'home':
            sql = 'update fb_homepage set likeCount=%s, fansCount=%s'
            self.conn.ping(reconnect=True)
            self.cs1.execute(sql, (item['likeCount'], item['fansCount']))
            self.conn.commit()  # 提交操作
        return item

    def close_spider(self,spider):
        if spider.name == 'home':
            # 关闭游标和连接
            self.cs1.close()
            self.conn.close()