# -*- coding: utf-8 -*-
import scrapy
import urllib
import time
from urllib.parse import urljoin, quote
from scrapy.loader import ItemLoader
from ecommerce.items import Product


class CraigslistUsSpider(scrapy.Spider):
    name = "craigslist_us"

    def start_requests(self):
        yield scrapy.Request(url='https://geo.craigslist.org/iso/us', callback=self.parse)

    def parse(self, response):
        links = [
            path for path in response.css(".geo-site-list a::attr(href)").extract()]
        item = Product()
        for url in links:
            yield scrapy.Request(url=url, callback=self.parse_subsites, meta={'item': item})

    def parse_subsites(self, response):
        item = response.meta['item']
        base_url = response.url
        mid_url = 'search/sss?query='
        search_url = quote('%s' % self.query)
        sort_url = '&sort=rel'
        query_url = urljoin(base_url, mid_url + search_url + sort_url)

        request = scrapy.Request(
            url=query_url, callback=self.parse_results, meta={'base_url': base_url})
        request.meta['item'] = item
        yield request

    def parse_results(self, response):
        print(response.url)
        base_url = response.meta['base_url']
        item_links = [urljoin(base_url, item_path) for item_path in response.css(
            '.hdrlnk::attr(href)').extract()]
        item_times = response.css(
            '.result-date').css('time::attr(datetime)').extract()
        item_names = response.css('.hdrlnk::text').extract()
        item_price = response.css('.result-price::text').extract()
        item_locality = response.css('.result-hood::text').extract()

        for i in range(len(item_times), len(item_links)):
            item_times.append('-')

        for i in range(len(item_price), len(item_links)):
            item_price.append('-')

            for i in range(len(item_locality), len(item_links)):
                item_locality.append('-')

        for i in range(0, len(item_links)):
            if(len(item_links) > len(item_locality)):
                item_locality.append('-')
            yield {
                'name': item_names[i],
                'link': item_links[i],
                'date': time.strftime("%m/%d/%Y",  time.strptime(str(item_times[i]), "%Y-%m-%d %H:%M")),
                'time': time.strftime("%H:%M",  time.strptime(str(item_times[i]), "%Y-%m-%d %H:%M")),
                'price': item_price[i],
                'locality': item_locality[i],
            }

        next_page_relative = response.css(
            '.bottom .next::attr(href)').extract()
        if next_page_relative != []:
            next_page = urljoin(base_url, next_page_relative[0])
            request = scrapy.Request(
                url=next_page, callback=self.parse_results, meta={'base_url': base_url})
            yield request
