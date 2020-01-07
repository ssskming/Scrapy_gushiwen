# -*- coding: utf-8 -*-
import scrapy


class GushiwenSpider(scrapy.Spider):
    name = 'gushiwen'
    allowed_domains = ['https://www.gushiwen.org']
    start_urls = ['http://https://www.gushiwen.org/']

    def parse(self, response):
        pass
