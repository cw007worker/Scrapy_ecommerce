# -*- coding: utf-8 -*-
import scrapy
import urllib
import time
from urllib.parse import urljoin
from scrapy.loader import ItemLoader
from ecommerce.items import Product


class KijijiSpider(scrapy.Spider):
    name = 'kijiji'
    start_urls = ['http://www.kijiji.ca/']

    def parse(self, response):
        base_url = 'http://www.kijiji.ca/'
        return scrapy.FormRequest.from_response(response, formdata={'keywords': self.query}, callback=self.after_login, meta={'base_url': base_url})

    def after_login(self, response):
        base_url = response.meta['base_url']
        
        item_names = response.css('.enable-search-navigation-flag::text').extract()
        item_names = [i.strip('\n ') for i in item_names]
        
        item_links = [urljoin(base_url, item_path) for item_path in response.css('.enable-search-navigation-flag::attr(href)').extract()]
        
        item_price = response.css('.price::text').extract()
        item_price = [i.strip('\n ') for i in item_price]
        
        item_dates = response.css('.location span::text').extract()
        
        item_locality = response.css('.location::text').extract()
        item_locality = item_locality[0:][::2]
        item_locality = [i.strip('\n ') for i in item_locality]

        for i in range(len(item_dates), len(item_links)):
            item_dates.append('-')

        for i in range(len(item_locality), len(item_links)):
            item_locality.append('-')

        for i in range(len(item_price), len(item_links)):
            item_price.append('-')
        
        for i in range(0, len(item_links)):
            yield {
            'name': item_names[i],
            'link': item_links[i],
            'date': item_dates[i],
            'price': item_price[i],
            'locality': item_locality[i]
            }
        next_page_relative = response.css('.pagination a~ span+ a::attr(href)').extract()
        if next_page_relative != []:
            next_page = urljoin(base_url, next_page_relative[0])
            request = scrapy.Request(url=next_page, callback=self.after_login, meta={'base_url': base_url})
            # request.meta['item'] = item
            yield request












