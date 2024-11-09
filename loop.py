# -*- coding: utf-8 -*-
"""
Created on Fri Nov  8 15:43:39 2024

@author: L
"""

from scrapy.crawler import CrawlerProcess
from scrapy import signals
from scrapy.utils.project import get_project_settings
from twisted.internet import reactor
import time
import mysql.connector

# Import your spider class
from ticker2.spiders.bisnis import BisnisSpider  # Update with your spider path

class MyCrawlerProcess(CrawlerProcess):
    def crawl(self, crawler_or_spidercls, *args, **kwargs):
        # Start the crawl and attach signal to each crawler
        crawler = super().crawl(crawler_or_spidercls, *args, **kwargs)
        crawler.addCallback(self.attach_signal)  # Attach spider_closed signal after crawl starts
        return crawler

    def attach_signal(self, crawler):
        # Connect the spider_closed signal to stop the reactor
        crawler.signals.connect(self.stop_reactor, signal=signals.spider_closed)

    def stop_reactor(self, spider, reason):
        # Stop the reactor when the spider finishes
        print(f"Spider closed: {spider.name}, Reason: {reason}")
        reactor.stop()


# Create a looped crawl function
def looped_crawl(categories):
    process = MyCrawlerProcess(get_project_settings())

    running = True
    while running:
    
        for category in categories:  # Change the range as needed to set the number of runs
            formatted_text = category.replace(" ", "+").rstrip(".")
            print(formatted_text)
            process.crawl(BisnisSpider, category=formatted_text)
            process.start()  # Start the crawl without stopping the reactor

            #answer = input('Repeat [Y/n]? ').strip().lower()
        
            #if answer == 'n':
            #    running = False
            #    reactor.stop()

            import sys
            del sys.modules['twisted.internet.reactor']
            from twisted.internet import reactor
            from twisted.internet import default
            default.install()     
    
        reactor.stop()  # Stop the reactor after the loop completes

         
 


# Establish a connection to your MySQL database
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="-",
    database="finance_nifty50"
)

# Create a cursor object
cursor = conn.cursor()
# Execute a query to fetch a single column
query = "SELECT Name FROM companies"
cursor.execute(query)
# Fetch all results
result = cursor.fetchall()
# Convert the single-column result into a Python list
categories = [row[0] for row in result]
# Close the cursor and connection
cursor.close()
conn.close()
# Run the looped crawl
looped_crawl(categories)
