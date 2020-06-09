# -*- coding: utf-8 -*-
from scrapy import Spider
from divar_posts.items import DivarPostsItem
from scrapy.loader import ItemLoader
from scrapy.http import Request


class DivarSpiderSpider(Spider):
    name = 'divar_spider'
    allowed_domains = ['divar.ir/']
    start_urls = ['http://divar.ir/s/isfahan/']

    def parse(self, response):
        posts = response.xpath('//*[@class="col-xs-12 col-sm-6 col-xl-4 p-tb-large p-lr-gutter post-card"]/@href').extract()
        for post in posts:
            yield Request('https://divar.ir' + post, callback=self.parse_post, dont_filter = True)

    # post-fields-item__title
    def parse_post(self, response):
        
        post_header_title = response.xpath('//*[@class="post-header__title"]/text()').extract_first()
        
        fields_available_title = response.xpath('//*[@class="post-fields-item__title"]/text()').extract()
        fields_available_value = response.xpath('//*[@class="post-fields-item__value"]/text()').extract()
        title_value_dict = dict(zip(fields_available_title, fields_available_value))
        yield { 'post_title': post_header_title}
        for key,value in list(title_value_dict.items()):
            yield { key :value }
        
