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


class Oberlo(scrapy.Spider):

	name = 'oberlo'

	domain = 'https://app.oberlo.com'

	history = []

	output = []

	def __init__(self):

		pass

		# script_dir = os.path.dirname(__file__)

		# file_path = script_dir + '/input.txt'

		# with open(file_path, 'rb') as text:

		# 	self.input_list =  [ x.strip() for x in text.readlines()]

		dispatcher.connect(self.spider_closed, signals.spider_closed)

		self.myfile = 'output.txt'

		self.page_no = 1
	
	def start_requests(self):

		url = "https://app.oberlo.com/login"

		headers = {
			"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
			"Accept-Encoding": "gzip, deflate, br",
			"Content-Type": "application/x-www-form-urlencoded",
			"Referer": "https://app.oberlo.com/login",
			"Upgrade-Insecure-Requests": "1",
			"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36"
		}

		formdata = {
			"_token": "BH3TUCdpkWMBVjxQYOzwtNQRjdhZgr6kX2G9EnKI",
			"email": "e@mail.com",
			"password": "password"
		}

		yield scrapy.FormRequest(url, headers=headers, method="POST", formdata=formdata, callback=self.parse) 

	def parse(self, response):

		url = "https://app.oberlo.com/ajax/explore/search?category=79&selling_to=US&sort=sellerRateDown&page"

		headers = {
			"Accept": "application/json, text/plain, */*",
			"Accept-Encoding": "gzip, deflate, br",
			"Cookie": "conversion=eyJpdiI6ImtXbHlWeWJUcE01cTUwSTFiYmJwM0E9PSIsInZhbHVlIjoiN2NqZE9ROHNJc2dYYzBCQjl5XC92a3pscDM2a2czV0RCVzIwb2xiaU1ORnk0ZWU4WVZGREVkQzZURjB5cStRZ3BxV2hTd2Fncll2a2lDUVEwaHhLbmJqWk45T2xZOG9PVDhxaHBMUG1rM3JNQ0NCTmp3SE1YRkpXaE5ZcG4rUzhpIiwibWFjIjoiN2U5ZDQ4ODM0MWFmN2M2NDcwZmU5NjcxMWU5MjNiMTE0MWY0YWRmZjJiMTk4MzJjZDBiNzY0NzJlZDI1ZWIyYyJ9; _y=596ada59-8DA8-46F4-819D-36BC60261B29; _shopify_y=596ada59-8DA8-46F4-819D-36BC60261B29; _shopify_fs=2018-11-28T08%3A24%3A06.077Z; _s=59d88830-FADA-4FB3-7167-F3A8523FE232; _shopify_s=59d88830-FADA-4FB3-7167-F3A8523FE232; intercom-session-bxbia7lj=dHplTE5vV2FtMlZiV3lQZjlBS3Y3N0VpR3RVcjVYbXZCNkNnSXpBckpPaEIvelpvbHNwWXJWTGQ0UVVVcnlRMC0taEtPSkp5WkozWTBVS1hQZmdKZGh0Zz09--6e45c091e0f09a18bc52c86831e4a3afc460662a; shippingCountry=eyJpdiI6Ik5uNVd0Z2NoVEY1ZmEwRXhBUjNoQnc9PSIsInZhbHVlIjoiNUFrM2M4MVc2aWkzZHg5ZlRIeUtadz09IiwibWFjIjoiNmE1ZjhjYmI3NTM4OGZhODI0Yzk3ZTkzZGMxZmI0YzFhOGQwZjY2NDU2ZjRlNjU0NWVlMjY3OTNkZTQwZDQyNyJ9; oberlo_session=eyJpdiI6IkZQVityU1hrWUExMWREMWlyK3pzanc9PSIsInZhbHVlIjoiTk02NklpdUlZamt3SGdibzFva1Qyck5rMGo4dzRGVU1SUExMeWtjOTdiYytNVkloeE1SeG5XYjhEUzZIM0ZvVHhCdU1mRXFZTUJ3RUZ3UmFMQSt0TXc9PSIsIm1hYyI6IjlmNDQzNzg5YWNmNjdlMGRlYzQ2ZDUxOGVjYTU2ZWQ4Mzk3ZmI3YjhkOGY5YmU0NDU1ZDA4OGY1MjAxMmYzZmMifQ%3D%3D",
			"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36",
			"X-CSRF-TOKEN": "rC0QDsobEMkJXXfYtdYHo53Ae3TpVIX0eInE7XaZ",
			"X-Requested-With": "XMLHttpRequest"
		}

		yield scrapy.Request(url, headers=headers, method="GET", callback=self.parse_list, dont_filter=True)


	def parse_list(self, response):

		total_count = json.loads(response.body)['data']['paginator']['last_page']

		product_list = json.loads(response.body)['data']['supplyProducts']

		for product in product_list:

			# if product['stats']['orders_count'] > 100:

			self.output.append(product)

		self.page_no += 1

		if self.page_no < 10:

			url = "https://app.oberlo.com/ajax/explore/search?category=79&selling_to=US&sort=sellerRateDown&page="+str(self.page_no)

			headers = {
				"Accept": "application/json, text/plain, */*",
				"Accept-Encoding": "gzip, deflate, br",
				"Cookie": "conversion=eyJpdiI6ImtXbHlWeWJUcE01cTUwSTFiYmJwM0E9PSIsInZhbHVlIjoiN2NqZE9ROHNJc2dYYzBCQjl5XC92a3pscDM2a2czV0RCVzIwb2xiaU1ORnk0ZWU4WVZGREVkQzZURjB5cStRZ3BxV2hTd2Fncll2a2lDUVEwaHhLbmJqWk45T2xZOG9PVDhxaHBMUG1rM3JNQ0NCTmp3SE1YRkpXaE5ZcG4rUzhpIiwibWFjIjoiN2U5ZDQ4ODM0MWFmN2M2NDcwZmU5NjcxMWU5MjNiMTE0MWY0YWRmZjJiMTk4MzJjZDBiNzY0NzJlZDI1ZWIyYyJ9; _y=596ada59-8DA8-46F4-819D-36BC60261B29; _shopify_y=596ada59-8DA8-46F4-819D-36BC60261B29; _shopify_fs=2018-11-28T08%3A24%3A06.077Z; _s=59d88830-FADA-4FB3-7167-F3A8523FE232; _shopify_s=59d88830-FADA-4FB3-7167-F3A8523FE232; intercom-session-bxbia7lj=dHplTE5vV2FtMlZiV3lQZjlBS3Y3N0VpR3RVcjVYbXZCNkNnSXpBckpPaEIvelpvbHNwWXJWTGQ0UVVVcnlRMC0taEtPSkp5WkozWTBVS1hQZmdKZGh0Zz09--6e45c091e0f09a18bc52c86831e4a3afc460662a; shippingCountry=eyJpdiI6Ik5uNVd0Z2NoVEY1ZmEwRXhBUjNoQnc9PSIsInZhbHVlIjoiNUFrM2M4MVc2aWkzZHg5ZlRIeUtadz09IiwibWFjIjoiNmE1ZjhjYmI3NTM4OGZhODI0Yzk3ZTkzZGMxZmI0YzFhOGQwZjY2NDU2ZjRlNjU0NWVlMjY3OTNkZTQwZDQyNyJ9; oberlo_session=eyJpdiI6IkZQVityU1hrWUExMWREMWlyK3pzanc9PSIsInZhbHVlIjoiTk02NklpdUlZamt3SGdibzFva1Qyck5rMGo4dzRGVU1SUExMeWtjOTdiYytNVkloeE1SeG5XYjhEUzZIM0ZvVHhCdU1mRXFZTUJ3RUZ3UmFMQSt0TXc9PSIsIm1hYyI6IjlmNDQzNzg5YWNmNjdlMGRlYzQ2ZDUxOGVjYTU2ZWQ4Mzk3ZmI3YjhkOGY5YmU0NDU1ZDA4OGY1MjAxMmYzZmMifQ%3D%3D",
				"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36",
				"X-CSRF-TOKEN": "rC0QDsobEMkJXXfYtdYHo53Ae3TpVIX0eInE7XaZ",
				"X-Requested-With": "XMLHttpRequest"
			}

			yield scrapy.Request(url, headers=headers, method="GET", callback=self.parse_list, dont_filter=True)


	def spider_closed(self, spider):

		try:

			with open(self.myfile, 'wb') as outfile:

				outfile.write(json.dumps(self.output))

		except Exception as e:

			pass


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



