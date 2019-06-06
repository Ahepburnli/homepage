# -*- coding: utf-8 -*-
import scrapy
from pymysql import *
import pandas as pd
import re
import logging
from homepage.settings import MYSQL_HOST, MYSQL_PORT, MYSQL_DB, MYSQL_USER, MYSQL_PASSWORD, MYSQL_CHARSET
from homepage.items import HomepageItem


class HomeSpider(scrapy.Spider):
    name = 'home'
    allowed_domains = ['home.com']

    # start_urls = ['http://home.com/']



    def start_requests(self):
        # 连接mysql数据库
        self.conn = connect(host=MYSQL_HOST, db=MYSQL_DB, port=MYSQL_PORT, user=MYSQL_USER,
                            password=MYSQL_PASSWORD, charset=MYSQL_CHARSET
                            )

        sql = 'select url from fb_homepage where likeCount=0'
        self.conn.ping(reconnect=True)  # 若mysql连接失败就重连
        df = pd.read_sql(sql, self.conn)  # 使用pandas从mysql中取出url
        # print(df)
        for url in df['url'].get_values():
            url = url
            yield scrapy.Request(url, callback=self.parse)

    def parse(self, response):
        if response.status == 200:
            item = HomepageItem()
            # 主页id
            pageId = response.xpath('.').re('"pageID":"(\d*?)"')
            item['pageId'] = pageId[0] if pageId else ''
            # 主页点赞次数
            likeCount1 = response.xpath('.').re(
                '<div class="_4bl9"><div>([0-9\,0-9]*?) people like this</div>')
            likeCount2 = response.xpath('.').re(
                '<div class="_4bl9"><div>([0-9\,0-9]*?) 位用户赞了</div>')
            likeCount = likeCount1 if likeCount1 else likeCount2
            likeCount = likeCount[0] if likeCount else '0'
            if ',' in likeCount:
                item['likeCount'] = int(''.join(likeCount.split(',')))
            else:
                item['likeCount'] = int(likeCount)
            logging.debug('likecount is ------------%s' % item['likeCount'])
            print('likecount is ------------%s' % item['likeCount'])
            # 粉丝数
            fansCount1 = response.xpath('.').re(
                '<div class="_4bl9"><div>([0-9\,0-9]*?) people follow this</div>')
            fansCount2 = response.xpath('.').re(
                '<div class="_4bl9"><div>([0-9\,0-9]*?) 位用户关注了</div>')
            fansCount = fansCount1 if fansCount1 else fansCount2
            fansCount = fansCount[0] if fansCount else '0'
            if ',' in fansCount:
                item['fansCount'] = int(''.join(fansCount.split(',')))
            else:
                item['fansCount'] = int(fansCount)
            logging.debug('fanscount is ------------%s' % item['fansCount'])
            print('fanscount is ------------%s' % item['fansCount'])

            yield item
