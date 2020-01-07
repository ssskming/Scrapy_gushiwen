# -*- coding: utf-8 -*-
import scrapy
from gushi.items import GushiItem


class GushiwenSpider(scrapy.Spider):
    name = 'gushiwen'
    allowed_domains = ['https://www.gushiwen.org']
    start_urls = ['https://www.gushiwen.org']

    def parse(self, response):
        sons = response.xpath('/html/body/div[2]/div[1]/div[@class="sons"]')
        
        for son in sons:
            item = GushiItem()
            item['name'] = son.xpath('div[@class="cont"]/p[1]/a/b/text()').extract()
            item['dynasty'] = son.xpath('div[@class="cont"]/p[2]/a[1]/text()').extract()[0]
            item['author'] = son.xpath('div[@class="cont"]/p[2]/a[2]/text()').extract_first()
            item['poetry'] = son.xpath('div[@class="cont"]/div[@class="contson"]/text()').extract()
            yield item

        next_page = response.xpath('//a[@id="amore"]/@href').extract_first()
        if next_page is not None:
            next_page = "https://www.gushiwen.org"+next_page
            # 添加dont_filter=True  
            # 解决对应问题scrapy提示DEBUG:Filtered offsite request to
            # 再次请求的url与allowed_domains 冲突
            yield scrapy.Request(next_page,callback=self.parse,dont_filter=True)
    

