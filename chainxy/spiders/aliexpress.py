# from __future__ import unicode_literals
import scrapy

import json

import os

import scrapy

from scrapy.spiders import Spider

from scrapy.http import FormRequest

from scrapy.http import Request

from chainxy.items import ChainItem

from scrapy import signals

from scrapy.xlib.pydispatch import dispatcher

from selenium import webdriver

from lxml import etree

from lxml import html

import time

import pdb


class AliExpress(scrapy.Spider):

	name = 'aliexpress'

	domain = 'https://www.aliexpress.com'

	history = []

	output = []

	def __init__(self):

		pass

	
	def start_requests(self):

		url = "https://www.aliexpress.com/category/3710/home-decor/2.html?site=glo&g=y&needQuery=n&tag="

		yield scrapy.Request(url, callback=self.parse) 


	def parse(self, response):

		product_list = response.xpath('//a[contains(@class, "picRind")]/@href').extract()

		for product in product_list:

			link = 'https:' + product

			yield scrapy.Request(link, callback=self.parse_detail)

		next_page = response.xpath('//a[@class="page-next ui-pagination-next"]/@href').extract_first()	

		if next_page:

			next_page = 'https:' + next_page

			yield scrapy.Request(next_page, callback=self.parse, dont_filter=True)


	def parse_detail(self, response):

		with open('test.txt', 'wb') as f:

			f.write(response.body)


	def validate(self, item):

		try:

			return item.replace('\n', '').replace('\t','').replace('\r', '').strip()

		except:

			pass


	def eliminate_space(self, items):

	    tmp = []

	    for item in items:

	        if self.validate(item) != '':

	            tmp.append(self.validate(item))

	    return tmp