# add product into oberlo

# url 

# https://app.oberlo.com/ajax/explore/addtoimportlist

# header

# Accept: */*
# Accept-Encoding: gzip, deflate, br
# Accept-Language: en-US,en;q=0.9
# Connection: keep-alive
# Content-Length: 415
# Content-Type: application/x-www-form-urlencoded; charset=UTF-8
# Cookie: conversion=eyJpdiI6ImtXbHlWeWJUcE01cTUwSTFiYmJwM0E9PSIsInZhbHVlIjoiN2NqZE9ROHNJc2dYYzBCQjl5XC92a3pscDM2a2czV0RCVzIwb2xiaU1ORnk0ZWU4WVZGREVkQzZURjB5cStRZ3BxV2hTd2Fncll2a2lDUVEwaHhLbmJqWk45T2xZOG9PVDhxaHBMUG1rM3JNQ0NCTmp3SE1YRkpXaE5ZcG4rUzhpIiwibWFjIjoiN2U5ZDQ4ODM0MWFmN2M2NDcwZmU5NjcxMWU5MjNiMTE0MWY0YWRmZjJiMTk4MzJjZDBiNzY0NzJlZDI1ZWIyYyJ9; _y=596ada59-8DA8-46F4-819D-36BC60261B29; _shopify_y=596ada59-8DA8-46F4-819D-36BC60261B29; _shopify_fs=2018-11-28T08%3A24%3A06.077Z; _s=5b1a2bc3-E336-439E-0FE5-A10A03211EFA; _shopify_s=5b1a2bc3-E336-439E-0FE5-A10A03211EFA; shippingCountry=eyJpdiI6ImxhMUpBYjhWaXhxRWlHTmFod0xVb2c9PSIsInZhbHVlIjoiZW1IVXh3czFSZE8ycEF5N1Fna0tudz09IiwibWFjIjoiYjYwN2UwYmMyNTg3YmY1NGNmZDhhNWJiOTBjZGY3NWEzYjllNzBjOWRjMzEzM2ZhMDI4ZGE1OTFhYzkxMDBhZCJ9; oberlo_session=eyJpdiI6IkxLbWFZNURUVm5nTnd4QlFzcmd3UlE9PSIsInZhbHVlIjoiTFd4UnR4SWE0SEQxYjZUc3Q0UkFpeTdETk9YVVJuQW96aWVhQW5LajZMMlBpTU1hK1o2ZmdBUlR3VmxvelZ6eHVDd3ZQR0VKUDlyd3VkUDhGNHVMY0E9PSIsIm1hYyI6ImZkNDhkMmNhNmMyNzZjODM5ZmRhYzY5OTZkOTRkNTllNGZiZmQ2NjQzN2NhOTNlYzMzMjU5YTI3YmQ1NzU0NGYifQ%3D%3D; intercom-session-bxbia7lj=S0NqeVFQeVA5NDk5aUswc0pVdy93QlFKb0VWamgvbDBxaDhrQ05CdXBCN3JPZjlSS3VHRjBTNU9qSlNLOUI5Mi0tYzMrWDdaNWtGVnN0WGcrdlN5MTg4QT09--d8445f4bdc43a2bf597385e9a9c659b9bb194129
# Host: app.oberlo.com
# Origin: https://app.oberlo.com
# Referer: https://app.oberlo.com/explore
# User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36
# X-Requested-With: XMLHttpRequest

# formdata

# id: 
# url: https://www.aliexpress.com/item/FENGRISE-Beach-Party-Novelty-Fruit-Pineapple-Sunglasses-Flamingo-Hawaiian-Funny-Glasses-Goggles-Event-Party-Supplies-Decoration/32811424950.html?spm=a2g01.12278173.layer-ogtaqu.20.5a72a3ce7Mgtko&gps-id=5860734&scm=1007.19882.117176.0&scm_id=1007.19882.117176.0&scm-url=1007.19882.117176.0&pvid=20b80ae8-326f-48f6-8e75-db1b09065ad7
# source: 5