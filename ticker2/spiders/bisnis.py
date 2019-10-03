# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

from ticker2.items import Ticker2Item
 
class BisnisSpider(scrapy.Spider):
    name = 'bisnis'
    allowed_domains = ['bisnis.com']
    #start_urls = ['http://search.bisnis.com/search/?q=antm']
    start_urls = ['http://search.bisnis.com/search/?q=antam&per_page=%d' %(n) for n in range(1, 210)]
    #manual_urls = ['http://search.bisnis.com/search/?q=antm&per_page=%d' %(n) for n in range(1, 26)]

    # index search Content Extractor 
    # title =>   response.xpath("//*[contains(@class, 'col-md-10 col-sm-12 no-mp')]//h2//text()").extract()
    # link =>   response.xpath("//*[contains(@class, 'col-md-10 col-sm-12 no-mp')]//h2//@href").extract()
    # date => response.xpath("//*[contains(@class, 'col-md-10 col-sm-12 no-mp')]//span//text()[not(ancestor::div[@class='ml-50']) and not(ancestor::p)]").extract()

    # news page content extract    
    # title => response.xpath('//div[@class="description"]/h1//text()').extract()
    # date => response.xpath("//*[contains(@class, 'wrapper-date')]//text()").extract()
    # body => response.xpath("//*[contains(@class, 'col-sm-10')]//text()[not(ancestor::div[@class='liat-juga'])]").extract()

    rules = (
        Rule(LinkExtractor(allow=(),),
             callback="parse_item",
             follow=True),)
    
    def parse(self, response):
        item_links = response.xpath("//*[contains(@class, 'col-md-10 col-sm-12 no-mp')]//h2//@href").extract()
        for a in item_links:
            yield scrapy.Request(a, callback=self.parse_detail_page)

    def parse_detail_page(self, response):
        title = response.xpath('//div[@class="description"]/h1//text()').extract()
        datex = ' '.join(response.xpath("//*[contains(@class, 'wrapper-date')]//text()").extract())
        body = ' '.join(response.xpath("//*[contains(@class, 'col-sm-10')]//text()[not(ancestor::div[@class='liat-juga'])]").extract())

        item = Ticker2Item()
        item['datex'] = datex
        item['title'] = title
        item['content'] = body
        item['link'] = response.url
        yield item
