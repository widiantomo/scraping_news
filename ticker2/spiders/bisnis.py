# -*- coding: utf-8 -*-
import scrapy

from datetime import datetime
import locale
import re
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
import requests
from textblob import TextBlob
from googletrans import Translator

from ticker2.items import Ticker2Item
 
class BisnisSpider(scrapy.Spider):
    name = 'bisnis'
    allowed_domains = ['bisnis.com']
    #start_urls = ['http://search.bisnis.com/search/?q=antm']
    #start_urls = ['https://search.bisnis.com/?q=aneka+gas+industri&page=%d' %(n) for n in range(1, 2)]
    
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
    
    def __init__(self, category=None, *args, **kwargs):
        super(BisnisSpider, self).__init__(*args, **kwargs)
        self.category = category  # Assign the parameter to an instance variable

    def start_requests(self):
    # Use the parameter in your requests
        start_urls = [f"https://search.bisnis.com/?q={self.category}&page=%d" %(n) for n in range(1, 5)]
        #start_urls = f"http://example.com/{self.category}"
        for url in start_urls:
            yield scrapy.Request(url, self.parse)
    
    def parse(self, response):
        item_links = response.xpath("//*[contains(@class, 'artLink')]//@href").extract()
        for a in item_links:
            yield scrapy.Request(a, callback=self.parse_detail_page)

    def parse_detail_page(self, response):
        #title = response.xpath('//h1[@class="detailsTitleCaption"]/h1//text()').extract()
        title = ' '.join(response.xpath("//*[contains(@class, 'detailsTitleCaption')]//text()").extract())
        datex = ' '.join(response.xpath("//*[contains(@class, 'detailsAttributeDates')]//text()").extract())
        body = ' '.join(response.xpath("//*[contains(@class, 'detailsContent force-17 mt40')]//text()[not(ancestor::div[@class='baca-juga-box'])]").extract())

        # Set locale to Indonesian (for day and month names)
        locale.setlocale(locale.LC_TIME, 'id_ID.UTF-8')  # Adjust locale name if needed
        # Original string
        date_string = datex

        # Strip whitespace and parse the date
        date_string = date_string.strip()
        date_format = "%A, %d %B %Y | %H:%M"

        # Convert to datetime object
        
        try:
            datetime_obj = datetime.strptime(date_string, date_format)
        except:
            datetime_obj = datetime.now()
        
        # Convert to MySQL datetime format
        mysql_datetime = datetime_obj.strftime("%Y-%m-%d %H:%M:%S")
        
        translator = Translator()
        text_indob = translator.translate(body, dest='en')
        text_indo = text_indob.text 
        textindo = TextBlob(text_indo)
        analysis = textindo.sentiment
        if analysis.polarity > 0:
           polarity = 'Positive'
        elif analysis.polarity < 0:
           polarity = 'Negative'
        else:
           polarity = 'Netral'
        #print( polarity)

        item = Ticker2Item()
        item['datex'] = mysql_datetime
        item['title'] = title
        body = re.sub(r'\s{3,}', ' ', body)
        item['content']= body.replace('\n', ' ').replace('\r', '').replace('googletag.cmd.push(function() { googletag.display(\"div-gpt-ad-parallax\"); }); ','')
        item['link'] = response.url
        item['polarity'] = polarity
        yield item
