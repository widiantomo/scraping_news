# -*- coding: utf-8 -*-
"""
Created on Fri Nov  8 15:43:39 2024

@author: L
"""

from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from twisted.internet import reactor
import time
import mysql.connector

# Import your spider class
from ticker2.spiders.BisnisSpider import bisnis  # Update with your spider path



# Create a looped crawl function
def looped_crawl(categories):
    process = CrawlerProcess(get_project_settings())
    
    for category in categories:  # Change the range as needed to set the number of runs
        formatted_text = category.replace(" ", "+").rstrip(".")    
        process.crawl(bisnis, category=category)
        process.start(stop_after_crawl=False)  # Start the crawl without stopping the reactor
        time.sleep(5)  # Wait 5 seconds between crawls (adjust as needed)

    reactor.stop()  # Stop the reactor after the loop completes


# Establish a connection to your MySQL database
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Superdisk1!",
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
