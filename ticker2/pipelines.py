# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html



import mysql.connector
from mysql.connector import errorcode
from scrapy.exceptions import DropItem

class Ticker2Pipeline(object):

    def __init__(self, host, user, password, database, table):
        self.host = "localhost"
        self.user = "root"
        self.password = "-"
        self.database = "finance_nifty50"
        self.table = "newscrawl"

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            host=crawler.settings.get('MYSQL_HOST'),
            user=crawler.settings.get('MYSQL_USER'),
            password=crawler.settings.get('MYSQL_PASSWORD'),
            database=crawler.settings.get('MYSQL_DATABASE'),
            table=crawler.settings.get('MYSQL_TABLE')
        )

    def open_spider(self, spider):
        self.conn = mysql.connector.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            database=self.database
        )
        self.cursor = self.conn.cursor()

        # Check if table exists
        self.cursor.execute(f"SHOW TABLES LIKE '{self.table}'")
        if not self.cursor.fetchone():
            # Create table
            self.cursor.execute(f'''
                CREATE TABLE {self.table} (
                    news_id INT auto_increment NOT NULL,
                    news_date datetime NOT NULL,
                    news_title Text,
                    news_content Text,
                    news_link Text,
                    news_polarity varchar(20),
                    recorded_datetime DATETIME,
                    CONSTRAINT newscrawl_pk PRIMARY KEY (news_id)
                )
            ''')
            self.conn.commit()

    def close_spider(self, spider):
        self.cursor.close()
        self.conn.close()

    def process_item(self, item, spider):
        try:
            self.cursor.execute(f'''
                INSERT INTO {self.table} 
                (news_date, news_title, news_content, news_link, news_polarity, recorded_datetime) 
                VALUES 
                (%s, %s, %s, %s, %s, NOW())
            ''', (item['datex'], item['title'], item['content'], item['link'], item['polarity']))

            self.conn.commit()
            return item
        except mysql.connector.Error as e:
            raise DropItem(f'Error inserting item: {e}')
