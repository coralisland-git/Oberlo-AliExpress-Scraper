# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import csv

import time

import datetime

from scrapy import signals

from scrapy.contrib.exporter import CsvItemExporter


class ChainxyPipeline(object):

    def __init__(self):

        self.file = {}

        self.headers = ['name', 'address', 'email']

        self.count = 0

        self.file_number = 0


    @classmethod
    def from_crawler(cls, crawler):

        pipeline = cls()

        crawler.signals.connect(pipeline.spider_opened, signals.spider_opened)

        crawler.signals.connect(pipeline.spider_closed, signals.spider_closed)

        return pipeline


    def spider_opened(self, spider):

        self.file = open('%s_%d.csv' % (spider.name, self.file_number), 'w+b')
                
        self.exporter = CsvItemExporter(self.file)
        
        self.exporter.fields_to_export = self.headers
        
        self.exporter.start_exporting()        


    def spider_closed(self, spider):
        
        self.exporter.finish_exporting()
        
        self.file.close()


    def process_item(self, item, spider):

        self.exporter.export_item(item)

        # self.count += 1

        # if self.count % 1000 : 

        #     self.exporter.finish_exporting()

        #     self.file.close()

        #     self.file_number += 1

        #     self.file = open('%s_%d.csv' % (spider.name, self.file_number), 'w+b')
                
        #     self.exporter = CsvItemExporter(file)
            
        #     self.exporter.fields_to_export = self.headers
            
        #     self.exporter.start_exporting()

        return item